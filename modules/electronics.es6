/* initialize debugger */
import { error, warn, init } from './debugger.es6';
const electronicDebug = init('elec');
electronicDebug('Debugger initialized!');

const exec = require('child_process').exec;
// const spawn = require('child_process').spawn;
const moment = require('moment');
const CronJob = require('cron').CronJob;
const PythonShell = require('python-shell');

function execOnNoSTDOUT(task, cb, altCB, quiet) {
  exec(task, (childerr, stdout, stderr) => {
    // if (quiet !== null)
    //   electronicDebug(`EXEC: ${task}`);
    if (childerr) electronicDebug(warn(childerr));
    if (stderr) electronicDebug(error(`stderr: ${stderr}`));
    if (!stdout)
      // if (quiet !== null)
      //   electronicDebug('No STDOUT returned, calling `cb`')
      cb()
    else {
      if (quiet !== null)
        electronicDebug(stdout);
      if (altCB)
        altCB()
    }
  });
}


// Run Pi-Blaster if not already running for smooth PID control
electronicDebug('Checking if pi-blaster should start');
if (process.env.LOCAL === 'false') {
  const pyShellPiBlaster = new PythonShell('scripts/bootPiBlaster.py');
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


const pyShellLCD = new PythonShell('scripts/lcd.py');
pyShellLCD.on('message', (message) => {
  electronicDebug(`rcvd (pyShellLCD): ${message}`);
});
pyShellLCD.on('close', (err) => {
  if (err)
    throw err;
  electronicDebug('Completed running pyShellLCD.py');
});
pyShellLCD.on('error', (err) => { throw err; });


module.exports = {
  startAlarm() {
    const listProc = "ps aux | grep '[a]larm.py' | awk '{print $2}'";
    execOnNoSTDOUT(listProc, () => {
      this.triggerAlarm();
    });
  },

  // Create python shell to run the predefined alarm script
  triggerAlarm() {
    electronicDebug('Starting Python Alarm Script');
    if (process.env.LOCAL === 'false') {
      const pyShellAlarm = new PythonShell('./scripts/alarm.py');
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
      const checkAlarm = "ps aux | grep '[a]larm.py' | awk '{print $2}'";
      execOnNoSTDOUT(checkAlarm, () => {
        this.updateClockDisplay(['ddd MMM Do', 'h:mm a']);
      }, () => {
        this.updateClockDisplay(['[** Alarm! **]', 'h:mm a']);
      }, true);
    }, () => {
      electronicDebug('Stopped updating Clock Display');
    }, true);
    return updateClock;
  },

  // Check alarm status:
  checkUserStatus() {
    // Deprecated in favor of version in init.es6
    const task = 'python scripts/alarm_status.py';
    exec(task, (childerr, stdout, stderr) => {
      electronicDebug(`EXECUTING: ${task}`);
      if (childerr) electronicDebug(warn(childerr));
      if (stderr) electronicDebug(error(`stderr: ${stderr}`));
      if (stdout) electronicDebug(error(`stdout: ${stdout}`));
    });
  },

  // Toggle LCD Brightness
  brightenLCD() {
    pyShellLCD.send('turn lcd screen for alarm clock on');
  },
  dimLCD() {
    pyShellLCD.send('turn lcd screen for alarm clock off');
  },

  // Universal Method for Interfacing with LCD Display
  updateClockDisplay(raw) {
    if (typeof raw === 'object') {
      let formattedText = '['
      for (let i = 0; i < raw.length; i++)
        formattedText = `${formattedText}'${moment().format(raw[i])}',`;
      formattedText = `${formattedText.slice(0, -1)}]`;
      electronicDebug(`Setting new clock text as: ${formattedText}`);
      pyShellLCD.send(formattedText);
      return formattedText
    }
    const displayText = moment().format(raw);
    electronicDebug(`Setting new clock text as: ${displayText}`);
    pyShellLCD.send(displayText);
    return displayText;
  },
};
