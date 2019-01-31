# 创建账户
# a = "insert into user(type, mobile, country_code, password, paypass_setting, auth_status, ga_status, level, logins, status, flag) values(1, '"
# b = "', '+86', '$2a$10$4p8WXyjgREewIMEAC8tno.sqkHalr34cDa8g8CT8inVIfWn6BbYai', 0, 1, 0, -1, 0, 1, 1);"
# for i in range(1):
#     print(a + str(12012340001 + i) + b)
#
# # insert into user(type, mobile, country_code, password, paypass_setting, auth_status, ga_status, level, logins, status, flag) values(1, '12012340001', '+86', '$2a$10$4p8WXyjgREewIMEAC8tno.sqkHalr34cDa8g8CT8inVIfWn6BbYai', 0, 1, 0, -1, 0, 1, 1);

aa = 'insert into user(type, mobile, country_code, password, paypass_setting, auth_status, ga_status, level, logins, status, flag) values'
bb = "(1, '%s', '+86', '$2a$10$4p8WXyjgREewIMEAC8tno.sqkHalr34cDa8g8CT8inVIfWn6BbYai', 0, 1, 0, -1, 0, 1, 1)"
cc = ''
for i in range(2500):
    if i == 2500:
        cc += bb % str(12012340001 + i) + ';'
    else:
        cc += bb % str(12012340001 + i) + ', '
print(aa + cc)


# 创建账户币的地址
c = "insert into `account`(user_id,coin_id,`status`,balance_amount,freeze_amount,recharge_amount, withdrawals_amount,net_value,lock_margin,float_profit,total_profit,version) select id as user_id, '"
d = "' as coin_id, '1' as `status`, '0' as balance_amount, '0' as freeze_amount, '0' as recharge_amount,'0' as withdrawals_amount, '0' as net_value,'0' as lock_margin, '0' as float_profit,'0' as total_profit, '0' as version from user where `id`  not in ( select user_id  FROM `ex_trade`.`account` where coin_id = '"
e = "' ) ;"
for coin_id in ['1059282603964833794']:
    print(c + coin_id + d + coin_id + e)

c1 = "update `account` set `balance_amount`  = 1000000 where `coin_id` ="
c2 = " and `user_id`  in ( SELECT id FROM user  where `mobile`  >='"
c3 = "' and mobile <='"
c4 = "' );"
# insert into `account`(user_id,coin_id,`status`,balance_amount,freeze_amount,recharge_amount, withdrawals_amount,net_value,lock_margin,float_profit,total_profit,version) select id as user_id, '1051479657631973377' as coin_id, '1' as `status`, '0' as balance_amount, '0' as freeze_amount, '0' as recharge_amount,'0' as withdrawals_amount, '0' as net_value,'0' as lock_margin, '0' as float_profit,'0' as total_profit, '0' as version from user where `id`  not in ( select user_id  FROM `ex_trade`.`account` where coin_id = '1051479657631973377' ) ;



# 给账户加币
coin1 = ['1059282603964833794']
coin2 = ['1022477152397598722']
# 从第几个账户开始
startp = 5000
for i in range(len(coin1)):
    # print(c1 + coin1[i] + c2 + str(15549595533) + c3 + str(15549595533) + c4)
    # print(c1 + coin2[i] + c2 + str(12012345000) + c3 + str(12012345000) + c4)
    print(c1 + coin1[i] + c2 + str(12012340001 + 38 * (i + startp)) + c3 + str(12012340038 + 38 * (i + startp)) + c4)
    print(c1 + coin2[i] + c2 + str(12012340001 + 38 * (i + startp)) + c3 + str(12012340038 + 38 * (i + startp)) + c4)
# update `account` set `balance_amount`  = 1000000 where `coin_id` =1043831549529890818 and `user_id`  in ( SELECT id FROM user  where `mobile`  >='12012340723' and mobile <='12012340760' );
# update `account` set `balance_amount`  = 1000000 where `coin_id` =1059282603964833794 and `user_id`  in ( SELECT id FROM user  where `mobile`  >='12012345001' and mobile <='12012347000' );
# update `account` set `balance_amount`  = 1000000 where `coin_id` =1022477152397598722 and `user_id`  in ( SELECT id FROM user  where `mobile`  >='12012345001' and mobile <='12012347000' );
