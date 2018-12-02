// Configure GraphQL

const lgr = require( 'debug' )( 'App:API' )

const jwt = require( 'jsonwebtoken' )
const bcrypt = require( 'bcryptjs' )
const { buildSchema } = require( 'graphql' )
const db = require( './Database.js' )

// Construct a schema, using GraphQL schema language
const schema = buildSchema( `
	input MutateAlarm {
		enabled: Boolean
		schedule: String
		title: String
		uniq: String
	}

	input NewAlarm {
		enabled: Boolean!
		schedule: String!
		title: String!
		uniq: String!
	}

	type Alarm {
		_id: ID!
		enabled: Boolean!
		schedule: String!
		title: String!
		uniq: String!
	}

	type Query {
		getAlarm(id: ID!): Alarm
	}

	type Mutation {
		createAlarm(input: NewAlarm): Alarm
		createToken(password: String!): String
		updateAlarm(id: ID!, input: MutateAlarm): Alarm
	}
` )

// The root provides a resolver function for each API endpoint
const rootValue = {
	createAlarm: async ( { input } ) => await db.prom.insert( db.alarms, input ),
	createToken: function( { password } ) {
		return db.prom.findOne( db.users, {} )
			.then( doc => {
				if ( doc.length === 0 )
					throw new Error( 'No user account found' )

				if ( bcrypt.compareSync( password, doc.hash ) ) {
					const token = jwt.sign( { user: { admin: true } }, process.env.JWT_SECRET, { expiresIn: '15m' } )
					lgr( token )
					return token
				} else
					throw new Error( 'Password error' )
			} )
	},
	getAlarm: function( { id } ) {
		return db.prom.findOne( db.alarms, { _id: id } )
			.then( doc => {
				if ( doc.length === 0 )
					throw new Error( 'no Alarm exists with id ' + id )
				return doc
			} )
	},
	ip: ( args, request ) => request.ip,
	updateAlarm: function( { id, input } ) {
		// returnUpdatedDocs: true > must be set to true to return docs
		// upsert: true > if document is not inserted, upsertedDoc be undefined
		return db.prom.update( db.alarms, { _id: id }, input, { multi: false, returnUpdatedDocs: true, upsert: true } )
			.then( ( { numAffected, affectedDocuments, upsertedDoc } ) => {
				if ( numAffected === 0 )
					throw new Error( 'no Alarm exists with id ' + id )
				return affectedDocuments[0]
			} )
			.catch( err => lgr( err ) )
	},
}

module.exports = {
	config: {
		graphiql: true,
		rootValue,
		schema,
	},
}
