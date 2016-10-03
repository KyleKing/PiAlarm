/* initialize debugger */
import { error, warn, init } from './debugger.es6';
const electronicDebug = init('elec');
electronicDebug('Debugger initialized!');

const exec = require('child_process').exec;
const spawn = require('child_process').spawn;
const moment = require('moment');
const CronJob = require('cron').CronJob;
const PythonShell = require('python-shell');

function exec_on_no_stdout(task, cb, altCB, quiet) {
  exec(task, (childerr, stdout, stderr) => {
    if (quiet === null)
      electronicDebug(`EXEC: ${task}`);
    if (childerr) electronicDebug(warn(childerr));
    if (stderr) electronicDebug(error(`stderr: ${stderr}`));
    if (!stdout) {
      if (quiet === null)
        electronicDebug('No STDOUT returned, calling `cb`')
      cb()
    } else {
      if (quiet === null)
        console.log(stdout);
      if (altCB)
        altCB()
    }
  });
}


// Run Pi-Blaster if not already running for smooth PID control
electronicDebug('Checking if pi-blaster should start');
if (process.env.LOCAL === 'false') {
  pyShellPiBlaster = new PythonShell('scripts/pyBootPiBlaster.py');
  pyShellPiBlaster.on('message', (message) => {
    electronicDebug(`rcvd (pyShellPiBlaster): ${message}`);
  });
  pyShellPiBlaster.on('close', (err) => {
    if (err)
      throw err;
    electronicDebug('Completed running pyShellPiBlaster.py');
  });
  pyShellPiBlaster.on('error', (err) => { throw err; });
}


let pyShellLCD = {};
if (process.env.LOCAL === 'false')
  pyShellLCD = new PythonShell('scripts/lcd.py');

module.exports = {
  startAlarm() {
    const listProc = "ps aux | grep '[p]ython alarm.py' | awk '{print $2}'";
    exec_on_no_stdout(listProc, () => {
      this.triggerAlarm();
    });
  },

  // Create python shell to run the predefined alarm script
  triggerAlarm() {
    electronicDebug('Starting Python Alarm Script');
    if (process.env.LOCAL === 'false') {
      const pyShellAlarm = new PythonShell('scripts/alarm.py');
      // pyShellAlarm.send('THIS COULD BE USEFUL!');
      pyShellAlarm.on('message', (message) => {
        electronicDebug(`rcvd (ALARM): ${message}`);
      });
      pyShellAlarm.on('close', (err) => {
        if (err)
          throw err;
        electronicDebug('Completed alarm and closed (ALARM.py)');
      });
      pyShellAlarm.on('error', (err) => { throw err; });
    }
  },

  // Update display on 1 minute intervals:
  startClock() {
    const updateClock = new CronJob('0 * * * * *', () => {
      const checkAlarm = "ps aux | grep '[p]ython alarm.py' | awk '{print $2}'";
      exec_on_no_stdout(checkAlarm, () => {
        this.updateClockDisplay('h:mm a        ddd - MMM Do');
      }, () => {
        this.updateClockDisplay('h:mm a            [ALARM!]');
      }, true);
    }, () => {
      electronicDebug('Stopped updating Clock Display');
    }, true);
    return updateClock;
  },

  // Universal Method for Interfacing with LCD Display
  updateClockDisplay(format) {
    const displayText = moment().format(format);
    if (process.env.LOCAL === 'false')
      pyShellLCD.send(displayText);
    electronicDebug(`Set New Clock Text: ${displayText}`);
    return displayText;
  },
};
