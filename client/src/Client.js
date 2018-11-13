function rollDice( dice, sides ) {
	var query = `query RollDice($dice: Int!, $sides: Int) {
		  rollDice(numDice: $dice, numSides: $sides)
		}`

	fetch( 'http://localhost:3001/graphql', {
		body: JSON.stringify( {
			query,
			variables: { dice, sides },
		} ),
		headers: {
			'Accept': 'application/json',
			'Authorization': `Bearer ${sessionStorage.getItem( 'jwt' )}`,
			'Content-Type': 'application/json',
		},
		method: 'POST',
	} )
		.then( r => {
			console.log( r )
			return r.json()
		} )
		.then( data => {
			console.log( 'rollDice() > returned:', data.data.rollDice )
			if ( data.errors )
				data.errors.map( err => console.log( err.message, err ) )

		} )
		.catch( err => console.error( err ) )
}

const Client = { rollDice }
export default Client
