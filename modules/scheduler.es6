// Quick CRON guide
// second         0-59
// minute         0-59
// hour           0-23
// day of month   0-31
// month          0-12 (or names, see below)
// day of week    0-7 (Sun-Sat) (7 = Sun)

/* initialize debugger */
import { init } from './debugger.es6';
import { updateClockDisplay } from './clock.es6';
import { startAlarm } from './electronics.es6';

const schedDebug = init('sched');
schedDebug('Debugger initialized!');

const CronJob = require('cron').CronJob;

// FIXME: Make more concise to run alarm right away
if (process.env.ALARM === true || process.env.ALARM === 'true')
  startAlarm();

module.exports = {
  // Schedule an alarm:
  scheduleCron(title, cronSchedule) {
    return new CronJob(cronSchedule, () => {
      schedDebug(' ! Starting Alarm ! ');
      updateClockDisplay(`[${title}] \n h:mm:ss a`);
      startAlarm();
    }, () => {
      schedDebug(`Alarm ('${title}') canceled.`);
    }, false);
  },
};
