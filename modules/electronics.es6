/* initialize debugger */
import {init} from './debugger.es6'
const electronicDebug = init( 'elec' )
electronicDebug( 'Debugger initialized!' )
const moment = require( 'moment' )
// const exec = require('child_process').exec;
// const spawn = require('child_process').spawn;
// const CronJob = require('cron').CronJob;

/**
 * Initialize the Python Controller
 */

const PythonShell = require( 'python-shell' )
const pyshell = new PythonShell( './Python/main.py' )
electronicDebug( 'Started main.py' )
pyshell.on( 'message', ( message ) => {
  electronicDebug( `rcvd (main): ${message}` )
} )
pyshell.on( 'close', ( err ) => {
  if ( err )
    throw err
  electronicDebug( 'Finished and closed main.py' )
} )
pyshell.on( 'error', ( err ) => { throw err } )
// Example: pyshell.send('[all_off]');
pyshell.send( '[LCD] @>start' )

// // Archived:
// function execOnNoSTDOUT(task, cb, altCB, quiet) {
//   exec(task, (childerr, stdout, stderr) => {
//     // if (quiet !== null)
//     //   electronicDebug(`EXEC: ${task}`);
//     if (childerr) electronicDebug(warn(childerr));
//     if (stderr) electronicDebug(error(`stderr: ${stderr}`));
//     if (!stdout)
//       // if (quiet !== null)
//       //   electronicDebug('No STDOUT returned, calling `cb`')
//       cb()
//     else {
//       if (quiet !== null)
//         electronicDebug(stdout);
//       if (altCB)
//         altCB()
//     }
//   });
// }

module.exports = {
  // Toggle LCD Brightness
  brightenLCD() {
    pyshell.send( '[LCD] @>display:>>on' )
  },
  dimLCD() {
    pyshell.send( '[LCD] @>display:>>off' )
  },

  // Universal Method for Interfacing with LCD Display
  queryStatus( cb = false ) {
    PythonShell.run( './Python/modules/status.py', ( err, results ) => {
      if ( err )
        throw err
      // FIXME: Log this result, but quieted for now:
      // electronicDebug(`rcvd (pyShellUserStatus): ${results}`);
      if ( cb )
        cb( results )
    } )
  },

  send( raw ) {
    // *FYI: The most important function:
    pyshell.send( raw )
  },

  startAlarm() {
    pyshell.send( '[alarm]' )
  },

  // // Create python shell to run the predefined alarm script
  // triggerAlarm() {
  //   electronicDebug('Starting Python Alarm Script');
  //   if (process.env.LOCAL === 'false') {
  //     const pyShellAlarm = new PythonShell('./scripts/alarm.py');
  //     // pyShellAlarm.send('THIS COULD BE USEFUL!');
  //     pyShellAlarm.on('message', (message) => {
  //       electronicDebug(`rcvd (ALARM): ${message}`);
  //     });
  //     pyShellAlarm.on('close', (err) => {
  //       if (err)
  //         throw err;
  //       electronicDebug('Completed alarm and closed (ALARM.py)');
  //     });
  //     pyShellAlarm.on('error', (err) => { throw err; });
  //   }
  // },

  // Universal Method for Interfacing with LCD Display
  updateClockDisplay( raw ) {
    let content = ''
    if ( typeof raw === 'object' ) {
      let formattedText = '['
      for ( let i = 0; i < raw.length; i += 1 )
        formattedText = `${formattedText}'${moment().format( raw[i] )}',`
      content = `${formattedText.slice( 0, -1 )}]`
    } else
      content = moment().format( raw )
    const displayText = `[lcd] @>message:>>${content} @>delay:>>1`
    electronicDebug( `Setting char_disp as: ${displayText}` )
    pyshell.send( displayText )
    return displayText
  },
}
