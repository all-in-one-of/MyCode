# encoding=utf-8

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# 前台开启浏览器模式
def openChrome():
    # 加启动配置
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    # 打开chrome浏览器
    driver = webdriver.Chrome(chrome_options=option)
    return driver

# 授权操作
def operationAuth(driver):
    url = "http://cf.3dintime.com/"
    driver.get(url)
    # 找到输入框并输入查询内容
    userName = driver.find_element_by_name("user")
    userName.send_keys("yingtai")
    pwdName = driver.find_element_by_name("pwd")
    pwdName.send_keys('YT56894!@#')
    a = driver.find_elements_by_class_name('btn')
    a[0].click()
    # 提交表单
    # driver.find_element_by_xpath("//*[@id='su']").click()
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    print(a)

# 方法主入口
if __name__ == '__main__':
    # 加启动配置
    driver = openChrome()
    operationAuth(driver)
