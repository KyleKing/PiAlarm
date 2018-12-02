// Generate headers
const fetchURL = 'http://localhost:3001/graphql'
const headers = {
	'Accept': 'application/json',
	'Authorization': `Bearer ${sessionStorage.getItem( 'jwt' )}`,
	'Content-Type': 'application/json',
}

const typeAlarm = `{
	_id
	enabled
	schedule
	title
	uniq
}`

// function getAlarms() {
// 	// Declare GetAlarm query that accepts id variable and returns only author,content fields
// 	return fetch( fetchURL, {
// 		body: JSON.stringify( {
// 			query: `query GetAlarms() {
// 	      getAlarms() [Alarm]
// 	    }`,
// 		} ),
// 		headers,
// 		method: 'POST',
// 	} )
// 		.then( r => r.json() )
// 		.then( data => {
// 			if ( data.errors )
// 				data.errors.map( err => console.log( err.message, err ) )

// 			console.log( 'getAlarms() > returned:', data.data.getAlarms )
// 			return data.data.getAlarms
// 		} )
// 		// .catch( err => console.error( err ) )
// }

function getAlarm( id ) {
	// Declare GetAlarm query that accepts id variable and returns only author,content fields
	return fetch( fetchURL, {
		body: JSON.stringify( {
			query: `query GetAlarm($id: ID!) {
	      getAlarm(id: $id) ${typeAlarm}
	    }`,
			variables: {
				id,
			},
		} ),
		headers,
		method: 'POST',
	} )
		.then( r => r.json() )
		.then( data => {
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

			console.log( 'getAlarm() > returned:', data.data.getAlarm )
			return data.data.getAlarm
		} )
		// .catch( err => console.error( err ) )
}

function modifyAlarm( id, input ) {
	return fetch( fetchURL, {
		body: JSON.stringify( {
			query: `mutation ModAlarm($id: ID!, $input: MutateAlarm) {
		    updateAlarm(id: $id, input: $input) ${typeAlarm}
		  }`,
			variables: {
				id: id,
				input,
			},
		} ),
		headers,
		method: 'POST',
	} )
		.then( r => r.json() )
		.then( data => {
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

			console.log( 'modifyAlarm() > returned:', data.data )
			return data.data.updateAlarm._id
		} )
		.then( idUpdate => getAlarm( idUpdate ) )
		// .catch( err => console.error( err ) )
}

function makeAlarm( input ) {
	return fetch( fetchURL, {
		body: JSON.stringify( {
			query: `mutation CreateAlarm($input: NewAlarm) {
		    createAlarm(input: $input) ${typeAlarm}
		  }`,
			variables: {
				input,
			},
		} ),
		headers,
		method: 'POST',
	} )
		.then( r => r.json() )
		.then( data => {
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

			const id = data.data.createAlarm._id
			console.log( 'makeAlarm() > returned:', id )
			return id
		} )
		// .catch( err => console.error( err ) )
}

// export default { getAlarm, getAlarms, makeAlarm, modifyAlarm }
export default { getAlarm, makeAlarm, modifyAlarm }
