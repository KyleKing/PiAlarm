// Database Management Utilities

const lgr = require( 'debug' )( 'App:database' )
require( 'dotenv' ).config()

const bcrypt = require( 'bcryptjs' )
// const doAsync = require( 'doasync' )
const Datastore = require( 'nedb' )
const moment = require( 'moment' )

// Wrap common NedB functions as promises
// TODO: There has to be an easier way to do this

function count( db, opt ) {
	return new Promise( ( resolve, reject ) => {
		db.count( opt, ( err, count ) => {
			if ( err )
				reject( err )
			else
				resolve( count )
		} )
	} )
}
function find( db, opt ) {
	return new Promise( ( resolve, reject ) => {
		db.find( opt, ( err, docs ) => {
			if ( err )
				reject( err )
			else
				resolve( docs )
		} )
	} )
}
function findOne( db, opt ) {
	return new Promise( ( resolve, reject ) => {
		db.findOne( opt, ( err, doc ) => {
			if ( err )
				reject( err )
			else
				resolve( doc )
		} )
	} )
}
function insert( db, opt ) {
	return new Promise( ( resolve, reject ) => {
		db.insert( opt, ( err, doc ) => {
			if ( err )
				reject( err )
			else
				resolve( doc )
		} )
	} )
}
function remove( db, opt ) {
	return new Promise( ( resolve, reject ) => {
		db.remove( opt, ( err, numRemoved ) => {
			if ( err )
				reject( err )
			else
				resolve( numRemoved )
		} )
	} )
}


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


// Load Alarms database, if no data present, populate with a random alarm
const alarms = new Datastore( { autoload: true, filename: './data/alarms.db' } )
// Demo Promises
// doAsync( alarms ).count( {} )
count( alarms, {} )
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

// alarms.insert( { todo: 'replace' }, ( err, newDoc ) => {
// 	lgr( `todo - newDoc?: ${newDoc}` )
// 	return newDoc
// } )

// lgr( 'next?' )

// doAsync( alarms ).insert( { 'todo': true } )
// 	.then( doc => {
// 		lgr( `todo - doc?: ${doc}` )
// 		return doc
// 	} ).catch( err => lgr( err ) )

// doAsync( alarms ).count( )
// 	.then( count => {
// 		lgr( `todo - count?: ${count}` )
// 		return count
// 	} ).catch( err => lgr( err ) )

// // }
// // that()


// Remove any existing passwords, then create single user account
const users = new Datastore( { autoload: true, filename: './data/users.db' } )
users.remove( {}, { multi: true }, ( err, numRemoved ) => {
	// Simple wrapper to only log error if one found
	if ( err )
		lgr( err )

	users.insert( {
		hash: bcrypt.hashSync( process.env.PASSWORD, bcrypt.genSaltSync( 14 ) ),
	}, ( err ) => {
		if ( err )
			lgr( err )
	} )
} )

const prom = {
	count,
	find,
	findOne,
	insert,
	remove,
}
module.exports = { alarms, generateUniq, prom, users }
