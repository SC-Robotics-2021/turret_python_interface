from turret_python_interface.datamodel.telemetry_packet import TelemetryPacket


def test_decode():
    raw = b'\r\xa2jturret_pos\x18jturret_rotgForwardgM\x06\x10\x00'
    response = TelemetryPacket.from_bytes(raw)

    # can't compare floats by equality; but we know the value is ~50 since we provided the data.
    assert round(response.turret_pos) == 0
