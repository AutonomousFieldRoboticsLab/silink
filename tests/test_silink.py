import unittest
from random import randint, random

import silink
from silink.serialization import (
    serialize, deserialize)
from silink.messages import (
    Imu, DepthSensor,
    Thrusters, ArmThrusters, ArmThrustersAck, Peripherals,
    ClockSyncInit, ClockSyncReq, ClockSyncResp, ClockSyncFinish,
    HealthStatus)


def randreal():
    return random() * 1e6 * (1.0 if random() < 0.5 else -1.0)

def randbool():
    return (True if random() < 0.5 else False)


class SerializationTest(unittest.TestCase):
    IMU_MSG = Imu(
        type=b'IM',
        epoch_ns=randint(0, 2 << 64 - 1),
        a_x=randreal(),
        a_y=randreal(),
        a_z=randreal(),
        g_x=randreal(),
        g_y=randreal(),
        g_z=randreal(),
        m_x=randreal(),
        m_y=randreal(),
        m_z=randreal())

    DEPTH_SENSOR_MSG = DepthSensor(
        type=b'DS',
        epoch_ns=randint(0, 2 << 64 - 1),
        pressure=randreal(),
        temperature=randreal())

    THRUSTERS_MSG = Thrusters(
        type=b'TH',
        t1=randreal(),
        t2=randreal(),
        t3=randreal(),
        t4=randreal(),
        t5=randreal(),
        t6=randreal(),
        t7=randreal(),
        t8=randreal())

    ARM_THRUSTERS_MSG = ArmThrusters(
        type=b'AR',
        t1=randbool(),
        t2=randbool(),
        t3=randbool(),
        t4=randbool(),
        t5=randbool(),
        t6=randbool(),
        t7=randbool(),
        t8=randbool())

    ARM_THRUSTERS_ACK_MSG = ArmThrustersAck(
        type=b'AK',
        t1=randbool(),
        t2=randbool(),
        t3=randbool(),
        t4=randbool(),
        t5=randbool(),
        t6=randbool(),
        t7=randbool(),
        t8=randbool())

    PERIPHERALS_MSG = Peripherals(
        type=b'PH',
        light=randreal(),
        led1=randbool(),
        led2=randbool(),
        led3=randbool())

    CLOCK_SYNC_INIT_MSG = ClockSyncInit(
        type=b'CI')

    CLOCK_SYNC_REQ_MSG = ClockSyncReq(
        type=b'CS',
        epoch_ns=randint(0, 2 << 64 - 1))

    CLOCK_SYNC_RESP_MSG = ClockSyncResp(
        type=b'CR',
        req_epoch_ns=randint(0, 2 << 64 - 1),
        resp_epoch_ns=randint(0, 2 << 64 - 1))

    CLOCK_SYNC_FINISH_MSG = ClockSyncFinish(
        type=b'CF',
        success=1)

    HEALTH_STATUS_MSG = HealthStatus(
        type=b'HS',
        epoch_ns=randint(0, 2 << 64 - 1),
        bat_v=15.4,
        temp_c=25.9)


    def test_serialization(self):
        print("Testing serialization ...")
        for msg in (
                self.IMU_MSG,
                self.DEPTH_SENSOR_MSG,
                self.THRUSTERS_MSG,
                self.ARM_THRUSTERS_MSG,
                self.CLOCK_SYNC_REQ_MSG,
                self.CLOCK_SYNC_RESP_MSG,
                self.CLOCK_SYNC_FINISH_MSG,
                self.HEALTH_STATUS_MSG,
        ):
            msg_type = msg.__class__.__name__
            packed = serialize(msg)
            unpacked = deserialize(packed)
            print(f"Msg type: {msg_type}\n Packed ({len(packed)}): {packed}\n Unpacked: {unpacked}\n")
            self.assertEqual(unpacked, msg)


    def test_silink_1(self):
        print("Testing silink ...")
        for msg in (
                self.IMU_MSG,
                self.DEPTH_SENSOR_MSG,
                self.THRUSTERS_MSG,
                self.ARM_THRUSTERS_MSG,
                self.ARM_THRUSTERS_ACK_MSG,
                self.CLOCK_SYNC_INIT_MSG,
                self.CLOCK_SYNC_REQ_MSG,
                self.CLOCK_SYNC_RESP_MSG,
                self.CLOCK_SYNC_FINISH_MSG,
                self.HEALTH_STATUS_MSG,
        ):
            msg_type = msg.__class__.__name__
            packed = silink.encode(msg)
            unpacked, rest_of_buff = silink.decode(packed)
            print(f"Msg type: {msg_type}\n Packed ({len(packed)}): {packed}\n Unpacked: {unpacked}\n")
            self.assertEqual(unpacked, msg)
            self.assertEqual(rest_of_buff, bytes([0 for _ in range(len(rest_of_buff))]))

    def test_silink_2(self):
        print("Testing silink with empty buffer ...")
        unpacked, rest_of_buff = silink.decode(b'')
        self.assertEqual(unpacked, None)
        self.assertEqual(len(rest_of_buff), 0)

    def test_silink_3(self):
        print("Testing silink with garbage in buffer ...")
        buff = b'asjkhdkjah0qweriouwoieuioweuriouw'
        unpacked, rest_of_buff = silink.decode(buff)
        self.assertEqual(unpacked, None)
        self.assertEqual(len(rest_of_buff), len(buff))
