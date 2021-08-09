import pytest

from turret_python_interface.datamodel.request_packet import RequestPacket


@pytest.fixture
def request_packet_fx() -> RequestPacket:
    return RequestPacket(kind=0)


def test_encode(request_packet_fx):
    """ Verifies a round-trip (en|de)coding cycle for a request packet """
    # Serialize the packet.
    wire_bytes = bytes(request_packet_fx)

    # Assert that the packet's checksum coincides with the ground-truth from the microcontroller.
    assert request_packet_fx.crc32 == 168841071

    # Verify that the packet can be decoded successfully.
    assert RequestPacket.from_bytes(wire_bytes) == request_packet_fx

