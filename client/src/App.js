import './Globals.css'
import './App.css'
import {
	Link, Redirect, Route, BrowserRouter as Router, Switch,
} from 'react-router-dom'
import React, { Component } from 'react'
import Alarm from './Alarm'
import Client from './Client'
import Login from './Login'
import Mutation from './Mutation'

const Alarms = () => <Alarm
	uniq="{alarm.uniq}"
	title="{alarm.title}"
	schedule="{alarm.schedule}"
	running="{alarm.running}" />  // FYI: will output error to console

const NoMatch = () => <h1><Link to="/">404 - URL Not Found</Link></h1>

function redirect() {
	return <Redirect to="/" />
}

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
	constructor( props ) {
		super( props )
		this.state = { approve: false }
		this.setApprove = this.setApprove.bind( this )
	}

	setApprove( approve ) {
		this.setState( { approve } )
	}

	render() {

		// Test GraphQL requests
		// auth( 'BadPass', () => '' )
		auth( 'SecretPass',  () => {
			Mutation.setMessage( 'DeepThoughts', 'How much wood can a wood chuck...' )
			setTimeout( Client.rollDice, 200, 3, 6 )
		} )

		return (
			<Router>
				<div className="App">
					<Switch>
						<Route path="/" exact render={( props ) => (
							<Login {...props} approveAuth={this.setApprove} />
						)} />
						<Route path="/Alarms/"
							component={this.state.approve ? Alarms : redirect} />
						<Route component={NoMatch} />
					</Switch>
				</div>
			</Router>
		)
	}
}

export default App
