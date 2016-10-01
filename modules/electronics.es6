/* initialize debugger */
import { error, warn, init } from './debugger.es6';
const electronicDebug = init('elec');
electronicDebug('Debugger initialized!');

const exec = require('child_process').exec;
const spawn = require('child_process').spawn;
const moment = require('moment');
const CronJob = require('cron').CronJob;

function exec_on_no_stdout(task, cb) {
  exec(task, (childerr, stdout, stderr) => {
    electronicDebug(`EXEC: ${task}`);
    if (childerr) electronicDebug(warn(childerr));
    if (stderr) electronicDebug(error(`stderr: ${stderr}`));
    if (!stdout) {
      electronicDebug('No STDOUT returned, calling `cb`')
      cb()
    } else {
      electronicDebug('REturned STDOUT (not calling `cb`');
      console.log(stdout);
    }
  });
}

electronicDebug('Checking if pi-blaster should start');
if (process.env.LOCAL === 'false') {
  exec_on_no_stdout('ps aux | grep [b]laster', () => {
    electronicDebug('Starting pi-blaster');
    spawn('sh', ['scripts/bootPiBlaster.sh']);
  });
}

const PythonShell = require('python-shell');
let pyshell = {};
if (process.env.LOCAL === 'false')
  pyshell = new PythonShell('scripts/lcd.py');

module.exports = {
  startAlarm() {
    const listProc = "ps aux | grep '[p]ython alarm.py' | awk '{print $2}'";
    exec_on_no_stdout(listProc, () => {
      this.triggerAlarm();
    });
  },

  triggerAlarm() {
    electronicDebug('Starting Alarm');
    if (process.env.LOCAL === 'false') {
      const pyshell = new PythonShell('scripts/alarm.py');
      // pyshell.send('THIS COULD BE USEFUL!');
      pyshell.on('message', (message) => {
        electronicDebug(`rcvd (ALARM): ${message}`);
      });
      pyshell.on('close', (err) => {
        if (err)
          throw err;
        electronicDebug('Completed alarm and closed (ALARM.py)');
      });
      pyshell.on('error', (err) => { throw err; });
    }
  },

  startClock() {
    const updateClock = new CronJob('0 * * * * *', () => {
      const checkAlarm = "ps aux | grep '[p]ython alarm.py' | awk '{print $2}'";
      exec_on_no_stdout(checkAlarm, () => {
        this.updateClockDisplay('h:mm a      [ALARM]');
      });
    }, () => {
      electronicDebug('Stopped updating Clock Display');
    }, true);
    return updateClock;
  },

  // Universal Method for Interfacing with LCD Display
  updateClockDisplay(format) {
    const displayText = moment().format(format);
    if (process.env.LOCAL === 'false')
      pyshell.send(displayText);
    electronicDebug(`Set New Clock Text: ${displayText}`);
    return displayText;
  },
};
