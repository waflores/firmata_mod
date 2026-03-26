"""
This example sets up and control an MPU6050 i2c accelerometer.
It will continuously print data the raw xyz data from the device.
"""

import sys
import time
from telemetrix import telemetrix

# Sensor address
DEVICE_ADDRESS = 0x68

# MPU6050 power management register
PWR_MGMT_1 = 0x6B

# MPU6050 sample rate register
SMPRT_DIV = 0x19

# MPU6050 configuration registers
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACELL_CONFIG = 0x1C

# MPU6050 data registers
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47


# the call back function to print the MPU6050 data
def the_callback(data):
    """

    :param data: [pin_type, Device address, device read register, x data pair, y data pair, z data pair]
    :return:
    """
    print(data)


def mpu6050(my_board):
    # setup mpu6050
    # device address = 0x68
    my_board.set_pin_mode_i2c()

    # Initial configuration for the MPU6050
    # Select the internal oscillator (8MHz) as clock source
    my_board.i2c_write(DEVICE_ADDRESS, [PWR_MGMT_1, 0x00])
    # Configure the sample rate as 1kHz
    my_board.i2c_write(DEVICE_ADDRESS, [SMPRT_DIV, 0x07])
    # Disable DLPF and FSYNC
    my_board.i2c_write(DEVICE_ADDRESS, [CONFIG, 0x06])
    # Set the full-scale range of the gyroscope output as +/- 2000 deg/s
    my_board.i2c_write(DEVICE_ADDRESS, [GYRO_CONFIG, 0x18])
    # Set the full-scale range of the accelerometer output as +/- 16g
    my_board.i2c_write(DEVICE_ADDRESS, [ACELL_CONFIG, 0x18])

    while True:
        # read 6 bytes from the data register
        try:
            print("Accel raw values:")
            my_board.i2c_read(DEVICE_ADDRESS, ACCEL_XOUT_H, 6, the_callback)
            print("Gyro raw values:")
            my_board.i2c_read(DEVICE_ADDRESS, GYRO_XOUT_H, 6, the_callback)
            time.sleep(0.5)

        except (KeyboardInterrupt, RuntimeError):
            my_board.shutdown()
            sys.exit(0)


board = telemetrix.Telemetrix()
try:
    mpu6050(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
