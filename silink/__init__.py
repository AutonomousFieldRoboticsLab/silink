from .framing import encode as encode_frame
from .framing import decode as decode_frame
from .serialization import *


# RP2040 has a 32bit hardware UART buffer. If a msg is smaller than 32bits,
# it might not be received immediately.
BUFF_ALIGNMENT = 32
PADDING = bytes([0 for _ in range(BUFF_ALIGNMENT)])


def encode(msg_tuple):
    """Encode a message using silink protocol.

    Args:
        msg_tuple: A named tuple as described in `serialization` module.

    Returns:
       A `bytes` object.
    """
    data_bytes = encode_frame(serialize(msg_tuple))
    len_padding = len(data_bytes) % BUFF_ALIGNMENT
    if len_padding > 0:
        return data_bytes + PADDING[:len_padding]
    else:
        return data_bytes


def decode(buff):
    """Decode a buffer and return the first message, if available.

    Args:
        buff: A `bytes` or `bytearray` object.

    Returns:
        A tuple of format `(decoded-msg, rest-of-buffer)`. `decoded-msg` is
        a named tuple as described in `serialization` module. It is `None`
        if no message is currently available in buffer.
    """
    frame, rest_of_buff = decode_frame(buff)
    if frame is None:
        return None, rest_of_buff
    else:
        return deserialize(frame), rest_of_buff
