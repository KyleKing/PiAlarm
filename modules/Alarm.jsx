import React from 'react';
const socket = io();

class Alarm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      uniq: this.props.uniq,
      title: this.props.title,
      schedule: this.props.schedule,
      running: this.props.running,
      removed: false,
      changed: false,
      error: false,
    };
    // Until I setup es2016...
    // https://github.com/goatslacker/alt/issues/283#issuecomment-122650637
    this.handleTitleChange = this.handleTitleChange.bind(this);
    this.handleScheduleChange = this.handleScheduleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  toggleButton() {
    // console.log(`Toggled: ${this.props.uniq}, but no direct action!`);
    this.setState({
      running: !this.state.running,
      changed: true,
    });
  }

  handleTitleChange(event) {
    this.setState({
      title: event.target.value,
      changed: true,
    });
  }

  // Quick CRON guide
  // second         0-59
  // minute         0-59
  // hour           0-23
  // day of month   0-31
  // month          0-12
  // day of week    0-6 (Sun-Sat)

  handleScheduleChange(event) {
    const newSched = event.target.value.trim();
    if (/^((\S+\s+){5}\S+)$/.test(newSched))
      // console.log(event.target.value);
      this.setState({
        schedule: newSched,
        changed: true,
        error: false,
      });
    else {
      this.setState({
        error: true,
      });
      console.warn(`[IC!]: Improper Cron formatting of ${newSched}`);
    }
  }

  handleSubmit(e) {
    // e.preventDefault();
    const newState = {
      uniq: this.state.uniq,
      title: this.state.title,
      schedule: this.state.schedule,
      running: this.state.running,
      removed: false,
      changed: false,
      error: false,
    };
    this.setState(newState);
    socket.emit('update', newState);
    console.log(`Submitted: ${this.props.uniq} with:`);
    console.log(newState);
  }

  removeAlarm() {
    const newState = {
      uniq: this.state.uniq,
      title: 'DELETED',
      removed: true,
      changed: true,
    };
    this.setState(newState);
    socket.emit('remove', this.props.uniq);
    console.log(`Clicked to remove: ${this.props.uniq}, which was:`);
    console.log(newState);
  }

  render() {
    const fc = 'flex-container'
    const fi = 'flex-item'
    const buttonBase = 'btn custom-button-formatting';
    const buttonValue = this.state.running ? 'Enabled' : 'Disabled';
    const buttonState = this.state.running ? 'info' : 'danger';
    const buttonClasses = `${buttonBase} btn-${buttonState} ${buttonValue}`;
    const removed = this.state.removed ? 'removed' : 'alarm-exists';
    const changed = this.state.changed ? 'changed' : 'unchanged';

    // <form className={`${fi} ${fc}`} style={{ display: 'inline' }} onSubmit={this.handleSubmit}>

    return (
      <div className={`alarm ${removed} ${fc}`}>
        <button
          type="button"
          className={`${fi} ${buttonClasses}`}
          onClick={() => this.toggleButton()}
        >{buttonValue}</button>

        <input
          type="text"
          className={`${fi} input-title`}
          defaultValue={this.state.title}
          onChange={this.handleTitleChange}
        />
        <input
          type="text"
          className={`${fi} input-schedule ${(this.state.error) ? 'input-error' : ''}`}
          defaultValue={this.state.schedule}
          onChange={this.handleScheduleChange}
        />
        <button
          className={`${fi} ${buttonBase} ${changed}`}
          onClick={() => this.handleSubmit()}
          type="submit"
        >Save</button>

        <button
          type="button"
          className={`${fi} ${buttonBase} btn-danger remove`}
          id={this.props.uniq}
          onClick={() => this.removeAlarm()}
        >REMOVE</button>
      </div>
    );
  }
}

Alarm.propTypes = {
  uniq: React.PropTypes.string.isRequired,
  title: React.PropTypes.string.isRequired,
  schedule: React.PropTypes.string.isRequired,
  running: React.PropTypes.bool.isRequired,
};

export default Alarm;