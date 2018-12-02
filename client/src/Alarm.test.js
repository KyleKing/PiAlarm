import Alarm from './Alarm'
import React from 'react'
import ReactDOM from 'react-dom'

// FIXME: Placeholder
it( 'renders without crashing', () => {
	const div = document.createElement( 'div' )
	ReactDOM.render( <Alarm
		uniq="UNIQUE"
		title="ALARM TITLE"
		schedule="SCHEDULE"
		enabled={true} />, div )
	ReactDOM.unmountComponentAtNode( div )
} )
