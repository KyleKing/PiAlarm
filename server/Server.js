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

module.exports = {
	init() {
		const app = express()
		app.set( 'port', ( process.env.PORT || 3001 ) )

		// Implement basic rate limiting
		app.use( rateLimit( {
			max: 100, // limit each IP to 100 requests per windowMs
			windowMs: 10 * 60 * 1000, // 10 minutes
		} ) )

		// Create custom logging middle ware
		app.use( ( req, res, next ) => {
			lgr( `ip: ${req.ip}` )
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

		// TODO: store password hash in database, manually  initialized once
		var hash = bcrypt.hashSync( process.env.PASSWORD, bcrypt.genSaltSync( 14 ) )

		// JWT or Password middle ware for authentication
		app.use( ( req, res, next ) => {
			// Check if request includes authorization string
			if ( typeof ( req.headers.authorization ) === 'string' ) {
				// Check support JWT and Password options for authentication
				const argsAuth = req.headers.authorization.split( ' ' )
				if ( argsAuth.length === 2 ) {
					if ( argsAuth[0] === 'Basic' && bcrypt.compareSync( argsAuth[1], hash ) )
						return next()  // User Authenticated
					if ( argsAuth[0] === 'Bearer' && jwt.verify( argsAuth[1], process.env.JWT_SECRET ) ) {
						// jwt.decode( argsAuth[1], process.env.JWT_SECRET )
						return next()  // User Authenticated
					}
				}
			}
			// Otherwise, send 401 - Unauthorized Status Code
			return res.sendStatus( 401 )
		} )

		// Configure GraphQL endpoint
		app.use( '/graphql',  graphqlHTTP( GQL.config ) )

		app.listen( app.get( 'port' ), () => {
			lgr( `Running GraphQL server at http://localhost:${app.get( 'port' )}/graphql` )
		} )
	},
}
