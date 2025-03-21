import ntcore
import time
import pyfirmata2
from wpilib import SmartDashboard

print("Hello World")
PORT = pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT, baudrate=115200)
time.sleep(1)
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("DriverStationLEDs")
inst.setServer("10.63.40.2")  # where TEAM=190, 294, etc, or use inst.setServer("hostname") or similar
inst.startDSClient()  # recommended if running on DS computer; this gets the robot IP from the DS
SDTable = inst.getTable("SmartDashboard")
time_until_endgame = SDTable.getDoubleTopic("TimeLeft").subscribe(120)
status = SDTable.getDoubleTopic("State").subscribe(0)
VTable = SDTable.getSubTable("Subsystem")
can_align = VTable.getBooleanTopic("Vision_CAN_ALIGN").subscribe(False)
aligned = VTable.getBooleanTopic("ALIGNED").subscribe(False)
NUM_LEDS = 69

def clear_pixels():
    board.send_sysex(0x70, bytearray([0xFE]))

def set_pixel_color(index, hue):
    board.send_sysex(0x70, bytearray([0x03, index, hue]))

def show_pixels():
    board.send_sysex(0x70, bytearray([0xFF]))

def set_strip_color(hue):
    board.send_sysex(0x70, bytearray([0x04, hue]))

def set_pixel_brightness(index, brightness):
    board.send_sysex(0x70, bytearray([0x05, index, int((brightness / 100) * 255)]))

def set_strip_brightness(brightness):
    board.send_sysex(0x70, bytearray([0x06, int((brightness / 100) * 255)]))

def flashStrip(hue=0, wait_ms=20, flashes=1):
    for i in range(flashes):
        print("Flashing strip #{}".format(i))
        set_strip_color(hue)
        show_pixels()
        time.sleep(wait_ms / 2000.0)
        clear_pixels()
        show_pixels()
        time.sleep(wait_ms / 2000.0)

def rainbowCycle(wait_ms=20, iterations=5):
    """Draw a rainbow that uniformly distributes itself across all pixels using hue values (0-360)."""
    for j in range(255 * iterations):  # Hue range from 0-360 instead of 0-255
        for i in range(NUM_LEDS):
            hue = (int(i * 255 / NUM_LEDS) + j) % 255  # Calculate hue per pixel
            set_pixel_color(i, hue)  # Assuming your library can handle direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)


import time

def hueCycle(wait_ms=10, iterations=1, minHue=0, maxHue=360):
    hueDifference = maxHue - minHue
    for j in range(hueDifference * iterations):  # 80 steps from 160 to 240
        for i in range(NUM_LEDS):
            hue = minHue + ((j + int(i * hueDifference / NUM_LEDS)) % hueDifference)  # Smooth transition between 160 and 240
            set_pixel_color(i, hue)  # Assuming your library supports direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)



def bouncingHue(wait_ms=20, iterations=5, minHue=0, maxHue=360):
    """Cycle hue back and forth between 160 and 240 across all pixels."""
    hue_min, hue_max = minHue, maxHue
    step = 1  # Hue step size
    hue = hue_min  # Start hue
    direction = 1  # 1 for increasing, -1 for decreasing

    for _ in range(255 * iterations):  # Arbitrary large number for continuous effect
        for i in range(NUM_LEDS):
            set_pixel_color(i, hue)  # Assuming the library supports direct hue values
        show_pixels()
        time.sleep(wait_ms / 1000.0)

        # Update hue with bouncing effect
        hue += step * direction
        if hue >= hue_max or hue <= hue_min:
            direction *= -1  # Reverse direction when hitting limits



if __name__ == '__main__':
    warned = False
    prevTime = 0
    prev_can_align = False
    prev_align = False
    prev_state = -1
    while True:
        time.sleep(.01)
        if warned == False & (time_until_endgame.get() <= 30):
            warned = True
            flashStrip(hue=0, wait_ms=100, flashes=5)
            lastSolid = ""

        if(prev_can_align != can_align.get()) | (prev_align != aligned.get()) | (prev_state != status.get()):
            prev_can_align = can_align.get()
            prev_align = aligned.get()
            prev_state = status.get()
            while aligned.get() & ((status.get() == 2) | (status.get() == 1)):
                flashStrip(hue=96, wait_ms=250, flashes=1)

            if can_align.get() & ((status.get() == 2) | (status.get() == 1)):
                set_strip_color(96)
                show_pixels()

            elif status.get() == 2:
                set_strip_color(155)
                show_pixels()

            while status.get() == 1:
                flashStrip(hue=0, wait_ms=500, flashes=1)
                lastSolid = ""

            while status.get() == 0:
                hueCycle(wait_ms=10, iterations=1, minHue=130, maxHue=170)
                lastSolid = ""


