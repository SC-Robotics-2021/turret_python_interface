from turret_python_interface.request_packet import RequestPacket


def test_encode():
    # with current encoding, the length is at least two words

    request_packet = RequestPacket(kind=0)
    wire_bytes = bytes(request_packet)
    assert len(wire_bytes) >= 8

    assert request_packet.crc32 == 168841071

    packet = bytes(RequestPacket(kind=4))

    assert RequestPacket.from_bytes(packet) == RequestPacket(4)
