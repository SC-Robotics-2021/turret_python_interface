from __future__ import annotations

from io import BytesIO

import attr
import cattr
import six
from cbor2 import dumps, loads
from cobs import cobs
from loguru import logger

from .crc_definition import crc_ethernet


@attr.dataclass
class RequestPacket:
    """a request object"""

    kind: int  # u32 BE

    def __bytes__(self):
        buf = BytesIO()
        # serialize this instance and ensure its in a binary form.
        # six is used to ensure its binary; such that the encoding `dumps` func can be replaced
        # seamlessly. (Json returns a string, cbor2 returns bytes.)
        payload = six.ensure_binary(dumps(cattr.unstructure(self)))
        buf.write(payload)

        payload_crc = crc_ethernet.calculate_checksum(payload[: len(payload) // 4 * 4])
        buf.write(payload_crc.to_bytes(4, "big", signed=False))

        # seek to the start of the BytesIO buffer
        buf.seek(0)
        # return the formed buffer object.
        return cobs.encode(buf.read())

    @classmethod
    def from_bytes(cls, raw: bytes) -> RequestPacket:
        packet = cobs.decode(raw[0: raw.find(b"\x00")])
        data, device_crc = packet[:-4], int.from_bytes(packet[-4:], "big")
        logger.debug(f"data bytes := {data!r}, device CRC := {device_crc}")
        if (
                crc := crc_ethernet.calculate_checksum(data[: len(data) // 4 * 4])
        ) != device_crc:
            raise ValueError(
                f"host checksum {crc} does not match device checksum {device_crc}. Abort."
            )
        return cattr.structure(loads(data), RequestPacket)
