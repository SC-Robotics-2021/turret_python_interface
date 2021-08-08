from __future__ import annotations

from .message_base import MessageBase

"""
Dataclass defining the turret's telemetry packet.
this MUST match the fields defined in the firmware package [here]()
"""
import attr


@attr.dataclass
class TelemetryPacket(MessageBase):
    turret_pos: float
