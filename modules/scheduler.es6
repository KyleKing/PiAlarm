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
function controlDisplay(schedule, task, activate) {
  const JOB = new CronJob(schedule, () => {
    schedDebug(`Starting ${task}`);
    if (activate)
      electronics.brightenLCD()
    else
      electronics.dimLCD()
  }, () => {
    schedDebug('Completed a task to change the LCD display')
  }, false);
  return JOB;
}
const weekendActivate = controlDisplay('0 30 8 * * 0,6', 'activate lcd display', true);
const weekdayActivate = controlDisplay('0 15 5 * * 1-5', 'activate lcd display', true);
const deactivate = controlDisplay('0 30 21 * * *', 'deactivate lcd display', false);
weekendActivate.start()
weekdayActivate.start()
deactivate.start()

module.exports = {
  scheduleCron(title, cronSchedule) {
    schedDebug(`Scheduling '${title}' (with sched: ${cronSchedule})`);
    return new CronJob(cronSchedule, () => {
      schedDebug(` ! Starting Alarm ('${title}') ! `);
      electronics.brightenLCD()
      electronics.updateClockDisplay([`[${title}]`, 'h:mm:ss a']);
      electronics.startAlarm();
    }, () => {
      schedDebug(`Alarm ('${title}') stopped.`);
    }, false);
  },
};
