# *_*coding:utf-8 *_*
all_account = {'main_account': "9013762",
               'fallow_account': ["9013778", "9013777"],
               }

account_level = {
    "9013778": 1,
    "9013777": 2,
}

pos = dict()
for f_acc in all_account['fallow_account']:
    pos[f_acc] = account_level[f_acc]


em_user = '295861809@qq.com'
pwd = 'qxkrwbmoxosdbhfi'
address = ['295861809@qq.com', ]
smtp_server = 'smtp.qq.com'
