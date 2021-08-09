from __future__ import annotations

import attr

from .message_base import MessageBase


@attr.dataclass
class RequestPacket(MessageBase):
    """a request object"""

    kind: int  # u32 BE
