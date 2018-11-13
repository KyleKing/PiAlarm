const express = require( 'express' )
const graphqlHTTP = require( 'express-graphql' )
const cors = require( 'cors' )
const jwt = require( 'jsonwebtoken' )
const rateLimit = require( 'express-rate-limit' )
const GQL = require( './server/GraphQL.js' )
const bcrypt = require( 'bcryptjs' )

require( 'dotenv' ).config()

var hash = bcrypt.hashSync( process.env.PASSWORD, bcrypt.genSaltSync( 12 ) )

const app = express()
app.set( 'port', ( process.env.PORT || 3001 ) )

// Implement basic rate limiting
app.use( rateLimit( {
	max: 100, // limit each IP to 100 requests per windowMs
	windowMs: 10 * 60 * 1000, // 10 minutes
} ) )

// Create custom logging middle ware
app.use( ( req, res, next ) => {
	console.log( 'ip:', req.ip )
	next()
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
app.use( ( req, res, next ) => {
	// Check if request includes authorization string
	if ( typeof ( req.headers.authorization ) === 'string' ) {
		const argsAuth = req.headers.authorization.split( ' ' )
		if ( argsAuth.length === 2 ) {
			// Check Password
			if ( argsAuth[0] === 'Basic' && bcrypt.compareSync( argsAuth[1], hash ) )
				return next()
			// Check JWT
			if ( argsAuth[0] === 'Bearer' && jwt.verify( argsAuth[1], process.env.JWT_SECRET ) ) {
				console.log( jwt.decode( argsAuth[1], process.env.JWT_SECRET ) )
				return next()
			}
		}
	}
	// Otherwise, send 401 - Unauthorized Status Code
	return res.sendStatus( 401 )
} )

// Configure GraphQL endpoint
app.use( '/graphql', graphqlHTTP( {
	graphiql: true,
	rootValue: GQL.root,
	schema: GQL.schema,
} ) )

app.listen( app.get( 'port' ), () => {
	console.log( `Running GraphQL server at http://localhost:${app.get( 'port' )}/graphql` )
} )
