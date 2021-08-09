from __future__ import annotations

from enum import Enum

import attr

from .message_base import MessageBase


class RequestKind(Enum):
    DEFAULT = 0
    TELEMETRY = 1


@attr.dataclass
class RequestPacket(MessageBase):
    """
    The datamodel for the turret's request type.
    MUST match the definition [here](https://github.com/SC-Robotics-2021/turret_monitor_firmware/blob/master/src/datamodel/request.rs)
    """

    kind: RequestKind = attr.ib(
        validator=attr.validators.instance_of(RequestKind), converter=RequestKind
    )  # u32 BE
