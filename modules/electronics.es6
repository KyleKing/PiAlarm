/* initialize debugger */
import { error, warn, init } from './debugger.es6';
const electronicDebug = init('elec');
electronicDebug('Debugger initialized!');

// const fs = require('fs-extra');
const PythonShell = require('python-shell');
const exec = require('child_process').exec;

electronicDebug('Testing if pi-blaster should start:');
if (process.env.LOCAL === 'false') {
  const spawn = require('child_process').spawn; // eslint-disable-line
  const listProcPiB = 'ps aux | grep [b]laster';
  exec(listProcPiB, (childerr, stdout, stderr) => {
    electronicDebug(`Checking for running Pi-B: ${listProcPiB}`);
    electronicDebug('stdout:');
    if (childerr) electronicDebug(warn(childerr));
    if (stderr) electronicDebug(error(`stderr: ${stderr}`));
    if (stdout) {
      electronicDebug('Something matching pi-blaster is running');
      console.log(stdout);
    } else {
      electronicDebug('Something matching pi-blaster is running');
      spawn('sh', ['bootPiBlaster.sh']);
    }
  });
}

// FIXME: this should be a class and not a series of functions:

function triggerAlarm() {
  electronicDebug('Starting Alarm');
  if (process.env.LOCAL === 'false') {
    const pyshell = new PythonShell('./alarm.py');
    // TODO: sends a message to the Python script via stdin
    // pyshell.send('msg');
    pyshell.on('message', (message) => {
      electronicDebug(`rcvd (ALARM): ${message}`);
    });
    pyshell.on('close', (err) => {
      if (err)
        throw err;
      electronicDebug('finished and closed (ALARM.py)');
    });
    pyshell.on('error', (err) => { throw err; });
  } else
    electronicDebug('Not starting alarm!');
}

function isAlarmRunning() {
  const listProc = "ps aux | grep '[p]ython alarm.py' | awk '{print $2}'";
  exec(listProc, (childerr, stdout, stderr) => {
    electronicDebug(`Getting PID list: ${listProc}`);
    if (childerr) electronicDebug(warn(childerr));
    if (stderr) electronicDebug(error(`stderr: ${stderr}`));
    if (stdout) {
      electronicDebug('stdout:');
      // console.log(stdout);
      const PIDs = stdout.trim().split(/\W+/);
      console.log(PIDs);
      const PIDsLen = PIDs.length;
      if (PIDsLen > 0)
        electronicDebug(' X Alarm running, don\'t start a second');
      // else {
      //   electronicDebug(' ✔ No alarm running, carry on with starting alarm');
      //   triggerAlarm();
      // }
    } else {
      electronicDebug(' ✔ No alarm running, carry on with starting alarm');
      triggerAlarm();
    }
  });

  // FIXME: Make only one pi-blaster instance running:
  const listProcPiB = 'ps aux | grep [b]laster';
  exec(listProcPiB, (childerr, stdout, stderr) => {
    electronicDebug(`Checking for running Pi-B: ${listProcPiB}`);
    electronicDebug('stdout:');
    if (childerr) electronicDebug(warn(childerr));
    if (stderr) electronicDebug(error(`stderr: ${stderr}`));
    if (stdout)
      console.log(stdout);
  });
}

module.exports = {
  startAlarm() {
    isAlarmRunning();
  },
};
