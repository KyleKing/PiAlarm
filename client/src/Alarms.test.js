import Alarms from './Alarms'
import React from 'react'
import ReactDOM from 'react-dom'

// FIXME: Placeholder
it( 'renders without crashing', () => {
	const div = document.createElement( 'div' )
	ReactDOM.render( <Alarms />, div )
	ReactDOM.unmountComponentAtNode( div )
} )
