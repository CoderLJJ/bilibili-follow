from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import xlrd
import time
import random
option = webdriver.ChromeOptions()
#设置为开发者模式，避免被识别
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument(
    r'--user-data-dir=C:\Users\81316\AppData\Local\Google\Chrome\linjj\Default')  # 加载前面获取的 个人资料路径
driver = webdriver.Chrome(options=option)
# driver.maximize_window()
data = xlrd.open_workbook('user.xlsx')
table = data.sheets()[0]
links = table.col_values(int(1))
for url in links[1:]:
    print(url)
    try:
        driver.get(url)
        time.sleep(1)
    except Exception as e:
        print(e)
    wait = WebDriverWait(driver, 3, 0.2)  # 设置等待时间
    try:
        driver.find_element_by_xpath('//*[@class="h-action"]/span[@class="h-f-btn h-follow"]').click()
    except Exception as e:
        print(e)
driver.quit()