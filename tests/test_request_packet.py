from turret_python_interface.request_packet import RequestPacket

def test_encode():
    packet = RequestPacket(kind=4)

    bytes(packet)