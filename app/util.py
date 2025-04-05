

def int_to_uint16(i: int) -> bytes:
    """
    Convert an integer to a 16-bit unsigned integer in little-endian byte order.
    """
    return int(i).to_bytes(2, byteorder='little', signed=False)

def int_to_uint8(i: int) -> bytes:
    """
    Convert an integer to an 8-bit unsigned integer in little-endian byte order.
    """
    return int(i).to_bytes(1, byteorder='little', signed=False)

def float_to_uint16(f: float) -> bytes:
    """
    Convert a float to a 16-bit unsigned integer in little-endian byte order.
    """
    value = int(f * 65535)
    return int_to_uint16(value)
