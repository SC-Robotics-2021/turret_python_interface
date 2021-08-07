from __future__ import annotations

from pathlib import Path
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Optional, Type
from serial import Serial
from loguru import logger

from .telemetry_packet import TelemetryPacket
from .requestpacket import RequestPacket


class Interface(AbstractContextManager):
    def __init__(self, serial_path: Path = Path("/") / "dev" / "ttyS0", baud: int = 115200):
        self.path = serial_path
        self.baud = baud
        self.con: Optional[Serial] = None

    def __enter__(self) -> Interface:
        path = str(self.path.absolute())
        logger.debug(f"opening serial port {path!r} with baud {self.baud}...")
        self.con = Serial(str(self.path.absolute()), baudrate=self.baud)
        logger.trace("opened serial port.")
        return self

    def __exit__(self, __exc_type: Optional[Type[BaseException]], __exc_value: Optional[BaseException],
                 __traceback: Optional[TracebackType]) -> Optional[bool]:
        if self.con:
            logger.trace("closing serial port...")
            self.con.close()
            logger.trace("serial port closed.")

        return super().__exit__(__exc_type, __exc_value, __traceback)

    def get_telemetry(self) -> TelemetryPacket:
        request = RequestPacket(kind=0)
        logger.debug("sending request {!r}...", request)
        self.con.write(bytes(request))
        logger.debug("awaiting response...")
        response_bytes = self.con.read_until(b"\x00")
        logger.debug(f"received device response := {response_bytes!r}")
        response = TelemetryPacket.from_bytes(response_bytes + b"\x00")
        logger.debug(f"received response {response!r}")
        return response
