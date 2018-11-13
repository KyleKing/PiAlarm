// Generate headers
const headers = {
	'Accept': 'application/json',
	'Authorization': `Bearer ${sessionStorage.getItem( 'jwt' )}`,
	'Content-Type': 'application/json',
}

function setMessage( author, content ) {
	var query = `mutation CrtMsg($input: MessageInput) {
    createMessage(input: $input) {
      id
    }
  }`

	fetch( 'http://localhost:3001/graphql', {
		body: JSON.stringify( {
			query,
			variables: {
				input: {
					author,
					content,
				},
			},
		} ),
		headers,
		method: 'POST',
	} )
		.then( r => r.json() )
		.then( data => {
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

			const { id } = data.data.createMessage
			console.log( 'setMessage() > returned:', id )
			return id
		} )
		.then( id => modifyMessage( id, 'PLaGeRizer' ) )
		.catch( err => console.error( err ) )
}

function modifyMessage( id, newAuthor ) {
	var query = `mutation ModMsg($id: ID!, $input: MessageInput) {
    updateMessage(id: $id, input: $input) {
      id
    }
  }`

	fetch( 'http://localhost:3001/graphql', {
		body: JSON.stringify( {
			query,
			variables: {
				id: id,
				input: {
					author: newAuthor,
				},
			},
		} ),
		headers,
		method: 'POST',
	} )
		.then( r => {
			console.log( r )
			return r.json()
		} )
		.then( data => {
			console.log( 'modifyMessage() > returned:', data.data )
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

			const { id } = data.data.updateMessage
			return id
		} )
		.then( id => getMessage( id ) )
		.catch( err => console.error( err ) )
}

function getMessage( id ) {
	// Declare GetMsg query that accepts id variable and returns only author,content fields
	var query = `query GetMsg($id: ID!) {
      getMessage(id: $id) {
				author
	      content
	    }
    }`

	fetch( 'http://localhost:3001/graphql', {
		body: JSON.stringify( {
			query,
			variables: { id },
		} ),
		headers,
		method: 'POST',
	} )
		.then( r => {
			console.log( r )
			return r.json()
		} )
		.then( data => {
			console.log( 'getMessage() > returned:', data.data.getMessage )
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )
		} )
		.catch( err => console.error( err ) )
}

const Mutation = { getMessage, setMessage }
export default Mutation
