// Configure GraphQL

const lgr = require( 'debug' )( 'App:API' )

const jwt = require( 'jsonwebtoken' )
const bcrypt = require( 'bcryptjs' )
const { buildSchema } = require( 'graphql' )
const db = require( './Database.js' )

// Construct a schema, using GraphQL schema language
const schema = buildSchema( `
	input MessageInput {
		content: String
		author: String
	}

	type Message {
		id: ID!
		content: String
		author: String
	}

	type Query {
		getMessage(id: ID!): Message
		rollDice(numDice: Int!, numSides: Int): [Int]
	}

	type Mutation {
		createMessage(input: MessageInput): Message
		updateMessage(id: ID!, input: MessageInput): Message
		createToken(password: String!): String
	}
` )

// If Message had any complex fields, we'd put them on this object.
class Message {
	constructor( id, { content, author } ) {
		this.id = id
		this.content = content
		this.author = author
	}
}

// The root provides a resolver function for each API endpoint
const rootValue = {
	// createMessage: async function( { input } ) {
	createMessage: function( { input } ) {
		return db.prom.insert( db.alarms, input )
			.then( doc => new Message( doc._id, doc ) )
	},
	createToken: function( { password } ) {
		return db.prom.findOne( db.users, {} )
			.then( doc => {
				if ( doc.length === 0 )
					throw new Error( 'No user account found' )

				if ( bcrypt.compareSync( password, doc.hash ) )
					return jwt.sign( { user: { admin: true } }, process.env.JWT_SECRET, { expiresIn: '10m' } )
				else
					throw new Error( 'Password error' )
			} )
	},
	getMessage: async function( { id } ) {
		return db.prom.findOne( db.alarms, { _id: id } )
			.then( doc => {
				if ( doc.length === 0 )
					throw new Error( 'no message exists with id ' + id )
				return new Message( doc._id, doc )
			} )
	},
	ip: function( args, request ) {
		return request.ip
	},
	rollDice: function( { numDice, numSides } ) {
		return ( [...Array( numDice ).keys()].map( () => Math.floor( Math.random() * ( numSides || 6 ) ) ) )
	},
	updateMessage: function( { id, input } ) {
		return db.prom.update( db.alarms, { _id: id }, input, { multi: true, returnUpdatedDocs: true, upsert: true } )
			.then( ( { numAffected, affectedDocuments, upsert } ) => {
				if ( numAffected === 0 )
					throw new Error( 'no message exists with id ' + id )

				// returnUpdatedDocs: true > must be set to true to return docs
				// multi: true > returns list of documents
				// upsert: true > if document is inserted, upsert will be the doc. Otherwise undefined
				const doc = affectedDocuments[0]
				return new Message( doc._id, doc )
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
