from turret_python_interface.telemetry_packet import TelemetryPacket


def test_decode():
    raw = b"\x16\xa1jturret_pos\xfaBG\xfdqV\x14\xd0\x9d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    response = TelemetryPacket.from_bytes(raw)

    # can't compare floats by equality; but we know the value is ~50 since we provided the data.
    assert round(response.turret_pos) == 50
