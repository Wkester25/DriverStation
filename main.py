import ntcore
import time
import pyfirmata2
from wpilib import Color

PORT = pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT, baudrate=115200)
time.sleep(1)
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("DriverStationLEDs")
inst.setServer("192.168.1.107")  # where TEAM=190, 294, etc, or use inst.setServer("hostname") or similar
inst.startDSClient()  # recommended if running on DS computer; this gets the robot IP from the DS
table = inst.getTable("SmartDashboard")
status = table.getDoubleTopic("STATE").subscribe(0)
table2 = table.getSubTable("Subsystem")
canAllign = table2.getBooleanTopic("Vision_CAN_ALIGN").subscribe(False)
alligned = table2.getBooleanTopic("ALIGNED").subscribe(False)
timeLeft = table.getDoubleTopic("TimeLeft").subscribe(0)

def clear_pixels():
    board.send_sysex(0x70, bytearray([0xFE]))

def set_pixel_color(index, hue):
    board.send_sysex(0x70, bytearray([0x03, index, hue]))

def set_strip_color(hue):
    board.send_sysex(0x70, bytearray([0x04, hue]))

def show_pixels():
    board.send_sysex(0x70, bytearray([0xFF]))

def rainbowCycle(wait_ms=20, iterations=5):
    for j in range(255 * iterations):  # Hue range from 0-360 instead of 0-255
        for i in range(36):
            hue = (int(i * 255 / 36) + j) % 255  # Calculate hue per pixel
            set_pixel_color(i, hue)  # Assuming your library can handle direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)

def hueCycle(wait_ms=10, iterations=1, hue_max=130, hue_min=170):
    hueDiff = hue_max - hue_min
    for j in range(hueDiff * iterations):  # 80 steps from 160 to 240
        for i in range(36):
            hue = hue_min + ((j + int(i * hueDiff / 36)) % hueDiff)  # Smooth transition between 160 and 240
            set_pixel_color(i, hue)  # Assuming your library supports direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)

def bouncingHue(wait_ms=20, iterations=5, hue_min=130, hue_max=170):
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


while True:
    if alligned.get():
        set_strip_color(255)
        show_pixels()
        clear_pixels()
        time.sleep(0.5)
    elif canAllign.get():
        
