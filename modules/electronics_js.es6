/* initialize debugger */
import { init } from './debugger.es6';
const electronicDebug = init('elec');
electronicDebug('Debugger initialized!');

electronicDebug('Start pi-blaster manually');
if (process.env.LOCAL === 'false') {
  const spawn = require('child_process').spawn;
  spawn('sh', ['scripts/bootPiBlaster.sh']);
}

const fs = require('fs-extra');
const PythonShell = require('python-shell');

// Workaround for working on a local testing platform
let Gpio = {};
let piblaster = {};
let button = {};
if (process.env.LOCAL === 'false') {
  Gpio = require('onoff').Gpio;
  piblaster = require('pi-blaster.js');

  // const led = new Gpio(18, 'out');
  button = new Gpio(4, 'in', 'both');
}

const shaker = 23; // also LED indicator
const buzzer = 18;
piblaster.setPwm(shaker, 0);

// Available Pins:
// GPIO number   Pin in P1 header
//      4              P1-7
//      17             P1-11
//      18             P1-12
//      21             P1-13
//      22             P1-15
//      23             P1-16
//      24             P1-18
//      25             P1-22


module.exports = {
  startAlarm() {
    electronicDebug('Starting Alarm');
    if (process.env.LOCAL === 'false') {
      electronicDebug('shaker, high, buzzer 0.5');
      piblaster.setPwm(shaker, 1);
      piblaster.setPwm(buzzer, 0.5);

      // Create listener if alarm deactivated:
      button.watch((err, value) => {
        electronicDebug(`Button interrupt with value: ${value}`);
        if (err)
          throw err;
        if (value === 1) {
          // led.writeSync(0);
          piblaster.setPwm(shaker, 0);
          piblaster.setPwm(buzzer, 0);
        }
      });
    } else
      electronicDebug('Not starting alarm!');
  },
};

// process.on('SIGINT', () => {
//   if (process.env.LOCAL === 'false')
//     // led.unexport();
//     button.unexport();
// });

// TODO (Adaptation of above):
// /** Create SIGNINT event on user input */
// socket.on('stop', () => {
//   new PythonShell('scripts/all_off.py');
//   console.log('Stopped Python Script Manually');
//   pyshell.childProcess.kill();
// });
