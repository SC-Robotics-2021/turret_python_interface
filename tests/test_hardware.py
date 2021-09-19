"""

Hardware validation tests

"""
import pathlib

import pytest

from turret_python_interface import Interface

from loguru import logger

@pytest.mark.hardware
def test_request():
    """ Verifies that a valid telemetry response is received from the actual hardware. """
    logger.debug("spawning interface...")
    target = pathlib.Path("/") / "dev" / "ttyUSB0"
    interface = Interface(timeout=1, serial_path=target)
    logger.debug("retrieving telemetry...")
    # fetch telemetry
    interface.get_telemetry()
    # if we got this far, we received a valid response from the firmware.
    # therefore, the test passes. (no asserts required for this.)
