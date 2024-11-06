import unittest
import random

from silink.cobs import encode, decode


class TestCOBS(unittest.TestCase):

    def _test_cobs(self, data_length, n_zeros):
        # Create a random input data devoid of value ZERO(0x00).
        input_data = bytearray([
            random.randint(1, 255) for _ in range(data_length)])

        # Enter controlled number of zeroes in the data.
        zero_indices = set()
        for _ in range(n_zeros):
            while True:
                idx = random.randint(0, data_length - 1)
                if idx not in zero_indices:
                    break

            input_data[idx] = 0x00
            zero_indices.add(idx)

        # Do COBS encoding.
        encoded_data = encode(input_data)

        # Check if zero remains in the encoded data.
        n_zeros_after = encoded_data.count(0x00)
        self.assertEqual(n_zeros_after, 0, 'Encoded data must not contain zero')

        # Check data validity.
        decoded_data = decode(encoded_data)
        self.assertEqual(input_data, decoded_data, 'Decoded data is not same as input data')


    def test_cobs(self):
        for l in range(16):
            data_length = 1 << l
            for n_zeros in range(min(8, data_length) + 1):
                print(f"Testing COBS on {data_length} byte random buffer with {n_zeros} zeros in random positions ...")
                self._test_cobs(data_length, n_zeros)

