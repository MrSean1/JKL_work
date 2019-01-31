# *_*coding:utf-8 *_*
import datetime


class LiangZhu():
    def __init__(self, klint_list):
        self.kline_list = klint_list

    def A(self):
        k_line_date = datetime.datetime.strptime(self.kline_list[-1][-1], "%Y-%m-%d %H:%M:%S")
        if k_line_date.hour < 12:
            return 60 * (k_line_date.hour - 9) - 30 + k_line_date.minute
        else:
            return 120 + 60 * (k_line_date.hour - 13) + k_line_date.minute

    def datacount(self):
        # 返回本地已有得K线个数
        return len(self.kline_list)