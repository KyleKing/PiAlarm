import './styles/Alarms.css'
import Alarm from './Alarm'
import Mutation from './Mutation'
import React from 'react'

export default class Alarms extends React.Component {
	constructor( props ) {
		super( props )
		this.state = {
			alarms: [],
		}
	}

	componentDidMount() {
		// Request all Alarms to populate UI
		Mutation.getAlarms().then( ( alarms ) => {
			this.setState( {
				alarms,
			} )
		} )
	}

	render() {
		const mappedAlarms = this.state.alarms.map( ( alarm ) => {
			return (
				<Alarm
					uniq={alarm.uniq}
					title={alarm.title}
					schedule={alarm.schedule}
					enabled={alarm.enabled} />
			)
		} )

		return (
			<div>
				{mappedAlarms}
			</div>
		)
	}
}
