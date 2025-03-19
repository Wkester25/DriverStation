import ntcore
import time
import pyfirmata2
from wpilib import Color

PORT = pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT, baudrate=115200)
time.sleep(1)
inst = ntcore.NetworkTableInstance.getDefault()
table = inst.getTable("DriverStation")
inst.startClient4("example client")
inst.setServer("192.168.1.107")  # where TEAM=190, 294, etc, or use inst.setServer("hostname") or similar
inst.startDSClient()  # recommended if running on DS computer; this gets the robot IP from the DS


def clear_pixels():
    board.send_sysex(0x70, bytearray([0xFE]))


def set_pixel_color(index, hue):
    board.send_sysex(0x70, bytearray([0x03, index, hue]))


def show_pixels():
    board.send_sysex(0x70, bytearray([0xFF]))



def rainbowCycle(wait_ms=20, iterations=5):
    """Draw a rainbow that uniformly distributes itself across all pixels using hue values (0-360)."""
    for j in range(255 * iterations):  # Hue range from 0-360 instead of 0-255
        for i in range(36):
            hue = (int(i * 255 / 36) + j) % 255  # Calculate hue per pixel
            set_pixel_color(i, hue)  # Assuming your library can handle direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)


import time

def hueCycle(wait_ms=10, iterations=1):
    for j in range(40 * iterations):  # 80 steps from 160 to 240
        for i in range(36):
            hue = 130 + ((j + int(i * 40 / 36)) % 40)  # Smooth transition between 160 and 240
            set_pixel_color(i, hue)  # Assuming your library supports direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)



def bouncingHue(wait_ms=20, iterations=5):
    """Cycle hue back and forth between 160 and 240 across all pixels."""
    hue_min, hue_max = 130, 170
    step = 1  # Hue step size
    hue = hue_min  # Start hue
    direction = 1  # 1 for increasing, -1 for decreasing

    for _ in range(255 * iterations):  # Arbitrary large number for continuous effect
        for i in range(36):
            set_pixel_color(i, hue)  # Assuming the library supports direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)

        # Update hue with bouncing effect
        hue += step * direction
        if hue >= hue_max or hue <= hue_min:
            direction *= -1  # Reverse direction when hitting limits


bouncingHue(wait_ms=50, iterations=5)