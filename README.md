# Simple Serial Link Protocol - SiLink

![CI](https://github.com/18r441m/silink/actions/workflows/ci.yml/badge.svg)

This repository implements a simple, low-level wire protocol for
serial links, targeted at micropython runtimes. The protocol covers
both serialization and framing. It's original intended use case is to
transfer IMU and depth sensor data through a UART using rp2040
microcontroller's micropython firmware.


## Design Goals

- Simple, yet convenient API.
- Low computational overhead.
- Transmission error detection.


## Usage example

```python
import silink
from silink.messages import DepthSensor

# Message Encoding.
ds_msg = DepthSensor(
   b'DS', pressure=1.0, temperature=25)
encoded_msg = silink.encode(ds_msg)
print(f"Encoded msg: {encoded_msg}")


# Message decoding in practical setting.
buff = b'noise_or_junk_data'
buff += encoded_msg
buff += b'noise_or_partial_msg'

decoded_msg, rest_of_buff = silink.decode(buff)
print(f"Decoded msg: {decoded_msg}")

# Trim the potentially junk filled buffer upto some
# size so that it does not consume all memory.
buff = rest_of_buff[:-200]
```


## Defining new messages

Messsages are defined in the `silink.messages` module. Each
message is declared as a `namedtuple`, with the first field
being a bytestring of size two - it's typecode.

Each message needs to have an entry in the
`silink.messages.MESSAGE_FORMATS` dictionary. The key is
the typecode of the message. The value is a three field
tuple of format - `(<struct-format>, <class>, <defaults>)`.

- `<struct-format>` is a `str` describing the byte-packing structure of
  the message, as described in `struct` module of micropython standard
  library. Note some datatypes supported by cpython are missing in
  micropython.
- `<class>` is the class of the message.
- `<defaults>` is a tuple containing default field values. This is a
  workaround of micropython's `namedtuple`-s missing default fields.


## Testing

To run the tests, execute -
```bash
tools/run_tests.sh
```

## Limitations

- Creation of new messages require the programmer to know not only
  the class, but also the 2-byte type code. This is an unintended
  side effect of micropython's `namedtuple` not supporting default
  fields.
- Despite the aim at efficiency, current implementation does quite
  a few memory allocations during operation. This could be improved.


## Contributors
- [Titon Barua](https://github.com/titonbarua)
- [Ibrahim Salman](https://github.com/18r441m)


