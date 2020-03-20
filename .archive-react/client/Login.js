import './styles/Login.css'
import React, { Component } from 'react'
import Auth from './Auth'

class Login extends Component {
	// Login input text

	constructor( props ) {
		super( props )
		// this.state = { hidePass: false, loadState: false, password: '' }  # FIXME: Remove password
		this.state = { hidePass: false, loadState: false, password: 'SecretPass' }
		// Bind handlers
		this.showHide = this.showHide.bind( this )
		this.handleChange = this.handleChange.bind( this )
		this.handleSubmit = this.handleSubmit.bind( this )
	}

	showHide( e ) {
		e.preventDefault()
		e.stopPropagation()
		// Toggle showing/hiding the password input
		this.setState( { hidePass: !this.state.hidePass } )
	}

	handleChange( e ) {
		// Parse the password while typed
		this.setState( { password: e.target.value } )
	}

	handleSubmit( e ) {
		e.preventDefault()
		// Hide password and disable form input while loading
		this.setState( { hidePass: true, loadState: true } )
		// Check password in Authorization promise
		Auth( 'SecretPass' )
			.then( ( token ) => {
				if ( token.length === 157 ) {
					this.props.approveAuth( true )
					this.props.history.push( '/Alarms' )
				}
			} ).catch( ( err ) => {
				this.setState( { loadState: false } )
				console.warn( `Password Denied: ${this.state.password}`, err )
				alert( err )
			} )
	}

	render() {
		// <Link to="/">Home</Link>
		const toggleLbl = this.state.hidePass ? 'Hide' : 'Show'
		return (
			<div className="center-up">
				<h1>PiAlarm</h1>
				<form onSubmit={this.handleSubmit}>
					<div className="pass-container">
						<input
							className={`password ${toggleLbl} dark`}
							type={this.state.hidePass ? 'password' : 'text'}
							onChange={this.handleChange}
							placeholder="Password"
							value={this.state.password}
							required={true}
							disabled={this.state.loadState}
						/>
						<div className="pass-container-buttons">
							<button
								className="password-toggle"
								onClick={this.showHide}
								type="button"
							>{toggleLbl}</button>
							<button
								type="submit"
								className="login"
								disabled={this.state.loadState}
							>Login</button>
						</div>
					</div>
				</form>
			</div>
		)
	}
}

export default Login
