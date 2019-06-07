from mt4_account import MT4Account
from Mythread import MyThread

account = [
    # ADSS
    # ['222057797', '172.31.22.70'],
    # ['222057801', '172.31.18.143'],
    # ['222057152', '172.31.30.98'],
    # ['222057149', '172.31.25.98'],
    # ['222057751', '172.31.31.227'],
    # ['222057730', '172.31.44.173'],
    # ['222057728', '172.31.29.23'],
    # ['222057267', '172.31.24.73'],
    # ['222057151', '172.31.22.4'],
    # ['222057873', '172.31.29.31'],
    # ['222057937', '172.31.22.70'],
    # ['222057875', '172.31.18.143'],
    # ['222057942', '172.31.44.173'],
    # ['222057943', '172.31.29.23'],
    # ['222057982', '172.31.30.98'],
    # ['222057985', '172.31.31.227'],
    # ['222058034', '172.31.24.73'],
    # ['222058031', '172.31.25.98'],
    # ['222058035', '172.31.29.31'],
    # ['222058041', '172.31.22.70'],
    # ['222058036', '172.31.22.4'],
    # ['222058100', '172.31.18.143'],
    # # IFC
    # ['59466', '172.31.22.70'],
    # ['59575', '172.31.18.143'],
    # ['59670', '172.31.44.173'],
    # # #ThinkForexAU-Live
    # ['9767126', '172.31.44.173'],
    # ['9767128', '172.31.30.98'],
    # ['9767134', '172.31.29.23'],
    # ['9767028', '172.31.31.227'],
    # # # SimpleFX-LiveUK
    # ['232841', '172.31.22.4'],
    # ['233815', '172.31.29.23'],
    # ['233873', '172.31.30.98'],
    # ['233862', '172.31.29.23'],
    # ['233878', '172.31.22.70'],
    ['233877', '172.31.31.227'],
    # ['232989', '172.31.24.73'],
    # ['232911', '172.31.25.98'],
    ['233875', '172.31.29.31'],
    # ['234116', '172.31.18.143'],
    ['234123', '172.31.44.173'],
    ['234827', '172.31.30.98'],
    ['234125', '172.31.31.227'],
    ['234839', '172.31.22.4'],
    # ['234124', '172.31.24.73'],
    ['234941', '172.31.25.98'],
    ['234942', '172.31.29.31'],
    ['234832', '172.31.22.70'],
    ['234937', '172.31.18.143'],
    ['234940', '172.31.44.173'],
    # # AVA
    # ['80031475', '172.31.29.31'],
    # # demo
    # ['9017161', '18.130.236.155'],
    # ['9017159', '18.130.236.155'],
    # ['9017158', '18.130.236.155'],
]


# acc = [MT4Account(acc) for acc in account]
# cl_th = [MyThread(i.close_all_position, args=()) for i in acc]
# [th.start() for th in cl_th]
# [th.join() for th in cl_th]
# [th.get_result() for th in cl_th]

def cancle_symbol_pos(symbol):
    orderID = list()
    acc = [MT4Account(acc[0], acc[1]) for acc in account]
    cl_th = [MyThread(i.get_trade_order(), args=()) for i in acc]
    [th.start() for th in cl_th]
    [th.join() for th in cl_th]
    result = [th.get_result() for th in cl_th]
    for trader_order in result:
        if trader_order:
            orderID.append([[order_id['ticket'], order_id['lots']] for order_id in trader_order])
        else:
            orderID.append([])
    for i in range(len(acc)):
        mt4_cancle_pos_th = [MyThread(while_cancle_pos, args=(acc[i], j)) for j in orderID if j]
        [th.start() for th in mt4_cancle_pos_th]
        [th.join() for th in mt4_cancle_pos_th]
        [th.get_result() for th in mt4_cancle_pos_th]


def while_cancle_pos(class_acc, order_list):
    result = list()
    for order in order_list:
        ret = class_acc.close_position(order[0], order[1])
        if ret:
            result.append(ret)
        else:
            result.append(ret)
