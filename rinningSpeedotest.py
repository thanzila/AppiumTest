from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {
    #"appium:app": "C:/Users/6114402/Downloads/SE_DashboarUI/simpleenergyservice/build/outputs/apk/debug/simpleenergyservice-debug.apk",
    #"appium:app": "C:/MyStoredData/Android/SE_DashboarUI/app/build/outputs/apk/debug/app-debug.apk",
    "appium:appPackage": "com.anvationlabs.se_dashboarui",
    "appium:appActivity": "com.anvationlabs.se_dashboarui.SplashScreen",
    #"appium:appWaitActivity": "com.anvationlabs.se_dashboarui.homescreen_activity",#runningspeedo_activity
    "platformName": "Android",
    "appium:deviceName": "Android Emulator",
    "appium:udid": "emulator-5554"
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.launch_app()
driver.implicitly_wait(10)