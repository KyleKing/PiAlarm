// Database Management Utilities

const lgr = require( 'debug' )( 'App:database' )
require( 'dotenv' ).config()

const bcrypt = require( 'bcryptjs' )
const Datastore = require( 'nedb' )
const moment = require( 'moment' )
const prom = require( './DatabasePromises.js' )

const alarms = new Datastore( { autoload: true, filename: './data/alarms.db' } )

// Generate Unique Identifier for Each Alarm
function generateUniq() {
	const randVal = Math.floor( Math.random() * ( 50 ) )
	return moment().format( `YYMMDD_mm-ss_${randVal}` )
}

// Create placeholder alarm
function seedAlarmDB() {
	lgr( 'Creating fresh cron DB with fake data' )
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


// If no data present, populate with a random alarm
prom.count( alarms, {} )
	.then( ( count ) => {
		lgr( `Found ${count} alarms` )
		if ( count === 0 ) {
			lgr( 'Initializing new Alarms data store' )
			seedAlarmDB()
		} else {
			lgr( 'Loading existing Alarms data store' )
			alarms.find( {}, ( err, docs ) => {
				if ( err ) throw new Error( err )
				docs.forEach( ( doc ) => {
					lgr( `>> (${doc.title}): uniq: ${doc.uniq}, sched: ${doc.schedule}` )
				} )
			} )
		}
	} )

// Remove any existing passwords, then create single user account
const users = new Datastore( { autoload: true, filename: './data/users.db' } )
users.remove( {}, { multi: true }, ( remErr, numRemoved ) => {
	// Simple wrapper to only log error if one found
	if ( remErr )
		lgr( remErr )

	users.insert( {
		hash: bcrypt.hashSync( process.env.PASSWORD, bcrypt.genSaltSync( 14 ) ),
	}, ( insErr ) => {
		if ( insErr )
			lgr( insErr )
	} )
} )

module.exports = { alarms, generateUniq, prom, users }
