#!/usr/bin/python3
import pyfirmata2
from pyfirmata2.util import to_two_bytes
from threading import Timer
import time

# https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
# https://components101.com/sites/default/files/component_datasheet/MPU6050-DataSheet.pdf

"""
        msg = [pyfirmata2.START_SYSEX,
               pyfirmata2.REPORT_FIRMWARE,
               2,
               1] + list(str_to_two_byte_iter('Firmware_name')) + \
              [pyfirmata2.END_SYSEX]
        self.board.sp.write(msg)
        self.board.iterate()
        self.assertEqual(self.board.firmware, 'Firmware_name')

"""

# Sensor address
MPU_DEVICE_ADDRESS = 0x68

# MPU6050 power management register
PWR_MGMT_1 = 0x6B

# MPU6050 sample rate register
SMPRT_DIV = 0x19

# MPU6050 configuration registers
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACELL_CONFIG = 0x1C
WHOAMI_COMMAND = 0x75

# MPU6050 data registers
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

I2C_READ_MODE = 0b00001000
I2C_WRITE_MODE = 0x0


class MPUDevice:
    def __init__(self, board, seconds):
        self.board = board
        # pin 13 which is connected to the internal LED
        # self.digital_0 = board.get_pin("d:13:o")

        # flag that we want the timer to restart itself in the callback
        self.timer = None

        # delay
        self.DELAY = seconds

    def report_firmware_version(self):
        self.timer = Timer(self.DELAY, self.report_firmware_version)
        # start the timer
        self.timer.start()

        self.board.send_sysex(
            pyfirmata2.I2C_REQUEST,
            [MPU_DEVICE_ADDRESS, I2C_READ_MODE, *to_two_bytes(WHOAMI_COMMAND), 0, 0, 0],
        )
        time.sleep(0.1)  # Serial SYNC

        serial_msg = bytearray()
        res = self.board.sp.read()
        while res:
            serial_msg += res
            res = self.board.sp.read()
        print(f"{serial_msg}")

    # callback function which toggles the digital port and
    # restarts the timer
    def blinkCallback(self):
        # call itself again so that it runs periodically
        self.timer = Timer(self.DELAY, self.report_firmware_version)

        # start the timer
        self.timer.start()

        # now let's toggle the LED
        v = self.digital_0.read()
        v = not v
        if v:
            print("On")
        else:
            print("Off")
        self.digital_0.write(v)

    # starts the blinking
    def start(self):
        # Kickstarting the perpetual timer by calling the
        # callback function once
        self.report_firmware_version()

    # stops the blinking
    def stop(self):
        # Cancel the timer
        self.timer.cancel()


# main program

# Adjust that the port match your system, see samples below:
# On Linux: /dev/ttyACM0,
# On Windows: COM1, COM2, ...
PORT = pyfirmata2.Arduino.AUTODETECT

# Creates a new board
board = pyfirmata2.Arduino(PORT, debug=True)

t = MPUDevice(board, 1)
t.start()

print("To stop the program press return.")
# Just blocking here to do nothing.
input()

t.stop()

# close the serial connection
board.exit()
