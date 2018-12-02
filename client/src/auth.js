export default function auth( pass ) {
	// FIXME: Use client secret to encrypt plain text password

	return fetch( 'http://localhost:3001/graphql', {
		body: JSON.stringify( {
			query: `mutation CreateToken($pass: String!) {
			  createToken(password: $pass)
			}`,
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
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

			// Store returned token for use in subsequent requests
			const token = data.data.createToken
			console.log( `createToken() > returned: ${token}` )
			sessionStorage.setItem( 'jwt', token )
			return token
		} )
}
