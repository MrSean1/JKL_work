import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText


# sym = sys.argv[1]
# sym_base = sys.argv[2]
# symbol = [sym, sym_base]
#
# key = account_info[sym_base][sym]
# ex_cx = []
# if sym == 'GATC':
#     for i in [0, 2, 3, 5]:
#         ex_cx.append(Exchange('bixin', key[i]))
#     to_customer = '991770107@qq.com'
# elif sym == 'DVC':
#     for i in range(6):
#         ex_cx.append(Exchange('bixin', key[i]))
#     to_customer = '468415432@qq.com'


class Email():
    def __init__(self, em_user, pwd, address, smtp_server):
        self.em_user = em_user
        self.pwd = pwd
        self.address = address
        self.smtp_server = smtp_server

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
                count += 1
                print('第{}次发送错误'.format(count) + now_time + "Falied, {}".format( e))
