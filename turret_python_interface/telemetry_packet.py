from __future__ import annotations

"""
Dataclass defining the turret's telemetry packet.
this MUST match the fields defined in the firmware package [here]()
"""
import attr
import cattr
import json
from .crc_definition import crc_ethernet

from cobs import cobs
from loguru import logger


@attr.dataclass
class TelemetryPacket:
    turret_pos: float

    @property
    def crc32(self):
        """computes the CRC32-Ethernet as defined by the device."""
        payload = json.dumps(cattr.unstructure(self))
        payload = payload[: len(payload) // 4 * 4]

        return crc_ethernet.calculate_checksum(payload)

    @classmethod
    def from_bytes(cls, raw: bytes) -> TelemetryPacket:
        packet = cobs.decode(raw[0 : raw.find(b"\x00")])
        data, device_crc = packet[:-4], int.from_bytes(packet[-4:], "big")
        logger.debug(f"data bytes := {data!r}, device CRC := {device_crc}")
        if (
            crc := crc_ethernet.calculate_checksum(data[: len(data) // 4 * 4])
        ) != device_crc:
            raise ValueError(
                f"host checksum {crc} does not match device checksum {device_crc}. Abort."
            )
        return cattr.structure(json.loads(data), TelemetryPacket)
