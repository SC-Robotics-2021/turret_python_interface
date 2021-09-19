from __future__ import annotations

from pathlib import Path
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Optional, Type
from serial import Serial
from loguru import logger

from .datamodel.telemetry_packet import TelemetryPacket
from .datamodel.request_packet import RequestPacket, RequestKind


class Interface(AbstractContextManager):
    """Provides a context manager abstraction around the turret-monitor-firmware device."""

    def __init__(
        self,
        serial_path: Path = Path("/") / "dev" / "ttyS0",
        baud: int = 115200,
        timeout=30,
    ):
        """
        Constructs an instance of this interface. This is a **CONTEXT MANAGER**

        Examples:
            >>> from turret_python_interface.interface import Interface
            >>> with Interface() as iface:
            ...     print(iface.get_telemetry())
            TelemetryPacket(turret_pos=0.0)

        Args:
            serial_path: filesystem path to the serial port
            baud: baud rate to communicate with the device
            timeout: serial read timeout, in seconds(?)
        """
        self.path = serial_path
        self.baud = baud
        self.con: Optional[Serial] = None
        self.timeout = timeout  # presumably in seconds?

        self.open_serial()

    def __enter__(self) -> Interface:
        self.open_serial()
        logger.trace("opened serial port.")
        return self

    def open_serial(self):
        path = str(self.path.absolute())
        logger.debug(f"opening serial port {path!r} with baud {self.baud}...")
        self.con = Serial(
            str(self.path.absolute()), baudrate=self.baud, timeout=self.timeout
        )

    def __exit__(
        self,
        __exc_type: Optional[Type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.close()
        return super().__exit__(__exc_type, __exc_value, __traceback)

    def get_telemetry(self) -> TelemetryPacket:
        """Requests telemetry from the device, returns the resulting packet."""
        request = RequestPacket(kind=RequestKind.TELEMETRY)
        payload = bytes(request) + b'\x00'
        logger.debug(f"sending request {request!r} [{payload!r}]...")

        # flush the input buffer,to ensure we don't have unread bytes from previous requests
        # Note: the buffer can't simply be purged after reading the response, as the extra
        #       bytes may not have yet arrived. By the time we get here they should have, hopefully.
        self.con.reset_input_buffer()

        self.con.write(payload)
        logger.debug("awaiting response...")
        response_bytes = self.con.read_until(b"\x00")
        if response_bytes == b"":
            raise EOFError("device didn't return any data, is it connected?")
        logger.debug(f"received device response := {response_bytes!r}")
        response = TelemetryPacket.from_bytes(response_bytes + b"\x00")
        logger.debug(f"received response {response!r}")
        return response

    def close(self):
        if self.con:
            logger.trace("closing serial port...")
            self.con.close()
            logger.trace("serial port closed.")
