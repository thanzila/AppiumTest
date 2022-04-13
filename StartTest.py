# import subprocess
#
# from tkinter.constants import FALSE
# import serial
# import serial.threaded
# import time
import subprocess
# #from Ridot_Simulator import Mode
# from enum import Enum
# import sys
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QWidget
# #from Ui_sim_Ridot import Ui_MainWindow
# from enum import IntEnum
# import Serial
# import threading
# import time
from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {
    #"appium:app": "C:/Users/6114402/Downloads/SE_DashboarUI/simpleenergyservice/build/outputs/apk/debug/simpleenergyservice-debug.apk",
    #"appium:app": "C:/MyStoredData/Android/SE_DashboarUI/app/build/outputs/apk/debug/app-debug.apk",
    "appPackage": "com.anvationlabs.se_dashboardui",
    "appActivity": "com.anvationlabs.se_dashboardui.SplashScreen",
    "automationName": "UIAutomator2",
    #"appium:appWaitActivity": "com.anvationlabs.se_dashboarui.homescreen_activity",#runningspeedo_activity
    "platformName": "Android",
    "platformVersion": "10.0",
    #"appium:automationName":"Appium",
    #"appium:deviceName": "device",
    "deviceName": "192.168.20.219:5555",
    "noReset" : True,
    "newCommandTimeout" : "120"
    # "ignoreHiddenApiPolicyError": "true"
    #"newCommandTimeout":"500"
    #"appium:udid": "192.168.20.11:5555"
}
driver = webdriver.Remotere('http://localhost:4723/wd/hub', desired_caps)
driver.launch_app()
driver.implicitly_wait(10)

#_1245_kms_homescreen
soc=65
socValuesByte = soc.to_bytes(length=1,byteorder="little")
bmsStateByte = bytearray([0x00])
canId = bytearray([0x0C,0x1D,0xFF,0xF2])
data = bytearray([0x02])
data1=socValuesByte+bmsStateByte
# write(BMS_StatusCanId, BMS_StatusDataSize, socValuesByte + bmsStateByte)
command = "adb.exe -P 5037 -s 192.168.20.219:5555 shell cansend slcan0 {}#{}".format((canId).hex().upper(), (data1).hex().upper())
cmd=(canId).hex().upper()+'#'+(data1).hex().upper()
print(command)
# subprocess.run(command)
driver.execute_script("adb shell cansend slcan0 {}".format(cmd))
# subprocess.getstatusoutput(command)


