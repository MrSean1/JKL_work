# *_*coding:utf-8 *_*
import numpy as np
import pandas as pd
import talib

'''
1. 初始化时需要传递进来多数K线   记录var9 及VARA
2. 只需传递最新的一根  根据历史数据可以求得 VAR9 及VARA
'''
media_list = list()
low_list = list()
high_list = list()
var9 = list()
varA = list()


class DuoKong():
    def __init__(self, kline_list):
        # self.count = count
        self.kline_list = kline_list
        self.period = None
        # if len(self.kline_list) != 1:
        #     for kline in self.kline_list:
        self.save_M_L_H_for_list()
        self.VAR9(media_list, low_list, high_list)
        self.VARA()


    # def median_low_high(self, kline):
    #     '''
    #     :param num_start: 需要从什么地方开始的K线
    #     :param number_end: 什么地方结束的K线  None表示一直到最后
    #     :return: 每根K线的中位 及所有K线的最小值 最大值
    #     '''
    #
    #     media = (kline[3] * 2 + kline[1] + kline[2]) / 4
    #     low_price = min(kline)
    #     high_price = max(kline)
    #     return media, low_price, high_price

    def save_M_L_H_for_list(self):
        if len(self.kline_list) == 1:
            media_list.append((2 * self.kline_list[0][3] + self.kline_list[0][1] + self.kline_list[0][2]) / 4)
            media_list.pop(0)
            low_list.append(min(self.kline_list)[0])
            low_list.pop(0)
            high_list.append(max(self.kline_list)[0])
            high_list.pop(0)
        else:
            for kline in self.kline_list:
                media_list.append((2 * kline[3] + kline[1] + kline[2]) / 4)
                low_list.append(min(kline))
                high_list.append(max(kline))

    def EMA(self, X, N):
        '''
        :param X: 数据
        :param N: 周期
        :return: 求N周期X值的指数加权移动平均。
        '''
        return talib.EMA(np.array(X), N)

    def VAR9(self, media_list, low_list, high_list):
        # media_list, low, high = self.median(-13)
        if len(self.kline_list) == 1:
            media = (2 * self.kline_list[0][3] + self.kline_list[0][1] + self.kline_list[0][2]) / 4
            low_list.append(min(self.kline_list[0]))
            low = min(low_list[-13:])
            high_list.append(max(self.kline_list[0]))
            high = max(high_list[-13:])
            var9.append(((media - low) / (high - low)) * 100 * 1 / 7 + var9[-1] * 6 / 7)
        else:
            # 初始的时候保存所有的var9
            X = list()
            for i in range(len(media_list)):
                X.append(
                    float(((media_list[i] - min(low_list[0:13])) / (max(high_list[0:13]) - min(low_list[0:13]))) * 100))
                var9.append(self.EMA(X, 13)[-1])

    def VARA(self):
        # 引用前一个周期的VAR9
        if len(self.kline_list) == 1:
            varA.append(2*(var9[-1]*0.333 + 0.667*var9[-2])/3 + 1*varA[-1]/3)
        else:
            X = list()
            for i in range(len(var9)):
                # if i == 0:
                #     X.append(np.nan)
                if np.isnan(var9[i]) is np.bool_(False) and np.isnan(var9[i - 1]) is np.bool_(False):
                    X.append(0.667 * var9[i - 1] + 0.333 * var9[i])
                    print(X)
                    varA.append(self.EMA(X, 2)[-1])
                elif np.isnan(var9[i]) is np.bool_(False):
                    X.append(var9[i])
                    varA.append(np.nan)
                else:
                    X.append(np.nan)
                    varA.append(np.nan)

    def Judge_more_empty(self):
        if var9[-1] > varA[-1]:
            return '多'
        elif var9[-1] < varA[-1]:
            return '空'
        elif var9[-1] == varA[-1]:
            if var9[-2] > var9[-1] and varA[-2] < varA[-1]:
                return '空'
            elif var9[-2] < var9[-1] and varA[-2] > varA[-1]:
                return '多'


# var9 = [np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#  56.270903010033436,
#  58.94648829431437,
#  64.96655518394648,
#  70.28189202102246,
#  73.90621800559688,
#  81.05005021597745,
#  86.24165794909868,
#  90.2257689253144,
#  91.15624914095271,
#  90.09044957423276,
#  91.35082013195107,
#  91.34418123111334,
#  84.9720311173518]
# X = list()
# for i in range(len(var9)):
#     # if i == 0:
#
#     if np.isnan(var9[i]) is np.bool_(False) and np.isnan(var9[i - 1]) is np.bool_(False):
#         X.append(0.667 * var9[i - 1] + 0.333 * var9[i])
#         print(X)
#         varA.append(self.EMA(X, 2)[-1])
#     else:
#         X.append(np.nan)

