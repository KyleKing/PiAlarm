"""Main script for launching the alarm."""

from dash_charts.dash_helpers import parse_cli_port
from pialarm.app_alarm import AppAlarm

if __name__ == '__main__':
    port = parse_cli_port()
    app = AppAlarm()
    app.create()
    app.run(port=port, debug=True)
else:
    app = AppAlarm()
    app.create()
    FLASK_HANDLE = app.get_server()
