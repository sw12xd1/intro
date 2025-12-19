from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
 
desired_caps = {
  'platformName': 'Android', # 被测手机是安卓
  'platformVersion': '16', # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
  'deviceName': 'SW12', # 设备名，安卓手机可以随意填写
  'appPackage': 'com.dianping.v1', # 启动APP Package名称
  'appActivity': '.NovaMainActivity', # 启动Activity名称
  'unicodeKeyboard': True, # 自动化需要输入中文时填True
  'resetKeyboard': True, # 执行完程序恢复原来输入法
  'noReset': True,       # 不要重置App
  'newCommandTimeout': 6000,
  'automationName' : 'UiAutomator2'
  # 'app': r'd:\apk\bili.apk',
}
 
# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', 
  options=UiAutomator2Options().load_capabilities(desired_caps))

driver.implicitly_wait(0)

# 根据id定位 免费试，点击
driver.find_element(AppiumBy.XPATH, "//*[@resource-id='com.dianping.v1:id/main_home_content_layout']//android.widget.LinearLayout//android.view.ViewGroup[2]"
                     ).click()

#筛选
driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("更多筛选")').click()

driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("我可报名")').click()


def swipe():
    screen_size = driver.get_window_size()
    start_x = screen_size["width"] / 2
    start_y = screen_size["height"] * 0.5
    end_y = start_y - 348
    end_x = start_x
    driver.swipe(start_x, start_y, end_x, end_y, duration=500)
    print(f"📱 下滑完成")

    
def free_draw(driver):
    """
    单次流程：免费抽 → 尝试报名 → 确认报名 → 完成 → 返回 → 下滑348px
    :param driver: Appium 驱动实例
    """
    # 1. 点击“免费抽”
    while True:
        try:
            # 最多等待0.5秒检测按钮（快速判断，不卡顿）
            free_draw_btn = WebDriverWait(driver, 0.5).until(
                EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("免费抽")'))
            )
            
            btn_location = free_draw_btn.location
            btn_y = btn_location['y']  # 获取按钮的y坐标
            
            # 判断按钮y坐标是否超出2488
            if btn_y > 2488:
                print(f"⚠️  免费抽按钮y坐标({btn_y})超出2488，直接下滑")
                swipe()
                continue  # 继续循环查找
            
            target_x = btn_location['x'] - 200
            target_y = btn_location['y']
            
            target_x = int(target_x)
            target_y = int(target_y)
            

            driver.tap([(target_x, target_y)], duration=50)  # duration=50ms（短按，模拟真实点击）
            print(f"✅ 点击成功！目标坐标：(X:{target_x}, Y:{target_y})（免费抽按钮X-200px）")
            break  # 点击成功，退出循环
        
        except TimeoutException:
            time.sleep(2)
            print("⚠️  未找到「免费抽」按钮，已滑动一页，2秒后重新检测...")
            swipe()



    time.sleep(1)  # 等待

    btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("我要报名")')
    btn.click()
    print("✅ 点击「我要报名」成功")

    # 3. 点击“确认报名”
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("确认报名")').click()
    print("✅ 点击「确认报名」成功")

    # 4. 返回
    driver.press_keycode(4)

    # 5. 下滑 348px（无论报名成功/失败，均下滑继续）
    swipe()

n=0
while True:
    print(f"\n===== 执行第{n}轮流程 =====")
    free_draw(driver)
    n+=1