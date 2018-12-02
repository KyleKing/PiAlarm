export default function auth( pass, cb ) {
	const query = `mutation CreateToken($pass: String!) {
		  createToken(password: $pass)
		}`

	fetch( 'http://localhost:3001/graphql', {
		body: JSON.stringify( {
			query,
			variables: { pass },
		} ),
		headers: {
			'Accept': 'application/json',
			'Authorization': `Basic ${pass}`,
			'Content-Type': 'application/json',
		},
		method: 'POST',
	} )
		.then( r => r.json() )
		.then( data => {
			console.log( 'createToken() > returned:', data.data.createToken )
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

			// Store returned token for use in subsequent requests
			sessionStorage.setItem( 'jwt', data.data.createToken )
		} )
		.then( cb() )
		.catch( err => console.error( err ) )
}
