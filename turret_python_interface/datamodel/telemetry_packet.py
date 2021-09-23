from __future__ import annotations

from enum import Enum

import attr

from .message_base import MessageBase


class TurretDirection(Enum):
    Forward = "Forward"
    Backward = "Backward"


@attr.dataclass
class TelemetryPacket(MessageBase):
    """
    Dataclass defining the turret's telemetry packet.
    this MUST match the fields defined in the firmware package [here](https://github.com/SC-Robotics-2021/turret_monitor_firmware/blob/master/src/datamodel/telemetry_packet.rs)
    """

    turret_pos: float
    turret_rot: TurretDirection
