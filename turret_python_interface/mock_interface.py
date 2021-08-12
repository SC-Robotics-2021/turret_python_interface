"""
Provides a mock Interface class for testing purposes, to decouple tests from requiring
the entire turret hardware stack.
"""

from math import tau
from pathlib import Path
from types import TracebackType
from typing import Optional, Type

from .interface import Interface
from .telemetry_packet import TelemetryPacket


class MockInterface(Interface):
    # noinspection PyMissingConstructor
    def __init__(self, **kwargs):
        # note: we intentionally don't call the constructor of the superclass as it would
        #       init a serial connection; which is an implementation detail
        #       and we cannot mock it effectively.
        self.t = 0
        ...

    @property
    def state(self) -> float:
        # basically, we are reproducing a sine wave.
        # Every time the state is observed, time progresses.
        self.t += pi/4
        return sin((self.t - pi/4) / tau)

    def __enter__(self) -> Interface:
        ...

    def __exit__(self, __exc_type: Optional[Type[BaseException]], __exc_value: Optional[BaseException],
                 __traceback: Optional[TracebackType]) -> Optional[bool]:
        ...

    def get_telemetry(self) -> TelemetryPacket:
        return TelemetryPacket(turret_pos=self.state)
