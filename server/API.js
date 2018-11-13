// Configure GraphQL

const lgr = require( 'debug' )( 'App:API' )

const jwt = require( 'jsonwebtoken' )
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
const doAsync = require( 'doasync' )

// The root provides a resolver function for each API endpoint
const rootValue = {
	// createMessage: async function( { input } ) {
	createMessage: function( { input } ) {
		lgr( input )
		// // // var message = doAsync( db.alarms ).insert( input )
		// var message = doAsync( db.alarms ).insert( input ).then( doc => {
		// 	lgr( `doc: ${doc}` )
		// 	return doc
		// } )

		// // var message = doAsync( db.alarms ).find( {} )
		// // 	.then( docs => {
		// // 		lgr( `docs: ${docs}` )
		// // 		return docs
		// // 	} )
		// // 	.catch( ( err ) => lgr( `Find Error: ${err}` ) )
		// // // var message = await doAsync( db.alarms ).insert( input ).then( doc => doc )

		var message =  db.prom.insert( db.alarms, input )
			.then( doc => {
				lgr( `doc: ${doc}` )
				doc.id = doc._id
				lgr( doc )
				// lgr( doc.author )
				// lgr( doc._id )
				return doc
			} )

		lgr( 'message:' )
		lgr( message )
		return ( message )
	},
	createToken: function( { password } ) {
		// bcrypt.compareSync( password, hash )  // FIXME: Check password, then return
		return jwt.sign( { user: { admin: true } }, process.env.JWT_SECRET, { expiresIn: '10m' } )
	},
	getMessage: async function( { id } ) {
		return await doAsync( db.alarms ).findOne( { _id: id } )
			.then( doc => {
				if ( doc.length === 0 )
					throw new Error( 'no message exists with id ' + id )
				return doc
			} )
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
