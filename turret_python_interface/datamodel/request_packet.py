from __future__ import annotations

import attr

from .message_base import MessageBase


@attr.dataclass
class RequestPacket(MessageBase):
    """
    The datamodel for the turret's request type.
    MUST match the definition [here](https://github.com/SC-Robotics-2021/turret_monitor_firmware/blob/master/src/datamodel/request.rs)
    """

    kind: int  # u32 BE
