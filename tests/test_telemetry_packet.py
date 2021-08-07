from turret_python_interface.telemetry_packet import TelemetryPacket


def test_decode():
    raw = b'\x17{"turret_pos":0.0}\xcb~aY\x00'
    response = TelemetryPacket.from_bytes(raw)

    assert response == TelemetryPacket(turret_pos=0.0)
