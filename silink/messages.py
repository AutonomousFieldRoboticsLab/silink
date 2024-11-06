from collections import namedtuple


Imu = namedtuple(
    'IM',
    ['type', 'epoch_ns', 'a_x', 'a_y', 'a_z', 'g_x', 'g_y', 'g_z', 'm_x', 'm_y', 'm_z'])

DepthSensor = namedtuple(
    'DS',
    ['type', 'epoch_ns', 'pressure', 'temperature'])

Thrusters = namedtuple(
    'TH',
    ['type', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8'])

ArmThrusters = namedtuple(
    'AR',
    ['type', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8'])

ArmThrustersAck = namedtuple(
    'AK',
    ['type', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8'])

Peripherals = namedtuple(
    'PE',
    ['type', 'light', 'led1', 'led2', 'led3'])

ClockSyncInit = namedtuple(
    'CI',
    ['type'])

ClockSyncReq = namedtuple(
    'CS',
    ['type', 'epoch_ns'])

ClockSyncResp = namedtuple(
    'CR',
    ['type', 'req_epoch_ns', 'resp_epoch_ns'])

ClockSyncFinish = namedtuple(
    'CF',
    ['type', 'success'])

HealthStatus = namedtuple(
    'HS',
    ['type', 'epoch_ns', 'bat_v', 'temp_c'])


MESSAGE_FORMATS = {
    # <type-key> : (<format-spec>, <tuple-class>, <tuple-defaults>)
    b'IM': ("!2sQ9d", Imu, (b'IM', 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    b'DS': ("!2sQ2d", DepthSensor, (b'DS', 0, 0.0, 0.0)),

    # Actuators.
    b'TH': ("!2s8d", Thrusters, (b'TH', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    b'AR': ("!2s8b", ArmThrusters, (b'AR', 0, 0, 0, 0, 0, 0, 0, 0)),
    b'AK': ("!2s8b", ArmThrustersAck, (b'AK', 0, 0, 0, 0, 0, 0, 0, 0)),
    b'PE': ("!2sd3b", Peripherals, (b'PE', 0.0, 0, 0, 0)),

    # Clock syncing.
    b'CI': ("!2s", ClockSyncInit, (b'CI', 0)),
    b'CS': ("!2sQ", ClockSyncReq, (b'CS', 0)),
    b'CR': ("!2s2Q", ClockSyncResp, (b'CR', 0, 0)),
    b'CF': ("!2sb", ClockSyncFinish, (b'CF', 0)),

    b'HS': ("!2sQ2d", HealthStatus, (b'HS', 0, 0.0, 0.0)),
}
