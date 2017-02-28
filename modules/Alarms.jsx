import React from 'react';
import ReactDOM from 'react-dom';
import Alarm from './Alarm.jsx';
const socket = io(); // eslint-disable-line

function leadingZero(value) {
  // Source: http://stackoverflow.com/a/3605248/3219667
  return `0${value}`.slice(-2);
}

function single(bit) {
  // Return a number:
  // return Number(bit.split(",")[0].split("-")[0]);
  // Or a string with a leading zero (i.e. 09 and not 9)
  return leadingZero(bit.split(",")[0].split("-")[0]);
}

function parseCron(cron) {
  const data = cron.schedule.split(" ");
  // Take only the first value of the cron descriptor
  const second = single(data[0]);
  const minute = single(data[1]);
  const hour = single(data[2]);
  const dayOfMonth = single(data[3]);
  const month = single(data[4]);
  const day = single(data[5]);
  return {
    id: month + dayOfMonth + day + hour + minute + second,
    value: cron,
  }
}

class AlarmContainer extends React.Component {
  constructor() {
    super();
    this.state = {
      alarms: [],
      userStatus: 'unknown..',
    };
    socket.on("alarm event", (newAlarm) => this.handleStateChange(newAlarm));
    socket.on("IFTTT event", (value) => this.updateIFTTTInfo(value));

    // More efficient bind to onClick event:
    this.newAlarm = this.newAlarm.bind(this);
  }

  updateIFTTTInfo(value) {
    this.setState({ userStatus: value });
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
    alarms.sort((a, b) => parseCron(a).id > parseCron(b).id);
    this.setState({ alarms });
  }

  newAlarm() {
    socket.emit("new");
  }

  render() {
    const whereUser = this.state.userStatus;
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
          <h3 className="text-center">Alarms ({whereUser})</h3>
          <ul className="alarm-list">
            {alarms}
          </ul>
        </div>
        <button
          type="button"
          className="btn custom-button-formatting btn-info button-oversized"
          onClick={this.newAlarm}
        ><h5>Add New</h5></button>
      </div>
    );
  }
}

ReactDOM.render(<AlarmContainer />, document.getElementById("alarms"));
