from __future__ import annotations

from .message_base import MessageBase

import attr


@attr.dataclass
class TelemetryPacket(MessageBase):
    """
    Dataclass defining the turret's telemetry packet.
    this MUST match the fields defined in the firmware package [here](https://github.com/SC-Robotics-2021/turret_monitor_firmware/blob/master/src/datamodel/telemetry_packet.rs)
    """

    turret_pos: float
