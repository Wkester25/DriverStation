import gpiozero
import ntcore
import time
import pyfirmata2


def printData(data):
    print(data)


PORT = pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT)
board.samplingOn(10000)
pin = board.get_pin("d:11:p")
#board.send_sysex(0x70, bytearray([0x0D, 0x12, 0x52]))
inst = ntcore.NetworkTableInstance.getDefault()
table = inst.getTable("DriverStation")
num = table.getDoubleTopic("number").subscribe(0)
inst.startClient4("example client")
inst.setServer("192.168.1.107") # where TEAM=190, 294, etc, or use inst.setServer("hostname") or similar
inst.startDSClient() # recommended if running on DS computer; this gets the robot IP from the DS
while True:
    time.sleep(5)
    print(num.get()/100             )
    #board.send_sysex(0x70, bytearray([0x01, (int(num.get())), 0xFF, 0xFF, 0xFF]))
    pin.write(num.get()/100)

