from struct import pack, unpack
from . messages import MESSAGE_FORMATS
try:
    import micropython
except ImportError:
    from . import dummy_micropython as micropython

@micropython.native
def serialize(msg_tuple):
    msg_type = msg_tuple.type
    msg_fmt = MESSAGE_FORMATS[msg_type][0]
    return pack(msg_fmt, *msg_tuple)
@micropython.native
def deserialize(msg_bytes):
    msg_type = bytes(msg_bytes[:2])
    msg_fmt, msg_tuple, _ = MESSAGE_FORMATS[msg_type]
    return msg_tuple(*unpack(msg_fmt, msg_bytes))
