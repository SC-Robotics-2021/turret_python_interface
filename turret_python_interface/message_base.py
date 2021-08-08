from __future__ import annotations

from abc import ABC

import attr
import cattr
from _cbor2 import loads, dumps
from cobs import cobs
from loguru import logger

from .crc_definition import crc_ethernet

from typing import TypeVar, Type

T = TypeVar("T")

@attr.dataclass
class MessageBase:
    @classmethod
    def from_bytes(cls: Type[T], raw: bytes) -> T:
        packet = cobs.decode(raw[0: raw.find(b"\x00")])
        data, device_crc = packet[:-4], int.from_bytes(packet[-4:], "big")
        logger.debug(f"data bytes := {data!r}, device CRC := {device_crc}")
        if (
                crc := crc_ethernet.calculate_checksum(data[: len(data) // 4 * 4])
        ) != device_crc:
            raise ValueError(
                f"host checksum {crc} does not match device checksum {device_crc}. Abort."
            )
        return cattr.structure(loads(data), cls)

    @property
    def crc32(self):
        """computes the CRC32-Ethernet as defined by the device."""
        payload = dumps(cattr.unstructure(self))
        payload = payload[: len(payload) // 4 * 4]

        return crc_ethernet.calculate_checksum(payload)


