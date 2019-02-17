import os
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from Log import Logger

em_user = '295861809@qq.com'
pwd = 'qxkrwbmoxosdbhfi'
address = ['295861809@qq.com', ]
smtp_server = 'smtp.qq.com'


class Email:
    def __init__(self, em_user, pwd, address, smtp_server):
        self.em_user = em_user
        self.pwd = pwd
        self.address = address
        self.smtp_server = smtp_server
        self.log = Logger('all.log', level='error')

    def send_email(self, message, title):
        count = 0
        while count < 5:
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                message_em = MIMEText(message)
                message_em['From'] = self.em_user
                # message_em['To'] = self.address
                message_em['Subject'] = title
                server = smtplib.SMTP_SSL(self.smtp_server, 465)
                server.set_debuglevel(1)
                server.login(self.em_user, self.pwd)
                server.sendmail(self.em_user, self.address, message_em.as_string())
                server.quit()
                break
            except smtplib.SMTPException as e:
                time.sleep(5)
                count += 1
                # print('第{}次发送错误'.format(count) + now_time + "Falied, {}".format(e))
                self.log.logger.error('第{}次发送错误'.format(count) + "Falied, {}".format(e))