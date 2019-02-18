# *_*coding:utf-8 *_*
import threading
import time

from sp_account import Account
from send_email import Email

product_list = ["YMH9", "HSIH9", "SSIH9"]
em_user = '295861809@qq.com'
pwd = 'irzrbrekyaldbicf'
address = ['295861809@qq.com', ]
smtp_server = 'smtp.qq.com'


def run(prod_code):
    sp_account = Account('DEMO201901267')
    time.sleep(5)
    while True:
        ret = sp_account.write_data_for_file(prod_code)
        if ret is False:
            msg = sp_account.login()
            if msg is False:
                # 发邮件提醒
                email_msg = '登陆失败，请检测是程序出错还是服务出错\n，' + msg
                email_title = 'SP数据抓取问题'
                Email(em_user=em_user, pwd=pwd, address=address, smtp_server=smtp_server).send_email(message=email_msg,
                                                                                                     title=email_title)
                break
            else:
                continue


def main():
    """
    采用多线程对sp期货数据进行抓取
    :return:
    """
    thread = [threading.Thread(target=run, args=(product,)) for product in product_list]
    [th.start() for th in thread]
    [th.join() for th in thread]


if __name__ == '__main__':
    main()
