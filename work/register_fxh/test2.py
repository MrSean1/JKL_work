from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

proxy = Proxy(
    {
        'proxyType': ProxyType.MANUAL,
        'httpProxy': '175.175.70.15:3617'  # 代理ip和端口
    }
)
# 新建一个“期望技能”，哈哈
desired_capabilities = DesiredCapabilities.CHROME.copy()
# 把代理ip加入到技能中
proxy.add_to_capabilities(desired_capabilities)
driver = webdriver.Chrome(
    executable_path="D:/work/register_fxh/chromedriver.exe",
    desired_capabilities=desired_capabilities
)
# 测试一下
# driver.get('http://httpbin.org/ip')
driver.get('https://www.feixiaohao.com/user/login')
# print(driver.page_source)

# 现在开始切换ip
# 再新建一个ip
proxy = Proxy(
    {
        'proxyType': ProxyType.MANUAL,
        'httpProxy': '112.113.107.240:894'  # 代理ip和端口
    }
)
# 再新建一个“期望技能”，（）
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# 把代理ip加入到技能中
proxy.add_to_capabilities(desired_capabilities)
# 新建一个会话，并把技能传入
driver.start_session(desired_capabilities)
driver.get('http://httpbin.org/ip')
# print(driver.page_source)
driver.close()

a = {"code": 200, "msg": "",
 "data_NK_HS-YM": [{"ip": "175.175.70.15", "port": 3617, "expire_time": "2018-10-19 10:46:39", "city": "辽宁 辽阳", "isp": "联通"},
          {"ip": "112.113.107.240", "port": 894, "expire_time": "2018-10-19 10:51:09", "city": "云南 德宏傣族景颇族自治州",
           "isp": "电信"},
          {"ip": "42.54.83.234", "port": 3617, "expire_time": "2018-10-19 10:31:29", "city": "辽宁 鞍山", "isp": "联通"},
          {"ip": "182.247.181.255", "port": 5412, "expire_time": "2018-10-19 10:46:11", "city": "云南 丽江", "isp": "电信"},
          {"ip": "180.115.223.27", "port": 3617, "expire_time": "2018-10-19 10:46:22", "city": "江苏 常州", "isp": "电信"},
          {"ip": "113.237.230.36", "port": 23564, "expire_time": "2018-10-19 10:41:50", "city": "辽宁 辽阳", "isp": "联通"},
          {"ip": "182.100.238.13", "port": 5412, "expire_time": "2018-10-19 10:31:46", "city": "江西 吉安", "isp": "电信"},
          {"ip": "106.59.35.95", "port": 3617, "expire_time": "2018-10-19 10:36:31", "city": "云南 文山壮族苗族自治州",
           "isp": "电信"},
          {"ip": "175.175.92.183", "port": 894, "expire_time": "2018-10-19 10:31:54", "city": "辽宁 辽阳", "isp": "联通"},
          {"ip": "114.99.8.96", "port": 36410, "expire_time": "2018-10-19 10:37:04", "city": "安徽 铜陵", "isp": "电信"},
          {"ip": "182.243.8.241", "port": 766, "expire_time": "2018-10-19 10:51:08", "city": "云南 昭通", "isp": "电信"},
          {"ip": "180.115.223.235", "port": 5412, "expire_time": "2018-10-19 10:51:11", "city": "江苏 常州", "isp": "电信"},
          {"ip": "116.55.75.166", "port": 5412, "expire_time": "2018-10-19 10:41:40", "city": "云南 丽江", "isp": "电信"},
          {"ip": "125.123.25.4", "port": 23564, "expire_time": "2018-10-19 10:51:28", "city": "浙江 嘉兴", "isp": "电信"},
          {"ip": "119.180.193.249", "port": 23564, "expire_time": "2018-10-19 10:32:16", "city": "山东 枣庄", "isp": "联通"},
          {"ip": "111.72.106.31", "port": 3617, "expire_time": "2018-10-19 10:36:46", "city": "江西 吉安", "isp": "电信"},
          {"ip": "182.244.168.209", "port": 894, "expire_time": "2018-10-19 10:36:11", "city": "云南 曲靖", "isp": "电信"},
          {"ip": "117.90.7.230", "port": 5412, "expire_time": "2018-10-19 10:47:51", "city": "江苏 镇江", "isp": "电信"},
          {"ip": "175.147.96.217", "port": 894, "expire_time": "2018-10-19 10:41:35", "city": "辽宁 鞍山", "isp": "联通"},
          {"ip": "183.130.59.71", "port": 23564, "expire_time": "2018-10-19 10:46:30", "city": "浙江 温州", "isp": "电信"}]}
