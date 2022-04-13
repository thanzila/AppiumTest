from gettext import gettext

from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = {
    #"appium:app": "C:/Users/6114402/Downloads/SE_DashboarUI/simpleenergyservice/build/outputs/apk/debug/simpleenergyservice-debug.apk",
    #"appium:app": "C:/GitAlabs/RidotK/04_Software/SE_DashboardUI/app/build/outputs/apk/debug/app-debug.apk",
    "appium:appPackage": "com.anvationlabs.se_dashboardui",
    "appium:appActivity": "com.anvationlabs.se_dashboardui.SplashScreen",
    #"appium:appWaitActivity": "com.anvationlabs.se_dashboarui.homescreen_activity",#runningspeedo_activity
    "platformName": "Android",
    "appium:deviceName": "device",
    "appium:udid": "192.168.20.11:5555",

}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.launch_app()
driver.implicitly_wait(10)
# driver.start_activity("com.anvationlabs.se_dashboarui",".runningspeedo_activity")
# km_h_rs=driver.find_element_by_id('km_h_rs')
# print(km_h_rs.text)
# _35_rs=driver.find_element_by_id('_35_rs')
# print(_35_rs.text)
# _9_41_rs=driver.find_element_by_id('_9_41_rs')
# print(_9_41_rs.text)
# _188_kms_rs=driver.find_element_by_id('_188_kms_rs')
# print(_188_kms_rs.text)
# _1245_kms_rs=driver.find_element_by_id('_1245_kms_rs')
# print(_1245_kms_rs.text)
# odo_text_rs=driver.find_element_by_id('odo_text_rs')
# print(odo_text_rs.text)
# _48_3_kms_rs=driver.find_element_by_id('_48_3_kms_rs')
# print(_48_3_kms_rs.text)
# rs_battrey_value=driver.find_element_by_id('rs_battrey_value')
# print(rs_battrey_value.text)

# motor_on_rs=driver.find_element_by_id('motor_on_rs')
# print(motor_on_rs.text)


# _30_psi_homescreen=driver.find_element_by_id('_30_psi_homescreen')
# print(_30_psi_homescreen.text)
# _32_psi_homescreen=driver.find_element_by_id('_32_psi_homescreen')
# print(_32_psi_homescreen)
# parking_text_homescreen=driver.find_element_by_id('parking_text_homescreen')
# print(parking_text_homescreen)
# rear_homescreen=driver.find_element_by_id('rear_homescreen')
# print(rear_homescreen)
# front_homescreen=driver.find_element_by_id('front_homescreen')
# print(front_homescreen)
# parking_icon_homescreen=driver.find_element_by_id('parking_icon_homescreen')
# parking_icon_homescreen.click()

# lunaticMode=driver.find_element_by_id('lunaticMode')
# lunaticMode.click()
#
# sportsMode=driver.find_element_by_id('sportsMode')
# sportsMode.click()
#
# rideMode=driver.find_element_by_id('rideMode')
# rideMode.click()
#
# ecoMode=driver.find_element_by_id('ecoMode')
# ecoMode.click()
#
# # motor_status_homescreen=driver.find_element_by_id('motor_status_homescreen')
# # print(motor_status_homescreen.text)
#
#
# # txtmotoron=driver.find_element_by_id('motor_on_homescreen')
# # print(txtmotoron.text)
#
# txtrangeblp=driver.find_element_by_id('range_blp')
# print(txtrangeblp.text)
#
# # vwmotor= driver.find_element_by_id('motor_on_homescreen')
# # print(vwmotor.text)
#
# txtclck=driver.find_element_by_id('time_homescreen')
# print(txtclck.text)
#
# txtbp=driver.find_element_by_id('homescreen_battery_progress')
# print(txtbp.text)
#
# txtbv=driver.find_element_by_id('homescreen_battery_value')
# print(txtbv.text)
#
# txtokms=driver.find_element_by_id('_0_homescreen')
# print(txtokms.text)
#
# txt1245=driver.find_element_by_id('_1245_kms_homescreen')
# print(txt1245.text)
#
# tvodo=driver.find_element_by_id('odo_homescreen')
# print(tvodo.text)
#
# tvavg=driver.find_element_by_id('avg__speed_homescreen')
# print(tvavg.text)
#
# txt32kms=driver.find_element_by_id('_32_km_h_homescreen')
# print(txt32kms.text)
#
# txttrip=driver.find_element_by_id('trip_a_homescreen')
# print(txttrip.text)
# txttrip.click()
# print(txttrip.text)
# txttrip.click()
# print(txttrip.text)
#
# txt45=driver.find_element_by_id('_45_mins_tlp')
# print(txt45.text)
#
# #maps=driver.find_element_by_id('maps_icon_homescreen')
# #maps.click()
#
# txtview=driver.find_element_by_id('_48_kms_tlp')
# print(txtview.text)
#
# # driver.wait_activity("com.anvationlabs.se_dashboarui.homescreen_activity",1000,1)
# # bprg1=driver.find_element(By.ID,'com.anvationlabs.se_dashboarui:id/settings_bg_homescreen')
#
#
# # bprg12=driver.find_element(By.ID,'com.anvationlabs.se_dashboarui:id/homescreen_battery_progress')
# # print(bprg12)_48_kms_tlp
settings_image_button = driver.find_element_by_id('settings_menu_homescreen')
settings_image_button.click()
vehicleStatus=driver.find_element_by_id('vehicle_status')
vehicleStatus.click()
customize=driver.find_element_by_id('customize_window')
customize.click()
connectivity=driver.find_element_by_id('connectivity')
connectivity.click()
sosSetup=driver.find_element_by_id('sos_setup')
sosSetup.click()
systemInfo=driver.find_element_by_id('system_info')
systemInfo.click()
myOne_bg=driver.find_element_by_id('my_one')
myOne_bg.click()
my_one_text=driver.find_element_by_id('my_one_text')
print(my_one_text)
vehicle_status_text=driver.find_element_by_id('vehicle_status_text')
print(vehicle_status_text.text)
customize_text=driver.find_element_by_id('customize_text')
print(customize_text.text)
connectivity_text=driver.find_element_by_id('connectivity_text')
print(connectivity_text.text)
sos_setup_text=driver.find_element_by_id('sos_setup_text')
print(sos_setup_text.text)
system_info_text=driver.find_element_by_id('system_info_text')
print(system_info_text.text)
shutdown_btn=driver.find_element_by_id('shutdown_btn')
shutdown_btn.click()
settings_image_close=driver.find_element_by_id('setting_close_btn')
settings_image_close.click()
# # bprg=driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[3]/android.widget.RelativeLayout[5]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ProgressBar")#driver.find_element_by_id('com.anvationlabs.se_dashboarui:id/homescreen_battery_value')
# # #bprg1=driver.find_element_by_id('com.anvationlabs.se_dashboarui:id/range_blp')
# # if bprg.set_value("10%"):
# #       bprg.set_text("20%")
#       #bprg1.set_text("20 Kms")
# #driver.wait_activity("com.anvationlabs.se_dashboarui.homescreen_activity", 1000, 1)
# #driver.stop_client()