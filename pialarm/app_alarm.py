"""Alarm App."""

import json
from pathlib import Path

import dash_auth
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_charts.utils_app import AppBase
from dash_charts.utils_fig import map_args, map_outputs


class AppAlarm(AppBase):
    """PiAlarm UI."""

    name = 'PiAlarm'
    """Application name"""

    secret_filename = Path(__file__).parent / 'secret.json'
    """Path to json file with username and passwords. Example: `{'username': 'password'}`."""

    external_stylesheets = [dbc.themes.FLATLY]
    """List of external stylesheets."""

    id_button = 'test-button'
    """Button ID."""

    id_status = 'string-status'
    """Status ID."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_button, self.id_status])

        if not self.secret_filename.is_file():
            raise FileNotFoundError(f'Expected: {self.secret_filename}')
        user_pass_pairs = json.loads(self.secret_filename.read_text())
        dash_auth.BasicAuth(self.app, user_pass_pairs)

    def create_elements(self):
        """Initialize charts and tables."""
        pass

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            obj: Dash HTML object. Default is simple HTML text

        """
        return dbc.Container([
            dbc.Col([
                html.H1('PiAlarm'),
                dbc.Button('Test Button', color='secondary', id=self.ids[self.id_button]),
                html.P('', id=self.ids[self.id_status]),
            ]),
        ])

    def create_callbacks(self):
        """Create Dash callbacks."""
        outputs = [(self.id_status, 'children')]
        inputs = [(self.id_button, 'n_clicks')]
        states = []

        @self.callback(outputs, inputs, states)
        def update_table(*raw_args):
            args_in, args_state = map_args(raw_args, inputs, states)
            n_clicks = args_in[self.id_button]['n_clicks']

            return map_outputs(outputs, [
                (self.id_status, 'children', f'Clicked: {n_clicks}'),
            ])
