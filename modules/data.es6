/* initialize debugger */
import { init, existsSync } from './debugger.es6';
const dataDebug = init('data');
dataDebug('Debugger initialized!');

const Datastore = require('nedb');
const moment = require('moment');
const alarms = new Datastore({
  filename: './data/alarms',
  autoload: true,
});

function generateUniq() {
  const randVal = Math.floor(Math.random() * (20));
  const uniq = moment().format(`YYYY_DDDD_kk_mm_ss_${randVal}`);
  return uniq;
}

function freshCron() {
  dataDebug('Creating a fresh cron DB with fake data');
  const prefs = [1];
  const schedule = '0 0 0 * * *';
  prefs.forEach((pref, index) => {
    const uniq = generateUniq();
    alarms.insert({
      uniq,
      title: `WORK: ${uniq}`,
      schedule,
      running: true,
    });
  });
}

if (existsSync('./data/alarms')) {
  dataDebug('Using existing cron DB');

  // // Check if more documents in need:
  // alarms.count({}, (err, count) => {
  //   if (err)
  //     throw err;
  //   if (count < 2)
  //     freshCron();
  // });

  alarms.find({}, (err, docs) => {
    if (err) throw new Error(err);
    docs.forEach((doc) => {
      dataDebug(`Found (${doc.title}): uniq: ${doc.uniq}, sched: ${doc.schedule}`);
    });
  });
} else
  freshCron();

module.exports = { alarms, generateUniq };
