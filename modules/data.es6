/* initialize debugger */
import {existsSync, init} from './debugger.es6'
const dataDebug = init( 'data' )
dataDebug( 'Debugger initialized!' )

const Datastore = require( 'nedb' )
const moment = require( 'moment' )
const alarms = new Datastore( {
  autoload: true,
  filename: './data/alarms',
} )

function generateUniq() {
  const randVal = Math.floor( Math.random() * ( 50 ) )
  const uniq = moment().format( `YYMMDD_mm-ss_${randVal}` )
  return uniq
}

function freshCron() {
  dataDebug( 'Creating a fresh cron DB with fake data' )
  const prefs = [1]
  const schedule = '20 0,5,10,15,20,25,30,35,40,45,50,55 * * * *'
  prefs.forEach( ( pref ) => {
    const uniq = generateUniq()
    alarms.insert( {
      running: true,
      schedule,
      title: `ALARM: ${uniq} - ${pref}`,
      uniq,
    } )
  } )
}

if ( existsSync( './data/alarms' ) ) {
  dataDebug( 'Using existing cron DB' )
  alarms.find( {}, ( err, docs ) => {
    if ( err ) throw new Error( err )
    docs.forEach( ( doc ) => {
      dataDebug( `Found (${doc.title}): uniq: ${doc.uniq}, sched: ${doc.schedule}` )
    } )
  } )
} else
  freshCron()

module.exports = {alarms, generateUniq}
