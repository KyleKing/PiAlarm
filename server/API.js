// Configure GraphQL

// const lgr = require( 'debug' )( 'App:API' )

const jwt = require( 'jsonwebtoken' )
const { buildSchema } = require( 'graphql' )

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

// FYI: Temporary database for testing
var fakeDatabase = {}

// The root provides a resolver function for each API endpoint
const rootValue = {
	createMessage: function( { input } ) {
		// Create a random id for our "database".
		const id = require( 'crypto' ).randomBytes( 10 ).toString( 'hex' )

		fakeDatabase[id] = input
		return new Message( id, input )
	},
	createToken: function( { password } ) {
		// bcrypt.compareSync( password, hash )  // FIXME: Check password, then return
		// 	FYI: Will need to do run in async: https://graphql.org/learn/execution/
		return jwt.sign( { user: { admin: true } }, process.env.JWT_SECRET, { expiresIn: '10m' } )
	},
	getMessage: function( { id } ) {
		if ( !fakeDatabase[id] )
			throw new Error( 'no message exists with id ' + id )

		return new Message( id, fakeDatabase[id] )
	},
	ip: function( args, request ) {
		return request.ip
	},
	rollDice: function( { numDice, numSides } ) {
		const output = []
		for ( let i = 0; i < numDice; i++ )
			output.push( 1 + Math.floor( Math.random() * ( numSides || 6 ) ) )

		return output
	},
	updateMessage: function( { id, input } ) {
		if ( !fakeDatabase[id] )
			throw new Error( 'no message exists with id ' + id )

		// Partially update the database entry rather than the entire object
		// 	src: https://stackoverflow.com/a/48209957/3219667
		Object.assign( fakeDatabase[id], input )

		return new Message( id, input )
	},
}


module.exports = {
	config: {
		graphiql: true,
		rootValue,
		schema,
	},
}
