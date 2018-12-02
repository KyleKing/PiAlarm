import './styles/Alarms.css'
import Alarm from './Alarm'
// import Mutation from './Mutation'
import React from 'react'

export default class Alarms extends React.Component {
	// // TODO: Enable getAlarms()
	// constructor( props ) {
	// 	super( props )
	// 	this.state = {
	// 		alarms: async () => await Mutation.getAlarms(),
	// 	}
	// }

	render() {
		// // TODO: Enable getAlarms()
		// return this.state.alarms.map( ( alarm ) => {
		// 	return (
		// 		<Alarm
		// 			uniq={alarm.uniq}
		// 			title={alarm.title}
		// 			schedule={alarm.schedule}
		// 			enabled={alarm.enabled} />
		// 	)
		// } )

		return (
			<Alarm
				uniq="{alarm.uniq}"
				title="{alarm.title}"
				schedule="{alarm.schedule}"
				enabled={true} />
		)
	}
}
