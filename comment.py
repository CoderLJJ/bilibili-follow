from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import xlrd

option = webdriver.ChromeOptions()
# 设置为开发者模式，避免被识别
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=option)
driver.maximize_window()
data = xlrd.open_workbook('python.xlsx')
table = data.sheets()[0]
links = table.col_values(int(1))
dts = []
for url in links[1:]:
    try:
        driver.get(url)
    except Exception as e:
        print(e)
    wait = WebDriverWait(driver, 10, 0.2)  # 设置等待时间
    while True:
        # 评论区是异步加载的，需要向下滑动才会出现数据
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        try:
            # 断言判断 网页源码是否有 ’没有更多评论‘ 这几个字 最底部才有，可以作为判断依据
            assert '没有更多评论' in driver.page_source
            break
        except AssertionError as e:  # 找不到就继续向下滑动
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
    try:
        # 查找评论区用户列表超链接
        a_list = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@class="user-face"]/a')), message='没有用户评论')
    except Exception as e:
        print(e)
    for a in a_list:
        try:
            user = a.get_attribute('href')  # 取出a链接
        except Exception as e:
            print(e)
        lst = []
        lst.append(user)
        dts.append(lst)
    df = pd.DataFrame(dts, columns=['urls'])
df.to_excel('user' + '.xlsx', encoding='utf-8')  # 保存
driver.quit()
