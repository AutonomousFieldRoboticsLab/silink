from . import cobs
from .crc import crc8

try:
    import micropython
    from micropython import const
except ImportError:
    from . import dummy_micropython as micropython
    from .dummy_micropython import const


_N_LENGTH_BYTES = const(2)
_N_CRC_BYTES = const(1)
_MAX_PAYLOAD_LENGTH = const(65536)
_COBS_FRAME_SEPARATOR = const(0x00)

_cobs_frame_separator_bytes = _COBS_FRAME_SEPARATOR.to_bytes(1, 'big')


@micropython.native
def encode(payload):
    payload = bytes(payload)
    length = len(payload)
    if length > _MAX_PAYLOAD_LENGTH:
        raise ValueError("Payload is too big!")

    length_bytes = length.to_bytes(
        _N_LENGTH_BYTES, 'big')

    length_payload = length_bytes + payload
    crc = crc8(length_payload)

    return (
        # Frame end marker.
        _cobs_frame_separator_bytes +

        # Encode data and the CRC byte with COBS.
        cobs.encode(
            length_payload +
            crc.to_bytes(_N_CRC_BYTES, 'big')) +

        # Frame start marker.
        _cobs_frame_separator_bytes)


@micropython.native
def decode(buff):
    # Grab the potential msg by looking at frame seperator.
    start_marker = buff.find(_cobs_frame_separator_bytes)
    if start_marker == -1:
        return None, buff

    # Skip any padding.
    i = start_marker + 1
    while i < len(buff) and buff[i] == _COBS_FRAME_SEPARATOR:
        i += 1
    start_marker = i - 1

    end_marker = buff.find(_cobs_frame_separator_bytes, i + 1)
    if end_marker == -1:
        return None, buff

    buff_msg = buff[start_marker + 1:end_marker]
    if len(buff_msg) < _N_LENGTH_BYTES + _N_CRC_BYTES:
        return None, buff[end_marker:]

    length_payload_crc = cobs.decode(buff_msg)
    length_payload, expected_crc = (
        length_payload_crc[:-_N_CRC_BYTES],
        int.from_bytes(length_payload_crc[-_N_CRC_BYTES:], 'big'))
    payload, expected_length = (
        length_payload[_N_LENGTH_BYTES:],
        int.from_bytes(length_payload[:_N_LENGTH_BYTES], 'big'))

    if expected_length != len(payload):
        # print("Expected length was different!")
        return None, buff[end_marker:]

    # Throw away the msg if CRC check fails.
    crc = crc8(length_payload)
    if crc != expected_crc:
        # print(f"CRC checksum failed. Expected: {expected_crc}, Actual: {crc}")
        return None, buff[end_marker:]

    return payload, buff[end_marker + 1:]
