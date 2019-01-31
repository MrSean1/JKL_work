# coding=utf-8
import time
from get_phone import get_phone
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd

# ip = get_ip(1, 'https').get_ip_address()
#
# print(ip[0])
# proxy = Proxy(
#     {
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': ip[0]  # 代理ip和端口
#     }
# )
# # 新建一个“期望技能”，哈哈
# desired_capabilities = DesiredCapabilities.CHROME.copy()
# # 把代理ip加入到技能中
# proxy.add_to_capabilities(desired_capabilities)
driver = webdriver.Chrome(
    executable_path="D:/work/register_fxh/chromedriver.exe",

)
# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
count = 0
while True:
    driver.get("https://www.feixiaohao.com/user/signin")
    data = driver.find_element_by_class_name("new-tab-cell").text
    # 打印数据内容
    print(data)
    phone = get_phone('64160004', 'wang190421')
    phone_num = phone.get_phone_num()
    driver.find_element_by_id("phoneNum").send_keys(phone_num)
    driver.find_element_by_id("sendCode").click()
    # time.sleep(20)
    time.sleep(3)
    verification = phone.get_sm(phone_num)
    driver.find_element_by_id("phoneVerify").send_keys(verification)
    driver.find_element_by_id("pwd1-1").send_keys("wht123456")
    driver.find_element_by_id("pwd2").send_keys("wht123456")
    driver.find_element_by_id("submit").click()
    time.sleep(5)
    # 登录
    driver.find_element_by_id("phoneNum").send_keys(phone_num)
    driver.find_element_by_id("pwd1").send_keys("wht123456")
    driver.find_element_by_xpath("//form[@id='loginForm']/button").click()
    time.sleep(2)
    data = pd.DataFrame([[phone_num]])
    data.to_csv('非小号手机号cvs', header=False, index=False, mode='a+', encoding='utf-8')
    driver.find_element_by_id("input-sm").send_keys("天天国际", Keys.DOWN, Keys.ENTER)
    driver.find_element_by_xpath("//div[@class='action-bar']/button").click()
    driver.find_element_by_id("input-sm").send_keys("CoinX", Keys.DOWN, Keys.ENTER)
    driver.find_element_by_xpath("//div[@class='action-bar']/button").click()
    print('账户余额为：' + str(phone.get_account()))
    print('撤销手机号状态为：' + phone.release_phone(phone_num))
    time.sleep(1)

    # # 再次新建ip
    # count += 1
    # if count % 5 == 0:
    #     ip = get_ip(1, 'https').get_ip_address()
    #     proxy = Proxy(
    #         {
    #             'proxyType': ProxyType.MANUAL,
    #             'httpProxy': ip  # 代理ip和端口
    #         }
    #     )
    #     desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    #     proxy.add_to_capabilities(desired_capabilities)
    #     driver.start_session(desired_capabilities)

    # 点击跳转到天天国际交易所
    # driver.find_element_by_xpath("//div[@class='slide']/div[1]/text()").click()
    # # driver.find_element_by_link_text('交易平台').click()
    # driver.find_element_by_xpath("//[@id='tableEx']/tbody/td[1]/a").click()
    # # 点击关注
    # driver.find_element_by_id("FocusExChose").click()
    # 点击退出
    # a = input('输入结果')
    # if a == '1':
    #     # driver.find_element_by_link_text('注册').click()
    #     time.sleep(3)
    # elif a == '2':
    #     break

# # 获取新的页面快照
# driver.save_screenshot("长城.png")
# # 打印网页渲染后的源代码
# print(driver.page_source)
# # 获取当前页面Cookie
# print(driver.get_cookies())
# # ctrl+a 全选输入框内容
# driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')
# # ctrl+x 剪切输入框内容
# driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x')
# # 输入框重新输入内容
# driver.find_element_by_id("kw").send_keys("atguigu")
# # 模拟Enter回车键
# driver.find_element_by_id("su").send_keys(Keys.RETURN)
# # 清除输入框内容
# driver.find_element_by_id("kw").clear()
# # 生成新的页面快照
# driver.save_screenshot("atguigu.png")
# # 获取当前url
# print(driver.current_url)
# # 关闭当前页面，如果只有一个页面，会关闭浏览器# driver.close()
# # 关闭浏览器
# driver.quit()
