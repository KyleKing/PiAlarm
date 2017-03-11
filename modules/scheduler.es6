// Quick CRON guide
// second         0-59
// minute         0-59
// hour           0-23
// day of month   0-31
// month          0-12
// day of week    0-6 (Sun-Sat)

/* initialize debugger */
import { init } from './debugger.es6';
const electronics = require('./electronics.es6');

const schedDebug = init('sched');
schedDebug('Debugger initialized!');

const CronJob = require('cron').CronJob;

// Allow immediate alarm test:
if (process.env.ALARM !== 'false')
  electronics.startAlarm();
else
  schedDebug(`process.env.ALARM is false - ${process.env.ALARM}`);


// Turn the display on when people should be around
function sendOnCron(schedule, msg) {
  const JOB = new CronJob(schedule, () => {
    schedDebug(`Sending ${msg}`);
    electronics.send(msg)
  }, () => {
    schedDebug('Completed sending a msg to the main Python thread')
  }, false);
  return JOB;
}
const weekendActivate = sendOnCron('50 30 8 * * 0,6', '[LCD] @>display:>>on');
const weekdayActivate = sendOnCron('50 30 6 * * 1-5', '[LCD] @>display:>>on');
const deactivate = sendOnCron('50 30 21 * * *', '[LCD] @>display:>>off');
weekendActivate.start();
weekdayActivate.start();
deactivate.start();

// Keep Pi and node app awake:
const everyFive = '0,5,10,15,20,25,30,35,40,45,50,55'
// const insomnia = sendOnCron(`20 ${everyFive} * * * *`, '[lcd] @>insomnia');
// insomnia.start()

function WOKE(schedule) {
  const JOB = new CronJob(schedule, () => {
    electronics.queryStatus();
  }, () => {
    schedDebug('Completed WOKE (Insonia V2) task')
  }, false);
  return JOB;
}
const insomnia = WOKE(`20 ${everyFive} * * * *`);
insomnia.start()

module.exports = {
  // Schedule the alarms in the database:
  scheduleCron(title, cronSchedule) {
    schedDebug(`Scheduling '${title}' (with sched: ${cronSchedule})`);
    return new CronJob(cronSchedule, () => {
      schedDebug(` ! Starting Alarm ('${title}') ! `);
      electronics.brightenLCD();
      electronics.updateClockDisplay([`[${title}]`, 'h:mm:ss a']);
      electronics.startAlarm();
    }, () => {
      schedDebug(`Alarm ('${title}') stopped.`);
    }, false);
  },
};
