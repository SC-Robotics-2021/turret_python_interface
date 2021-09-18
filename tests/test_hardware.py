"""

Hardware validation tests

"""
import pathlib

import pytest

from turret_python_interface import Interface

from loguru import logger

@pytest.mark.hardware
def test_request():
    logger.debug("spawning interface...")
    target = pathlib.Path("/") / "dev" / "ttyUSB0"
    interface = Interface(timeout=1, serial_path=target)
    logger.debug("retrieving telemetry...")
    response = interface.get_telemetry()
