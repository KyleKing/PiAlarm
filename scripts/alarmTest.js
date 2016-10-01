console.log('Manually test the alarm script from a JS script');

console.log('Start pi-blaster manually');
const spawn = require('child_process').spawn; // eslint-disable-line
spawn('sh', ['scripts/bootPiBlaster.sh']);

const PythonShell = require('python-shell');

function triggerAlarm() {
  console.log('Starting Alarm');
  // Run the actual alarm:
  const pyshell = new PythonShell('./alarm.py');
  // TODO: sends a message to the Python script via stdin
  // pyshell.send('msg');
  pyshell.on('message', (message) => {
    console.log(`rcvd (ALARM): ${message}`);
  });
  pyshell.on('close', (err) => {
    if (err)
      throw err;
    console.log('finished and closed (ALARM.py)');
  });
  pyshell.on('error', (err) => { throw err; });
}

triggerAlarm();
