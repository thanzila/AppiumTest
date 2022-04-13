from appium import webdriver
desired_caps = {
    #"appium:app": "C:/Users/thanz/Documents/SE_DashboarUI/SE_DashboarUI/app/build/outputs/apk/debug/app-debug.apk",
    "appium:appPackage": "com.anvationlabs.se_dashboardui",
    "appium:appActivity": "com.anvationlabs.se_dashboardui.SplashScreen",
    "appium:deviceName": "device",
    "appium:udid": "192.168.20.11:5555",
    "appium:platformName": "Android"
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.launch_app()
driver.implicitly_wait(10)





