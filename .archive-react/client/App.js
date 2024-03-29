import './styles/Globals.css'
import './styles/App.css'
import {
	Link, Redirect, Route, BrowserRouter as Router, Switch,
} from 'react-router-dom'
import React, { Component } from 'react'
import Alarms from './Alarms'
import Login from './Login'

const NoMatch = () => <h1><Link to="/">404 - URL Not Found</Link></h1>

function redirect() {
	return <Redirect to="/" />
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
