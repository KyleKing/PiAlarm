import './App.css'
import React, { Component } from 'react'
import Client from './Client'
import Mutation from './Mutation'
import logo from './logo.svg'

function auth( pass, cb ) {
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

class App extends Component {
	render() {

		// Test GraphQL requests
		auth( 'BadPass', () => '' )
		auth( 'SecretPass',  () => {
			Client.rollDice( 3, 6 )
			Mutation.setMessage( 'DeepThoughts', 'How much wood can a wood chuck...' )
		} )

		return (
			<div className="App">
				<header className="App-header">
					<img src={logo} className="App-logo" alt="logo" />
					<p>
            Edit <code>src/App.js</code> and save to reload.
					</p>
					<a
						className="App-link"
						href="https://reactjs.org"
						target="_blank"
						rel="noopener noreferrer"
					>
            Learn React
					</a>
				</header>
			</div>
		)
	}
}

export default App
