/**
 * General Configuration
 */

// Configure environmental variables (debugging mode, etc.)
require('babel-register');
const fs = require('fs-extra');
const program = require('commander');
program
  .version(fs.readJsonSync('package.json'))
  .option('-v, --verbose', 'run in verbose mode (verbose)')
  .option('-l, --local', 'when not a Raspberry Pi, run in \'local\' mode')
  .option('-a --alarm', 'Start an alarm right away for testing')
  .parse(process.argv);
process.env.VEBOSE = program.verbose || 'false';
process.env.LOCAL = program.local || 'false';
process.env.ALARM = program.alarm || 'false';

// const PythonShell = require('python-shell');
const debug = require('./modules/debugger.es6');
const mainDebug = debug.init('main');
const init = require('./modules/initialize.es6');

// Boot server:
const app = init.run(__dirname);
const http = require('http').Server(app); // eslint-disable-line
const io = require('socket.io')(http);
const interfaceAddresses = require('interface-addresses');
const addresses = interfaceAddresses();
// const inspect = require('eyespect').inspector();

// Check IP:
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
    mainDebug('NO recognized address - but this is really just localhost...');
    // nIP = 'check address manually';
    // inspect(addresses, 'network interface IPv4 addresses (non-internal)');
  mainDebug(`listening on ${nIP}:${app.get('port')}`);
});


/**
 * Configure Alarm Database and Socket
 */

// Create DB full of alarms alarms:
const db = require('./modules/data.es6');
const alarms = db.alarms;
const sched = require('./modules/scheduler.es6');
const electronics = require('./electronics.es6');

const ClockAlarms = {};
// Create alarms only once:
alarms.find({}, (err, allAlarms) => {
  mainDebug('Registering all alarms (forEach loop):');
  if (err)
    throw err;
  allAlarms.forEach((alarm) => {
    mainDebug('Registering:');
    mainDebug(alarm);
    ClockAlarms[alarm.uniq] = sched.scheduleCron(alarm.title, alarm.schedule);

    if (alarm.running === true) {
      ClockAlarms[alarm.uniq].start();
      mainDebug(`(Register) ^ Started: ${alarm.title}`);
      mainDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
    } else {
      mainDebug(`(Register) x Not starting: ${alarm.title}`);
      mainDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
    }
  });
});

/**
 * Alarm Operations
 */

function deleteAlarm(uniq) {
  alarms.remove({ uniq }, {}, (err, numRemoved) => {
    if (err)
      throw err;
    if (numRemoved <= 0)
      mainDebug(`(deleteAlarm) Removing ${uniq} FAILED!`);
  });
}

function eraseAlarm(uniq) {
  mainDebug(`(eraseAlarm) x Stopped: ${ClockAlarms[uniq].title}`);
  mainDebug(`    - ${uniq} (is running? ${ClockAlarms[uniq].running})`);
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
        mainDebug(`(createAlarm) ^ Started: ${alarm.title}`);
        mainDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
      } else {
        mainDebug(`(createAlarm) x Didnt start: ${alarm.title}`);
        mainDebug(`    - ${alarm.uniq} (is running? ${ClockAlarms[alarm.uniq].running})`);
      }
      socket.emit('alarm event', alarm);
    } else
      mainDebug('WARN: No alarm in insert callback');
  });
}

/**
 * Socket Operations
 */

io.on('connection', (socket) => {
  // Check alarm status (present/away)
  // PythonShell.run('./Python/modules/status.py', (err, results) => {
  //   if (err)
  //     throw err;
  //   mainDebug(`rcvd (pyShellUserStatus): ${results}`);
  //   const userStatus = results;
  //   // const userStatus = results[0];
  electronics.queryStaus((userStatus) => {
    socket.emit('IFTTT event', userStatus);
  });

  // Export all alarms:
  alarms.find({}, (err, allAlarms) => {
    if (err)
      throw err;
    allAlarms.forEach((alarm) => {
      socket.emit('alarm event', alarm);
    });
  });
  // Generate a new blank alarm:
  socket.on('new', () => {
    const uniq = db.generateUniq();
    mainDebug(`(socket.new) Creating new alarm (${uniq})`);
    const alarmState = {
      uniq,
      title: '_New_Alarm_',
      schedule: '0 0 0 * * 0-7',
      running: false,
      saved: false,
    };
    createAlarm(alarmState, socket);
  });
  // Modify an existing alarm:
  socket.on('update', (newState) => {
    mainDebug('(socket.update) Is updated alarm in ClockAlarms? ' +
      `${ClockAlarms.hasOwnProperty(newState.uniq)}`);  // eslint-disable-line
    eraseAlarm(newState.uniq);
    createAlarm(newState, socket);
  });
  // Delete an alarm:
  socket.on('remove', (uniq) => {
    mainDebug(`(socket.remove) Deleting alarm (${uniq})`);
    eraseAlarm(uniq);
  });
});
