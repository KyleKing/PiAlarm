"""Final test alphabetically (zz) to catch general integration cases."""

import time

import pytest
import toml
from pialarm import __version__
from pialarm.app_alarm import AppAlarm


@pytest.mark.CHROME
def test_smoke_test_main(dash_duo):
    app = AppAlarm()
    app.create()
    dash_duo.start_server(app.app)

    time.sleep(1)

    assert not dash_duo.get_logs()


def test_version():
    """Check that PyProject and __version__ are equivalent."""
    assert toml.load('pyproject.toml')['tool']['poetry']['version'] == __version__
