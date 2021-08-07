from crc import Configuration, CrcCalculator

crc_ethernet_config = Configuration(
    width=32,
    polynomial=0x4C11DB7,
    init_value=0xFFFF_FFFF,
    reverse_input=False,
    reverse_output=False,
    final_xor_value=0x0000_0000,
)
crc_ethernet = CrcCalculator(crc_ethernet_config)
