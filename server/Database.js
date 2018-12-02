// Database Management Utilities

const lgr = require( 'debug' )( 'App:database' )
require( 'dotenv' ).config()

const bcrypt = require( 'bcryptjs' )
const Datastore = require( 'nedb' )
const moment = require( 'moment' )
const prom = require( './DatabasePromises.js' )

// Load alarms database
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
			enabled: true,
			schedule,
			title: `ALARM: ${uniq} - ${pref}`,
			uniq,
		} )
	} )
}

// Check number of alarms in database
prom.count( alarms, {} )
	.then( ( count ) => {
		lgr( `Found ${count} alarms` )
		if ( count === 0 ) {
			// If no data present, populate with a random alarm
			lgr( 'Initializing new Alarms data store' )
			seedAlarmDB()
		} else {
			// Otherwise, log database initial state for debugging
			lgr( 'Loading existing Alarms data store' )
			alarms.find( {}, ( err, docs ) => {
				if ( err ) throw new Error( err )
				docs.forEach( ( doc ) => {
					lgr( `>> (${doc.title}): uniq: ${doc.uniq}, sched: ${doc.schedule}, enabled: ${doc.enabled}` )
				} )
			} )
		}
	} )

// Remove any existing users (passwords) then create the single user account
const users = new Datastore( { autoload: true, filename: './data/users.db' } )
users.remove( {}, { multi: true }, ( remErr, numRemoved ) => {
	if ( remErr )
		lgr( remErr )

	// Insert new user based on the password variable set in the .env file
	users.insert( {
		hash: bcrypt.hashSync( process.env.PASSWORD, bcrypt.genSaltSync( 14 ) ),
	}, ( insErr ) => {
		if ( insErr )
			lgr( insErr )
	} )
} )

module.exports = { alarms, generateUniq, prom, users }
