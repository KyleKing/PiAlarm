#!/usr/bin/env node

/**
 * General Configuration
 */

require('babel-register');
const fs = require('fs-extra');
const program = require('commander');
program
  .version(fs.readJsonSync('package.json'))
  .option('-d, --debug', 'run in debug mode (verbose)')
  .option('-l, --local', 'when not a Raspberry Pi, run in \'local\' mode')
  .option('--alarm', 'Start an alarm right away for testing')
  .parse(process.argv);
process.env.DEBUG = program.debug || 'false';
process.env.LOCAL = program.local || 'false';
process.env.ALARM = program.alarm || 'false';

/* initialize debugger */
const debug = require('./modules/debugger.es6');
const initDebug = debug.init('init');
initDebug('Debugger initialized!');

/* Now everything else */
const path = require('path');
const secret = require('./secret.json');
const bodyParser = require('body-parser');
const express = require('express');
const cookieParser = require('cookie-parser');
const session = require('cookie-session');
// const flash = require('connect-flash');
// // const nunjucks = require('nunjucks');
// // const resourcesPath = path.join(__dirname, '..', 'common');
const app = express();
app.set('port', 3000);
app.use(express.static('dist'));
app.use(bodyParser.urlencoded({ extended: false }));

const users = require('express-users');
const userRouter = users({
  store: 'nedb',
  nedb: { filename: `${__dirname}/data/users` },
  data: [
    { username: secret.username, pwd: secret.pwd},
  ],
});

app.use(cookieParser());
app.use(session({
  resave: false,
  saveUninitialized: false,
  secret: secret.passport,
}));
app.use(userRouter.passport.initialize());
app.use(userRouter.passport.session());
app.use(userRouter);

// app.use(flash());
// // nunjucks.configure(path.join(resourcesPath, 'views'), {
// //   autoescape: true,
// //   express: app,
// // });
// app.use((req, res, next) => {
//   const messages = {
//     error: req.flash('error'),
//     success: req.flash('success'),
//     info: req.flash('info'),
//   };
//   res.locals.flash = messages;
//   next();
// });


// ////////////////////////////
// Set Routes and Launch Server
// ////////////////////////////

app.get('/', (req, res) => {
  if (req.isAuthenticated())
    return res.redirect('/app');
  return res.sendFile(path.resolve(`${__dirname}/views/login.html`));
});
app.get('/app', (req, res) => {
  if (req.isAuthenticated() && req.user.username === secret.username) {
    initDebug(`User (${secret.username}) logged in to /app`);
    return res.sendFile(path.resolve(`${__dirname}/views/index.html`));
  }
  return res.sendFile(path.resolve(`${__dirname}/views/login.html`));
  // return res.redirect('/');
});

// Respond to Maker requests:
app.get(`/${secret.maker}/:id`, (req) => {
  if (req.params.id === 'enter')
    console.log('Make sure Alarm is activated');
  else if (req.params.id === 'exit')
    console.log('Make sure Alarm is activated');
  else
    console.log('WARN: Unknown Maker http get request');
});

const http = require('http').Server(app); // eslint-disable-line
const io = require('socket.io')(http);
const interfaceAddresses = require('interface-addresses');
const addresses = interfaceAddresses();
// const inspect = require('eyespect').inspector();

http.listen(app.get('port'), () => {
  // Filter through possible IP addresses
  let nIP = '';
  if (addresses.en0)
    nIP = addresses.en0;
  else if (addresses.en1)
    nIP = addresses.en1;
  else if (addresses.wlan0)
    nIP = addresses.wlan0;
  else if (addresses.eth0)
    nIP = addresses.eth0;
  else
    initDebug('NO recognized address - but this is really just localhost...');
    // nIP = 'check address manually';
    // inspect(addresses, 'network interface IPv4 addresses (non-internal)');
  initDebug(`listening on ${nIP}:${app.get('port')}`);
});


/**
 * Configure the electronics and cron tasks:
 */

// Create DB full of alarms alarms:
const db = require('./modules/data.es6');
const alarms = db.alarms;
const sched = require('./modules/scheduler.es6');
const electronics = require('./modules/electronics.es6');
electronics.startClock();
const PythonShell = require('python-shell');

if (process.env.LOCAL === 'false') {
  const pyshell = new PythonShell('scripts/all_off.py');
  initDebug('Started all_off.py');
  pyshell.on('message', (message) => {
    initDebug(`rcvd (ALL_OFF): ${message}`);
  });
  pyshell.on('close', (err) => {
    if (err)
      throw err;
    initDebug('Finished and closed all_off.py');
  });
  pyshell.on('error', (err) => { throw err; });
}

// ////////////////////////////
// Initialize Alarms
// //////////////////////////

const ClockAlarms = {};
// Create alarms only once:
alarms.find({}, (err, allAlarms) => {
  initDebug('Registering all alarms (forEach loop):');
  if (err)
    throw err;
  allAlarms.forEach((alarm) => {
    initDebug('Registering:');
    initDebug(alarm);
    ClockAlarms[alarm.uniq] = sched.scheduleCron(alarm.title, alarm.schedule);

    if (alarm.running === true) {
      ClockAlarms[alarm.uniq].start();
      initDebug(`(Register) ^ Started: ${alarm.title}`);
      initDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
    } else {
      initDebug(`(Register) x Not starting: ${alarm.title}`);
      initDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
    }
  });
});


// ////////////////////////////
// Alarm Operations
// ////////////////////////////

function deleteAlarm(uniq) {
  alarms.remove({ uniq }, {}, (err, numRemoved) => {
    if (err)
      throw err;
    if (numRemoved <= 0)
      initDebug(`(deleteAlarm) Removing ${uniq} FAILED!`);
  });
}

function eraseAlarm(uniq) {
  initDebug(`(eraseAlarm) x Stopped: ${ClockAlarms[uniq].title}`);
  initDebug(`    - ${uniq} (is running? ${ClockAlarms[uniq].running})`);
  ClockAlarms[uniq].stop();
  ClockAlarms[uniq] = null;
  deleteAlarm(uniq);
}

function createAlarm(alarmState, socket) {
  alarms.insert(alarmState, (err, alarm) => {
    if (err)
      throw err;
    if (alarm) {
      ClockAlarms[alarm.uniq] = sched.scheduleCron(alarm.title, alarm.schedule);
      if (alarm.running === true) {
        ClockAlarms[alarm.uniq].start();
        initDebug(`(createAlarm) ^ Started: ${alarm.title}`);
        initDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
      } else {
        initDebug(`(createAlarm) x Didn't start: ${alarm.title}`);
        initDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
      }
      socket.emit('alarm event', alarm);
    } else
      initDebug('WARN: No alarm in insert callback');
  });
}

// ////////////////////////////
// Socket Actions
// ////////////////////////////

io.on('connection', (socket) => {
  alarms.find({}, (err, allAlarms) => {
    if (err)
      throw err;
    allAlarms.forEach((alarm) => {
      socket.emit('alarm event', alarm);
    });
  });

  socket.on('new', () => {
    const uniq = db.generateUniq();
    initDebug(`(socket.new) Creating new alarm (${uniq})`);
    const alarmState = {
      uniq,
      title: '_New_Alarm_',
      schedule: '10 0 5 * * 1-5',
      running: false,
      saved: false,
    };
    createAlarm(alarmState, socket);
  });

  socket.on('update', (newState) => {
    initDebug(`(socket.update) Is updated alarm in ClockAlarms? ${ClockAlarms.hasOwnProperty(newState.uniq)}`);  // eslint-disable-line
    eraseAlarm(newState.uniq);
    createAlarm(newState, socket);
  });

  socket.on('remove', (uniq) => {
    initDebug(`(socket.remove) Deleting alarm (${uniq})`);
    eraseAlarm(uniq);
  });
});
