// Configure Express Server

const lgr = require( 'debug' )( 'App:server' )
require( 'dotenv' ).config()

const express = require( 'express' )
const cors = require( 'cors' )
const jwt = require( 'jsonwebtoken' )
const rateLimit = require( 'express-rate-limit' )
const bcrypt = require( 'bcryptjs' )
const GQL = require( './API.js' )
const graphqlHTTP = require( 'express-graphql' )
const CircularJSON = require( 'circular-json' )
const db = require( './Database.js' )

const app = express()
app.set( 'port', ( process.env.PORT || 3001 ) )

// Implement basic rate limiting
app.use( rateLimit( {
	max: 100, // limit each IP to 100 requests per windowMs
	windowMs: 10 * 60 * 1000, // 10 minutes
} ) )

// Create custom logging middle ware
app.use( ( req, res, next ) => {
	lgr( `Connection from ip: ${req.ip}` )
	return next()
} )

// Enable CORS (src: https://stackoverflow.com/a/33483759/3219667)
const whitelist = [
	'http://localhost:3000',
	'http://localhost:5000',
]
app.use( cors( {
	credentials: true,
	origin: function( origin, callback ) {
		const originIsWhitelisted = whitelist.indexOf( origin ) !== -1
		callback( null, originIsWhitelisted )
	},
} ) )

// JWT or Password middle ware for authentication
app.use( async ( req, res, next ) => {
	// Check if request includes authorization string
	if ( typeof ( req.headers.authorization ) === 'string' ) {
		// Check support JWT and Password options for authentication
		const argsAuth = req.headers.authorization.split( ' ' )
		if ( argsAuth.length === 2 ) {
			if ( argsAuth[0] === 'Basic' ) {
				// Check provided password against database
				var passAuth = await db.prom.findOne( db.users, {} ).then( doc => {
					if ( doc.length === 0 )
						throw new Error( 'No user account found' )
					return bcrypt.compareSync( argsAuth[1], doc.hash )
				} ).catch( ( err ) => {
					lgr( err )
					return false
				} )

				if ( passAuth )
					return next()
			} else if ( argsAuth[0] === 'Bearer' ) {
				try {
					if ( jwt.verify( argsAuth[1], process.env.JWT_SECRET ) )  {
						// jwt.decode( argsAuth[1], process.env.JWT_SECRET )
						return next()  // User Authenticated
					}
				} catch ( err ) {
					lgr( err )
					return res.sendStatus( 205 )
				}
			}
		}
		lgr( `Denied access to: '${req.headers.authorization}'` )
	}
	// Otherwise, send 401 - Unauthorized Status Code
	lgr( `UnAuthorized Request: '${CircularJSON.stringify( req.headers )}'` )
	return res.sendStatus( 401 )
} )

// Configure GraphQL endpoint
app.use( '/graphql',  graphqlHTTP( GQL.config ) )

app.listen( app.get( 'port' ), () => {
	lgr( `Running GraphQL server at http://localhost:${app.get( 'port' )}/graphql` )
} )
