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

module.exports = {
  scheduleCron(title, cronSchedule) {
    schedDebug(`Scheduling '${title}' (with sched: ${cronSchedule})`);
    return new CronJob(cronSchedule, () => {
      schedDebug(` ! Starting Alarm ('${title}') ! `);
      electronics.updateClockDisplay(`h:mm:ss a   [${title}]`);
      electronics.startAlarm();
    }, () => {
      schedDebug(`Alarm ('${title}') canceled.`);
    }, false);
  },
};
