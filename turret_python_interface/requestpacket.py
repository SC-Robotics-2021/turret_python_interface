import cattr
import attr
from cobs import cobs
import json

from .crc_definition import crc_ethernet

from enum import Flag

from io import BytesIO


@attr.dataclass
class RequestPacket:
    """a request object"""

    kind: int  # u32 BE

    def __bytes__(self):
        buf = BytesIO()
        payload = json.dumps(cattr.unstructure(self)).encode()
        buf.write(payload)

        payload_crc = crc_ethernet.calculate_checksum(payload[: len(payload) // 4 * 4])
        buf.write(payload_crc.to_bytes(4, "big", signed=False))

        # seek to the start of the BytesIO buffer
        buf.seek(0)
        # return the formed buffer object.
        return cobs.encode(buf.read())
