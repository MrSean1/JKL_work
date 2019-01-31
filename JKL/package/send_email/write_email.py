import re
from datetime import datetime

from send_email.send_email import Email
from short_message.short_message import send_sms


# '568327240@qq.com'
# em_user = '295861809@qq.com'
# pwd = 'irzrbrekyaldbicf'
# address = ['295861809@qq.com', ]
# smtp_server = 'smtp.qq.com'
# phone = ['8613120362121', '8615311460485', '8613910860759']


class WriteEmail():
    def __init__(self, message, title, filename='./email_msg/warn_email.txt'):
        self.message = message
        self.title = title
        self.filename = filename

    def write(self):
        try:
            with open(self.filename, 'a') as f:
                f.write('%s。\n' % self.title)
                f.write('%s。\n\n' % self.message)
        except Exception:
            with open(self.filename, 'w') as f:
                f.write('')

    def del_email(self):
        try:
            with open(self.filename, "r+") as f:
                f.seek(0)
                f.truncate()
        except Exception:
            with open(self.filename, 'w') as f:
                f.write('')

    def send(self, count, em_user, pwd, address, smtp_server, info='K线'):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.filename) as f:
                message = f.read()
        except Exception:
            message = ''
        if message:
            title = now_time + info + '监测问题总和'
            Email(em_user, pwd, address, smtp_server).send_email(message, title)
        # else:
        #     if self.filename == 'warn_api.txt' and len(address) == 2:
        #         address.pop(1)
        #     title = now_time + info + ' 监测正常'
        #     if count == 0:
        #         Email(em_user, pwd, address, smtp_server).send_email(message, title)

    def send_sm(self, phone):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.filename) as f:
                message = f.read()
        except Exception:
            message = ''
        if message != '':
            message_list = message.split("\n\n")
            # 所有包含网络请求错误得每条信息
            q_list = []
            for i in message_list:
                if '交易所网络请求问题' in i:
                    q_list.append(i)
            pattern = r"[a-mo-zA-Z0-9]*交易所"
            name_list = re.compile(pattern).findall(str(q_list))
            # 有网络请求错误的交易所名称列表  去重后的
            name_new_list = []
            for i in name_list:
                if name_list.count(i) > 10 and i not in name_new_list:
                    name_new_list.append(i)
            message_sms = now_time + str(name_new_list) + '交易对网络请求错误达到10对以上'
            if name_new_list:
                for i in phone:
                    send_sms(message_sms, phone=i)

    def send_sm_price(self, phone):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.filename) as f:
                message = f.read()
        except Exception:
            message = ''
        if message != '':
            message_list = message.split("\n\n")
            # 所有包含网络请求错误得每条信息
            fall_list = []
            rise_list = []
            for i in message_list:
                if '涨幅过大，已超过30%' in i:
                    fall_list.append(i)
                if '跌幅过大，已超过30%' in i:
                    rise_list.append(i)
            pattern = r"[a-mo-zA-Z0-9]*交易所[a-zA-Z]*币种"
            name_list_fall = re.compile(pattern).findall(str(fall_list))
            name_list_rise = set(re.compile(pattern).findall(str(rise_list)))
            if name_list_rise:
                smg_rise = now_time + str(set(name_list_rise)) + '跌幅过大，已超过30%，请查看k线确认是否出现问题' + '\n'
            else:
                smg_rise = ''
            if name_list_fall:
                smg_fall = now_time + str(set(name_list_fall)) + '涨幅过大，已超过30%，请查看k线确认是否出现问题' + '\n'
            else:
                smg_fall = ''

            smg_all = smg_fall + smg_rise
            if smg_all:
                for i in phone:
                    send_sms(smg_all, phone=i)

    def send_fxh_sm(self, phone):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.filename) as f:
                message = f.read()
        except Exception:
            message = ''
        if message != '':
            message = now_time + ": " + message
            for i in phone:
                send_sms(message, phone=i)

    def send_depth_all_sm(self, phone):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.filename) as f:
                message = f.read()
        except Exception:
            message = ''
        if message != '':
            message_list = message.split("\n\n")
            message_dict = dict()
            for i in message_list:
                pattern1 = r"交易所：[a-mo-zA-Z0-9]*"
                pattern2 = r"交易对:[a-zA-Z]*"
                name_list_title = re.compile(pattern1).findall(i)
                name_list_name = re.compile(pattern2).findall(i)
                if len(name_list_title) != 0 and len(name_list_name) != 0:
                    if name_list_title[0] in message_dict.keys():
                        message_dict[name_list_title[0]].append(name_list_name[0])
                    else:
                        message_dict[name_list_title[0]] = [name_list_name[0]]
            if message_dict:
                smg = now_time + ' ' + str(message_dict) + '这些交易对最低卖价和最高买价出现问题，请查看网页进行确认。'
                if smg:
                    for i in phone:
                        send_sms(smg, phone=i)
            else:
                q_list = []
                for i in message_list:
                    if '交易所网络请求问题' in i:
                        q_list.append(i)
                pattern = r"[a-mo-zA-Z0-9]*交易所"
                name_list = re.compile(pattern).findall(str(q_list))
                # 有网络请求错误的交易所名称列表  去重后的
                name_new_list = []
                for i in name_list:
                    if name_list.count(i) > 5 and i not in name_new_list:
                        name_new_list.append(i)
                message_sms = '市场深度价格监控：' + now_time + str(name_new_list) + '交易对网络请求错误达到5对以上'
                if name_new_list:
                    for i in phone:
                        send_sms(message_sms, phone=i)


# '568327240@qq.com'
# em_user = '295861809@qq.com'
# pwd = 'irzrbrekyaldbicf'
# address = ['295861809@qq.com', ]
# smtp_server = 'smtp.qq.com'
# em_user = 'pkusimon@qq.com'
# pwd = 'zvgtfnzjvlkmbdig'
# address = ['295861809@qq.com', '568327240@qq.com']
# smtp_server = 'smtp.qq.com'
# phone = ['8613120362121', '8615311460485', '8613910860759']
