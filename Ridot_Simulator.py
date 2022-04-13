import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from Ui_sim_Ridot import Ui_MainWindow
from enum import IntEnum
import Serial
import threading
import time

class Mode(IntEnum):
    ECO = 100
    RIDE =101
    DASH = 102
    SONIC = 103
    PARK = 104

class KeyState(IntEnum):
    UNLOCKED = 111
    LOCKED = 110

class MotorState(IntEnum):
    ON = 121
    OFF = 120



class Ridot_Simulator(QtWidgets.QMainWindow):

    KeyStatus = KeyState.LOCKED
    MotorStatus = MotorState.OFF
    ModeStatus = Mode.ECO
    autoRideEnabled = False
    autoRideThread = None
    batteryLevel = 0

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.batteryLevel = self.ui.batteryLevel.value()
        self.ui.KeyButon.clicked.connect(self.keyBtnClicked)
        self.ui.motorButton.clicked.connect(self.motorBtnClicked)
        self.ui.ecoBtn.clicked.connect(self.updateRideMode)
        self.ui.rideBtn.clicked.connect(self.updateRideMode)
        self.ui.dashBtn.clicked.connect(self.updateRideMode)
        self.ui.sonicBtn.clicked.connect(self.updateRideMode)
        self.ui.leftBtn.clicked.connect(self.indicationUpdate)
        self.ui.rightBtn.clicked.connect(self.indicationUpdate)
        self.ui.hazardBtn.clicked.connect(self.indicationUpdate)
        self.ui.highBeamBtn.clicked.connect(self.indicationUpdate)
        self.ui.rideButton.clicked.connect(self.autoRideBtnClicked)
        self.ui.batteryLevel.valueChanged.connect(self.updateBatteryLevel)
        self.ui.odoUpdate.clicked.connect(self.updateOdoValue)


    def updateOdoValue(self):
        Serial.sendOdoValue(int(self.ui.odoValue.text()))
    def keyBtnClicked(self):
        Serial.sendKeyStatus(self.ui.KeyButon.isChecked())
        if(not self.ui.KeyButon.isChecked()):
            self.ui.KeyButon.setText("UNLOCK")
            self.KeyStatus = KeyState.LOCKED
        else:
            self.ui.KeyButon.setText("LOCK")
            self.KeyStatus = KeyState.UNLOCKED
        self.ui.keyStatus.setText(self.KeyStatus.name)

    def motorBtnClicked(self):
        if(self.ui.motorButton.isChecked()):
            self.ui.motorButton.setText("STOP")
            Serial.sendKillSwitchInfo(True)
            time.sleep(1)
            Serial.sendMotorStatus(True)
            self.ui.motorStatus.setText("ON")
        else:
            self.ui.motorButton.setText("START")
            Serial.sendKillSwitchInfo(False)
            time.sleep(1)
            Serial.sendMotorStatus(False)
            self.ui.motorStatus.setText("OFF")

    def autoRideBtnClicked(self):
        self.autoRideEnabled = self.ui.rideButton.isChecked()
        self.ui.rideButton.setText("OFF" if self.autoRideEnabled else "ON")
        self.configureAutoRide(self.autoRideEnabled)

    def configureAutoRide(self, enabled):

        if(enabled):
            self.autoRideThread = AutoRideThread(self)
            self.autoRideThread.start()
        # else:
        #     if self.autoRideThread is not None:
        #         self.autoRideThread.join()
        pass

    def updateRideMode(self):
        if(self.ui.ecoBtn.isChecked()):
            self.ModeStatus = Mode.ECO
        elif (self.ui.rideBtn.isChecked()):
            self.ModeStatus = Mode.RIDE
        elif (self.ui.dashBtn.isChecked()):
            self.ModeStatus = Mode.DASH
        elif (self.ui.sonicBtn.isChecked()):
            self.ModeStatus = Mode.SONIC
        else:
            return

        Serial.sendRideModeStatus(self.ModeStatus)
        self.ui.modeStatus.setText(self.ModeStatus.name)


    def indicationUpdate(self):
        if(self.ui.hazardBtn.isChecked()):
            Serial.sendLeftIndicSwitchInfo(True)
            time.sleep(0.2)
            Serial.sendRightIndicSwitchInfo(True)
        else:
            Serial.sendLeftIndicSwitchInfo(self.ui.leftBtn.isChecked())
            time.sleep(0.2)
            Serial.sendRightIndicSwitchInfo(self.ui.rightBtn.isChecked())
        
        time.sleep(0.2)
        Serial.sendHighBeamSwitchInfo(self.ui.highBeamBtn.isChecked())

    def updateSpeedLevel(self, speed):
        self.ui.speedStatus.setText(str(speed))
        Serial.sendSpeedMessage(int(speed))

    def updateBatteryLevel(self):
        self.batteryLevel = self.ui.batteryLevel.value()
        print("SOC: %d"%self.batteryLevel)
        
        Serial.sendBMSStatus(int(self.batteryLevel))

class AutoRideThread(threading.Thread):
    
    speed = 1
    mode = Mode.ECO
    speedStep = 1
    waitCount = 50
    speedIncrement = True # Ture is speed up and False is speed down
    speedLimits = {
        Mode.ECO: {
            "min" : 1,
            "max": 45
        },
        Mode.RIDE: {
            "min" : 45,
            "max": 65
        },
        Mode.DASH: {
            "min": 65,
            "max": 85
        },
        Mode.SONIC: {
            "min": 85,
            "max": 103
        }
    }
    def __init__(self, simulator :Ridot_Simulator):
        super().__init__()
        self.sim = simulator
        pass

    def run(self):
        wCount=0
        lastMode=self.mode
        print("Started Auto ride thread")
        while(self.sim.autoRideEnabled):
            if(self.speed < self.speedLimits[self.mode]["max"] and self.speed >= self.speedLimits[self.mode]["min"]):
                self.speed = (self.speed + self.speedStep) if self.speedIncrement else (self.speed - self.speedStep)
                wCount = 0
            else:
                if(wCount <= self.waitCount):
                    wCount += 1
                else:
                    if self.mode == Mode.ECO:
                        if(self.speedIncrement):
                            self.mode = Mode.RIDE
                        else :
                            self.speedIncrement = not self.speedIncrement
                            self.speed = (self.speed + self.speedStep) if self.speedIncrement else (self.speed - self.speedStep)
                    elif self.mode == Mode.RIDE:
                        self.mode = Mode.DASH if self.speedIncrement else Mode.ECO
                    elif self.mode == Mode.DASH: 
                        self.mode=Mode.SONIC if self.speedIncrement else Mode.RIDE
                    elif self.mode == Mode.SONIC: 
                        if(self.speedIncrement):
                            self.speedIncrement = not self.speedIncrement
                            self.speed = (self.speed + self.speedStep) if self.speedIncrement else (self.speed - self.speedStep)
                        else:
                            self.mode = Mode.DASH

            
            
            if self.mode == Mode.ECO:
                self.sim.ui.ecoBtn.setChecked(True)
            elif self.mode == Mode.RIDE:
                self.sim.ui.rideBtn.setChecked(True)
            elif self.mode == Mode.DASH:
                self.sim.ui.dashBtn.setChecked(True)
            elif self.mode == Mode.SONIC:
                self.sim.ui.sonicBtn.setChecked(True)

            if self.mode != lastMode:
                self.sim.updateRideMode()
                time.sleep(0.1)
                lastMode = self.mode
            self.sim.updateSpeedLevel(self.speed)
            time.sleep(0.1)
            # print("Speed : %s  Mode: %s"%(self.speed, self.mode.name))
            

        while(self.speed > 0):
            self.speed -= 1
            self.sim.updateSpeedLevel(self.speed)
            time.sleep(0.2)
            

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ridot_Simulator()
    win.show()
    sys.exit(app.exec_())
