try:
    import micropython
except ImportError:
    from . import dummy_micropython as micropython


@micropython.native
def encode(data):
    read_pointer = 0
    write_pointer = 1
    code_pointer = 0
    code = 1

    output = bytearray(len(data) + len(data) // 254 + 2)

    data_length = len(data)
    while read_pointer < data_length:
        byte = data[read_pointer]
        read_pointer += 1
        if byte == 0:
            output[code_pointer] = code
            code_pointer = write_pointer
            write_pointer += 1
            code = 1
        else:
            output[write_pointer] = byte
            write_pointer += 1
            code += 1
            if code == 0xFF:
                output[code_pointer] = code
                code_pointer = write_pointer
                write_pointer += 1
                code = 1

    output[code_pointer] = code
    return output[:write_pointer]


@micropython.native
def decode(data):
    read_pointer = 0
    write_pointer = 0

    data_length = len(data)
    output = bytearray(data_length)

    while read_pointer < data_length:
        code = data[read_pointer]
        read_pointer += 1

        if code == 0:
            return None

        end = read_pointer + code - 1
        while read_pointer < end and read_pointer < data_length:
            output[write_pointer] = data[read_pointer]
            write_pointer += 1
            read_pointer += 1

        if code < 0xFF and read_pointer < data_length:
            output[write_pointer] = 0
            write_pointer += 1

    return output[:write_pointer]