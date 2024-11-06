import unittest
import random

from silink.framing import encode, decode


TEST_MIN_MSG_LENGTH = 0
# NOTE: Don't increase it to more than 250 without fixing COBS bug!
TEST_MAX_MSG_LENGTH = 250
TEST_N_MSGS = 500
TEST_CORRUPTION_RATE = 0.3


class TestFraming(unittest.TestCase):

    def test_simple(self):
        payload = b'deadbeef'
        decoded, rest = decode(encode(payload))
        self.assertEqual(decoded, payload)
        self.assertEqual(rest, b'')

    def test_long_msgs(
            self,
            min_msg_length=TEST_MIN_MSG_LENGTH,
            max_msg_length=TEST_MAX_MSG_LENGTH,
            n_msgs=TEST_N_MSGS):

        # Create some random payloads.
        payloads = [
            bytearray([
                random.randint(0, 255)
                for _ in range(
                        random.randint(min_msg_length, max_msg_length))])
            for _ in range(n_msgs)]

        # Encode the payload using framing protocol.
        encoded = [encode(pl) for pl in payloads]

        # Try to decode the payload.
        for org, em in zip(payloads, encoded):
            self.assertEqual(decode(em)[0], org)

    def test_corruption_resilience(
            self,
            min_msg_length=TEST_MIN_MSG_LENGTH,
            max_msg_length=TEST_MAX_MSG_LENGTH,
            n_msgs=TEST_N_MSGS,
            corruption_rate=TEST_CORRUPTION_RATE):

        # Create some random payloads.
        payloads = [
            bytearray([
                random.randint(0, 255)
                for _ in range(
                        random.randint(min_msg_length, max_msg_length))])
            for _ in range(n_msgs)]

        # Encode the payload using framing protocol.
        encoded = [bytearray(encode(pl)) for pl in payloads]

        # Corrupted msg index.
        corrupted_indices = list(sorted(random.sample(
            range(n_msgs), k=int(corruption_rate * n_msgs))))

        # Corrupt the chosen messages just by 1 byte, randomly.
        for idx in corrupted_indices:
            encoded_msg = encoded[idx]
            corrupted_byte_idx = random.randint(0, len(encoded_msg) - 1)
            org_byte = encoded_msg[corrupted_byte_idx]

            # Create a corruption.
            rand_byte = org_byte
            while not org_byte != rand_byte:
                rand_byte = random.randint(0, 255)

            encoded[idx][corrupted_byte_idx] = rand_byte

        # Create receive buffer with corrupted msgs.
        buff = b''
        for em in encoded:
            buff += em

        # Decode the whole buffer.
        received = []
        while len(buff) > 0:
            msg, buff_rest = decode(buff)
            if msg is not None:
                received.append(msg)

            if buff_rest == buff:
                break
            else:
                buff = buff_rest

        n_missing = 0
        for idx, msg in enumerate(payloads):
            if idx not in corrupted_indices:
                if msg not in received:
                    n_missing += 1
                # self.assertEqual(
                #     msg in received,
                #     True,
                #     f'Uncorrupted msg was not received! Msg: {msg}, Len: {len(msg)}')

        n_fictional = 0
        n_crc_collision = 0
        if len(received) != (len(payloads) - len(corrupted_indices)):
            for msg in received:
                # Check how many fictional msgs were received.
                if msg not in payloads:
                    n_fictional += 1
                    # raise ValueError(f"Fake msg was received! Msg: {msg}")

                # Check how many corrupted msgs were received.
                idx = payloads.index(msg)
                if idx in corrupted_indices:
                    n_crc_collision += 1
                    # raise ValueError(f"Corrupted msg was received due to CRC collision! Msg: {msg}")

        print(
            f"Corruption resiliency analysis; TX: total - {n_msgs},"
            f" corrupted - {len(corrupted_indices)} ;"
            f" RX: total - {len(received)},"
            f" valid missing: {n_missing},"
            f" fictional: {n_fictional},"
            f" crc collision: {n_crc_collision}")
