from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# 设置Chrome浏览器的配置项
chrome_options = Options()
#chrome_options.add_argument('--headless')  # 无界面模式
#chrome_options.add_argument('--start-maximized')  # 窗口最大化模式

# 创建一个ChromeDriver实例
driver = webdriver.Chrome(options=chrome_options)

# 目标链接
url = 'https://leetcode.cn/problemset/all/'

# 访问目标链接
driver.get(url)

# 等待所有暂不尝试按钮出现并关闭它们
wait = WebDriverWait(driver, 10)
buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//button[text()="暂不尝试"]')))
for btn in buttons:
    btn.click()


# 获取包含所有题目信息的列表
# question_list = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[6]/div[2]/div/div/div[2]/div')
question_list = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[5]/div[2]/div/div/div[2]/div')


print('show question_list=', question_list)
# 存储试题列表
df = pd.DataFrame()
# 遍历所有题目信息
for question in question_list:
    # 获取序号、标题、难度等级、通过率和题目链接
    temp = question.find_element(By.XPATH, './div[2]/div/div/div/div').text.strip()
    number, title = temp.split('.')
    difficulty = question.find_element(By.XPATH, './div[5]/span').text.strip()
    acceptance = question.find_element(By.XPATH, './div[4]/span').text.strip()
    link = question.find_element(By.XPATH, './div[2]/div/div/div/div/a').get_attribute('href')

    # 打印题目信息
    print(f'序号：{number}\n标题：{title}\n难度等级：{difficulty}\n通过率：{acceptance}\n链接：{link}\n')
    row = {}
    row['problem_id'] = number
    row['title'] = title
    row['difficulty'] = difficulty
    row['acceptance'] = acceptance
    row['link'] = link
    df = df._append(row, ignore_index=True)
print("df",df)
df.to_excel('C:/Users/18810/Aliyun_Tianchi/数据科学家的成长之路/21天ChatGPT训练营/Leecode采集与数据库建立/3-数据采集/LeetCode试题列表.xlsx', index=False)
# 关闭浏览器窗口
driver.quit()
