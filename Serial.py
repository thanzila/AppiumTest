from tkinter.constants import FALSE
import serial
import serial.threaded
import time
import subprocess
from Ridot_Simulator import Mode
from enum import Enum
# # db = cantools.database.load_file('Example.dbc')
# # message = db.get_message_by_name('EEC1')
# # print (message.encode({'EngineSpeed':621.0},True,True,False))
# print (db.decode_message('EEC1',db.encode_message('EEC1', {'EngineSpeed': 621.0})))
#ser=serial.Serial()
#ser.baudrate = 460800
#ser.port = 'COM4'
#ser.baudrate = 115200
#ser.port = '/dev/ttyUSB2'
#ser.open()
## Example DBC and can message
EEC1CanId = bytearray([0x0C,0xF0,0x04,0xFE])
EEC1values = bytearray([0x00,0x00,0x00,0x68,0x13,0x00,0x00,0x00]) ## speed 621 rpm

## SimpleEnergy's Message data sizes
VCU_DataSize = bytearray([0x01])
BMS_StatusDataSize = bytearray([0x02])
KEY_InfoDataSize = bytearray([0x01])
IGNITIONCOMMANDDataSize = bytearray([0x01])
SwitchInfoDataSize = bytearray([0x03])
RideModeCommandDataSize = bytearray([0x01])
MOTORCONTROLLER_STATUSDataSize = bytearray([0x08])
ODO_Value_SIZE = bytearray([0x04])

## SimpleEnergy Can Id's
VCU_StateCanId = bytearray([0x0C,0x01,0xFF,0x22])
BMS_StatusCanId = bytearray([0x0C,0x1D,0xFF,0xF2])
KEY_INFOCanId = bytearray([0x04,0xF1,0x33,0x33])
IGNITION_COMMANDCanId = bytearray([0x08,0x17,0x11,0x33])
SWITCH_INFOCanId = bytearray([0x0C,0x17,0xE6,0xF4])
RIDE_COMMANDCanId = bytearray([0x0C,0x16,0x11,0xFE])
MOTORCONTROLLER_STATUSCanId = bytearray([0x0C,0x01,0xFF,0xF3])
ODOCONTROL_CANId = bytearray([0x0C, 0x19, 0xE6, 0xF4])

# Message output format control
isDataIncluded = True
isSLCanSupport = True

def sendOdoValue(odo: int):
    write(ODOCONTROL_CANId, ODO_Value_SIZE, odo.to_bytes(4, 'little'))
    
# <Message id="0x4F13333" name="KEY_INFO" length="1" format="extended">
def sendKeyStatus(status):
    # <Signal name="KEY_IN" offset="1">
    # <Notes>User turned on the key</Notes>
    if status:
        KEY_INFOdata = bytearray([0x02])
    else:
        KEY_INFOdata = bytearray([0x00])
    write(KEY_INFOCanId,KEY_InfoDataSize,KEY_INFOdata)
    return  
# def sendKeyOnStatus(status):
#     # <Signal name="KEY_OFF" offset="0">
#     # <Notes>When key is closed - 1When key is open - 0</Notes>
#     if status:
#         KEY_INFOdata = bytearray([0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
#     else:
#         KEY_INFOdata = bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
#     ser.write(KEY_INFOCanId+KEY_INFOdata)
#     return


#  <Message id="0xC152233" name="SWITCH_INFO" length="2" format="extended">

highBeamStatus = False
killSwitchStatus = False
brakeLeftStatus = False
brakeRightStatus = False
indicatorLeftStatus = False
indicatorRightStatus = False
navTopStatus = False
navBotStatus = False
navLeftStatus = False
navRightStatus = False
navCentreStatus = False
ignitionSwitchStatus =False

# def sendBrakeStatus(status):
#     # <Signal name="BRAKE" offset="0">
#     # <Notes>Status if brake is pressed or not</Notes>
#     global brakeStatus
#     brakeStatus = status
#     sendSwitchMessage()

def sendHighBeamSwitchInfo(status):
    # <Signal name="HIGHBEAM_Switch" offset="1">
    #     <Notes>Status if Highbeam is on or off</Notes>
    global highBeamStatus 
    highBeamStatus = status
    sendSwitchMessage()
    return  

def sendKillSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global killSwitchStatus
    killSwitchStatus = status
    sendSwitchMessage()


def sendLeftIndicSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global indicatorLeftStatus
    indicatorLeftStatus = status
    sendSwitchMessage()

def sendRightIndicSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global indicatorRightStatus
    indicatorRightStatus = status
    sendSwitchMessage()

def sendNavTopSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global navTopStatus
    navTopStatus = status
    sendSwitchMessage()

def sendNavBotSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global navBotStatus
    navBotStatus = status
    sendSwitchMessage()

def sendNavLeftSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global navLeftStatus
    navLeftStatus = status
    sendSwitchMessage()

def sendNavRightSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global navRightStatus
    navRightStatus = status
    sendSwitchMessage()

def sendNavMidSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global navCentreStatus
    navCentreStatus = status
    sendSwitchMessage()

def sendIgnitionSwitchInfo(status):
# <Signal name="KILL_SWITCH" offset="2">
#  <Notes>when kill switch is 1 MOTOR CONTROLLER ON when kill switch is 0 MOTOR CONTROLLER OFF</Notes>
    global ignitionSwitchStatus
    ignitionSwitchStatus = status
    sendSwitchMessage()
    
    

def sendSwitchMessage():
    # This first byte comprises of Indicator, NAV,HighBeam,Brake value
    #switchDataFirstByte = bytes([killSwitchStatus<<0 | highBeamStatus<<1 | indicatorLeftStatus <<2 | indicatorRightStatus<<3|ignitionSwitchStatus<<4 | navBotStatus<<5 | navCentreStatus <<7 | navRightStatus<<7])
    switchDataFirstByte = bytes([0x00])
    switchDataSecondByte = bytes([highBeamStatus << 0 | indicatorLeftStatus << 1 | indicatorRightStatus << 2 | killSwitchStatus << 5])
    switchDataThirdByte = bytes([ignitionSwitchStatus<<0])
    # print (brakeStatus<<0 | highBeamStatus<<1 | killSwitchStatus <<2 | indicatorPosition<<3)
    switchDataRemainingBytes = bytearray([0x00,0x00,0x00,0x00,0x00])
    write(SWITCH_INFOCanId,SwitchInfoDataSize,switchDataFirstByte+switchDataSecondByte+switchDataThirdByte)



# End of SWITCH_INFO Messages


 ##<Message id="0xCF23311" name="MOTORCONTROLLER_STATUS" length="5" format="extended">
speedValue = 0
rideMode : Mode = Mode.ECO
motorOnStatus = False
def sendMotorStatus(status):
    # <Signal name="STARTSTOP_Status" offset="0">
    # <Notes>Shows if motor is in start or stop condition</Notes>
    global motorOnStatus 
    global speedValue
    motorOnStatus= status
    if motorOnStatus == False:
        speedValue = 0
    sendMotorControllerStatusMessage()


def sendSpeedMessage(values):
    # <Signal length="16" name="SPEED" offset="24">
    # <Notes>Speed of Motor in RPM</Notes>
    global speedValue
    speedValue = values
    # if (rideMode == Mode.ECO) & (values >45) :
    #     speedValue = 45
    # if (rideMode == Mode.RIDE) & (values >65) :
    #     speedValue = 65
    # if (rideMode == Mode.DASH) & (values >85) :
    #     speedValue = 85
    # if (rideMode == Mode.SONIC) & (values >103) :
    #     speedValue = 103
    # if motorOnStatus == False:
    #     speedValue = 0
    sendMotorControllerStatusMessage()
    return    

def sendRideModeStatus(mode):
    # <Signal length="4" name="RIDEMODE_Status" offset="4">
    #     <Notes>Shows the status of current ride mode0000 0001 - ECO Mode0010 - SPORT Mode0011 - RIDE Mode0100 - Park Reverse</Notes>
    global rideMode 
    global speedValue
    rideMode= mode
    if (rideMode == Mode.ECO) and (speedValue >45) :
        speedValue = 45
    if (rideMode == Mode.RIDE) and (speedValue >65) :
        speedValue = 65
    if (rideMode == Mode.DASH) and (speedValue >85) :
        speedValue = 85
    if (rideMode == Mode.SONIC) and (speedValue >103) :
        speedValue = 103
    sendMotorControllerStatusMessage()

def sendMotorControllerStatusMessage():
    global rideMode
    if motorOnStatus:
        if rideMode == Mode.ECO:
            rideModedata = bytearray([0x11,0x00,0x00])
        if rideMode == Mode.RIDE:
            rideModedata = bytearray([0x31,0x00,0x00])
        if rideMode == Mode.DASH:
            rideModedata = bytearray([0x21,0x00,0x00])
        if rideMode == Mode.SONIC:
            rideModedata = bytearray([0x01,0x00,0x00])
        if rideMode == Mode.PARK:
            rideModedata = bytearray([0x41,0x00,0x00])
    else:
        if rideMode == Mode.ECO:
            rideModedata = bytearray([0x10,0x00,0x00])
        if rideMode == Mode.RIDE:
            rideModedata = bytearray([0x30,0x00,0x00])
        if rideMode == Mode.DASH:
            rideModedata = bytearray([0x20,0x00,0x00])
        if rideMode == Mode.SONIC:
            rideModedata = bytearray([0x00,0x00,0x00])
        if rideMode == Mode.PARK:
            rideModedata = bytearray([0x40,0x00,0x00])
    print("Sending Motor Controller message")
    byteAroundSpeed = bytearray([0x00,0x00,0x00])

    rideModeByte = 1
    if rideMode == Mode.ECO:
        rideModeByte = 1
    if rideMode == Mode.RIDE:
        rideModeByte = 3
    if rideMode == Mode.DASH:
        rideModeByte = 2
    if rideMode == Mode.SONIC:
        rideModeByte = 0
    if rideMode == Mode.PARK:
        rideModeByte = 4

    global speedValue
    if speedValue > 0xff:
        speedValue = 0xff
    if speedValue < 0:
        speedValue = 0

    motorOnStatusBit = 0
    if motorOnStatus:
        motorOnStatusBit = 0x01
    speedValueBytes = speedValue.to_bytes(1,"little")
    d = bytearray([0x00, 0x00, 0x00, motorOnStatusBit, rideModeByte, speedValueBytes[0], 0x00, 0x00])
    write(MOTORCONTROLLER_STATUSCanId, MOTORCONTROLLER_STATUSDataSize, d)
    #write(MOTORCONTROLLER_STATUSCanId,MOTORCONTROLLER_STATUSDataSize,rideModedata+speedValueBytes)

# End of MotorControllerStatus messages

# <Message id="0xC00FF44" name="BMS_Status" length="2" format="extended">
def sendBMSStatus(soc):
    # <Signal length="8" name="SOC" offset="0">
    # <Notes>SOC </Notes>
    socValuesByte = soc.to_bytes(1,"little")
    bmsStateByte = bytearray([0x00])
    write(BMS_StatusCanId,BMS_StatusDataSize,socValuesByte+bmsStateByte)


def write(canId,dataLength,data):

    
    if isSLCanSupport:
        #ser.write(bytes("T{}{}{}\r".format((canId).hex().upper(), dataLength.hex()[1], (data).hex().upper()), "ascii"))
        print(bytes("T{}{}{}\r".format((canId).hex().upper(), dataLength.hex()[1], (data).hex().upper()), "ascii"))
        command = "adb shell cansend slcan0 {}#{}".format((canId).hex().upper(), (data).hex().upper())
        print(command)
        subprocess.run(command)
    else:
        pass
        #if isDataIncluded:
        #    ser.write(canId+dataLength+data)
        #else:
        #    ser.write(canId+data)


