import React from 'react';
import ReactDOM from 'react-dom';
import Alarm from './Alarm.jsx';
const socket = io();

class AlarmContainer extends React.Component {
  constructor() {
    super();
    this.state = { alarms: [] };
    socket.on('alarm event', (newAlarm) => this.handleStateChange(newAlarm));
  }

  handleStateChange(newAlarm) {
    let isNewAlarm = true;
    const alarms = this.state.alarms.map((alarm) => {
      // If alarm already exists, replace the old one:
      if (alarm.uniq === newAlarm.uniq) {
        isNewAlarm = false;
        return newAlarm;
      }
      return alarm;
    });

    if (isNewAlarm)
      alarms.push(newAlarm);

    // FIXME: Sort alarms by schedule
    // alarms.sort((a, b) => {
    //   // console.log(a.timestamp >= b.timestamp);
    //   // return a.timestamp >= b.timestamp;
    //   return
    // });

    this.setState({ alarms });
  }

  newAlarm() {
    socket.emit('new');
  }

  render() {
    const alarms = this.state.alarms.map((alarm) =>
      (
        <li key={alarm.uniq}>
          <Alarm
            uniq={alarm.uniq}
            title={alarm.title}
            schedule={alarm.schedule}
            running={alarm.running}
          />
        </li>
      )
    );

    return (
      <div className="row">
        <div className="alarm-container col-md-12">
          <h3 className="text-center">Alarms</h3>
          <ul className="alarm-list">
            {alarms}
          </ul>
        </div>
        <button
          type="button"
          className="btn custom-button-formatting btn-info button-oversized"
          onClick={() => this.newAlarm()}
        ><h5>Add New</h5></button>
      </div>
    );
  }
}

ReactDOM.render(<AlarmContainer />, document.getElementById('alarms'));
