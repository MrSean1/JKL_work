from ex_api.exchange import Exchange, get_USDT_CNY
import random
import time


# 基本的定价
class Price:
    def __init__(self, ex_name, sym, sym_base, price_decimal, start_price, adjust_by_market=False):
        # 初始化时需要指定交易对和起始价格
        self.ex_name = ex_name
        self.sym = sym
        self.sym_base = sym_base
        self.symbol = [self.sym, self.sym_base]
        self.api_bxx = Exchange('bxx', [self.ex_name, '', '']).api
        self.price = start_price
        self.decimal = price_decimal
        self.flag_adjust = adjust_by_market

    def set_params(self, *args):
        # 给定一种策略，重新设置参数
        pass

    def refresh_price(self):
        # 给定一种策略，刷新并返回价格
        try:
            if self.flag_adjust:
                self.adjust_by_market()
        except Exception as e:
            print(e)
        return self.price

    def adjust_by_market(self):
        # 根据当前市场价格调整定价
        try:
            tic = eval(self.api_bxx.get_tick(self.symbol))
            self.price = round((0.7 * self.price + 0.3 * sum(tic[1:5]) / 4), self.decimal)
        except Exception as e:
            print(e)

    def slight_wave(self, wave_range=0.001):
        return round(self.price * (1 + random.uniform(-wave_range, wave_range)), self.decimal)

    def save_price(self, out_dir, flag_new=False):
        # 将当前时间和价格存储至日志，或者存储至临时文件与其它进程交流
        mode = 'a'
        if flag_new:
            mode = 'w'
        with open(out_dir, mode) as f:
            f.writelines(time.asctime() + '\n' + self.ex_name + ' ' + self.sym + ' ' + self.sym_base + '\n' + str(
                self.price) + '\n\n')


class BaseWavingPrice(Price):
    def __init__(self, ex_name, sym, sym_base, price_decimal, start_price, hb, lb, price_object, base_waving_range,
                 adjust_by_market=True):
        Price.__init__(self, ex_name, sym, sym_base, price_decimal, start_price, adjust_by_market)
        self.hb = hb
        self.lb = lb
        self.p_obj = price_object
        self.base_waving_range = base_waving_range
        self.count = 0

    def set_params(self, start_price, hb, lb, price_object, base_waving_range, adjust_by_market=True):
        self.price = start_price
        self.hb = hb
        self.lb = lb
        self.p_obj = price_object
        self.base_waving_range = base_waving_range
        self.flag_adjust = adjust_by_market

    def refresh_price(self):
        self.count = (self.count + 1) % 5
        if self.count == 1:
            try:
                if self.price > self.p_obj:
                    scale = random.uniform(1 - 2 * self.base_waving_range, 1 + self.base_waving_range)
                else:
                    scale = random.uniform(1 - self.base_waving_range, 1 + 2 * self.base_waving_range)
                new_price = self.price * scale
                self.price = min(max(round(new_price, self.decimal), self.lb), self.hb)
                if self.flag_adjust:
                    self.adjust_by_market()
                self.price = min(max(self.price, self.lb), self.hb)
            except Exception as e:
                print(e)
            return self.price
        else:
            return self.slight_wave(self.base_waving_range)


# 通过参照其他交易对的价格来定义
class FixScalePrice(Price):
    def __init__(self, ex_name, sym, sym_base, price_decimal, start_price, refer_ex_name, refer_sym, refer_sym_base,
                 scale, change_mode=False, change_sym=False, change_sym_base=False, adjust_by_market=False):
        Price.__init__(self, ex_name, sym, sym_base, price_decimal, start_price, adjust_by_market)
        if refer_ex_name.lower() == refer_ex_name:
            self.api_refer = Exchange(refer_ex_name, ['', '']).api
        else:
            self.api_refer = self.api_bxx
        self.refer_sym = refer_sym
        self.refer_sym_base = refer_sym_base
        self.refer_symbol = [self.refer_sym, self.refer_sym_base]
        self.scale = scale
        self.change_mode = change_mode
        self.change_symbol = [change_sym, change_sym_base]

    def set_params(self, scale, adjust_by_market=False):
        self.scale = scale
        self.flag_adjust = adjust_by_market

    def refresh_price(self):
        try:
            depth = self.api_refer.get_depth(self.refer_symbol)
            # 传入不同的self.scale(比例) 可以的到不同的比例的价格   并让价格保留几位小数
            new_price = round((float(depth['asks'][0][0]) + float(depth['bids'][0][0])) / 2 * self.scale, self.decimal)
            if self.change_mode == 'm':
                # 获取比对交易对上一次的开高低收的价格的平均值作为基准
                tic = eval(self.api_bxx.get_tick(self.change_symbol))
                new_price = round(new_price * sum(tic[1:5]) / 4, self.decimal)
            if self.change_mode == 'd':
                tic = eval(self.api_bxx.get_tick(self.change_symbol))
                new_price = round(new_price / sum(tic[1:5]) * 4, self.decimal)
            # 自己平台定价统一美元计算   若需要参照coinw（人民币）时需要用到汇率换算
            if self.change_mode == 'CNY':
                USDT_CNY = get_USDT_CNY()
                new_price = round(new_price / USDT_CNY, self.decimal)
            self.price = new_price
            # 根据当前市场价格 调整定价
            if self.flag_adjust:
                self.adjust_by_market()
        except Exception as e:
            print(e)
        return self.price


class FiveWavingPrice(Price):
    def __init__(self, ex_name, sym, sym_base, price_decimal, start_price, hb, lb, price_object, round_limit,
                 adjust_by_market=True):
        Price.__init__(self, ex_name, sym, sym_base, price_decimal, start_price, adjust_by_market)


#
class FakeStatusPrice(Price):
    def __init__(self, ex_name, sym, sym_base, price_decimal, start_price, threshold_waving, threshold_sell,
                 base_waving_range, adjust_by_market=False):
        Price.__init__(self, ex_name, sym, sym_base, price_decimal, start_price, adjust_by_market)
        self.th_waving = threshold_waving
        self.th_sell = threshold_sell
        self.base_waving_range = base_waving_range
        # status: 0 for rising, 1 for waving, 2 for decresing
        self.status = 0
        self.p_obj = random.uniform(self.price * (1 - 30 * self.base_waving_range),
                                    self.price * (1 + 150 * self.base_waving_range))
        self.hb = max(self.price, self.p_obj) * (1 + 20 * self.base_waving_range)
        self.lb = min(self.price, self.p_obj) * (1 - 20 * self.base_waving_range)
        self.wave_count = 0
        self.refresh_range_count = 0

    def set_params(self, status, threshold_waving, threshold_sell):
        self.th_waving = threshold_waving
        self.th_sell = threshold_sell
        self.status = status

    def refresh_status(self, customer_balance):
        if customer_balance > self.th_sell:
            return 2
        elif customer_balance > self.th_waving:
            return 1
        else:
            return 0

    def refresh_price(self, param_dict):
        c_balance = param_dict['customer_balance']
        new_status = self.refresh_status(c_balance)
        print('customer balance is ' + str(c_balance) + '\nnew status is ' + str(new_status))
        if new_status == 2 and self.status != 2:
            self.status = new_status
            self.price = round(self.price * (1 - 5 * self.base_waving_range), self.decimal)
            return self.price
        elif new_status == 1 and self.status != 1:
            self.status = new_status
            self.p_obj = self.price
            self.lb = self.price * (1 - 50 * self.base_waving_range)
            self.hb = self.price * (1 + 50 * self.base_waving_range)
        elif new_status == 0 and self.status != 0:
            self.status = new_status
            self.p_obj = random.uniform(self.price * (1 - 30 * self.base_waving_range),
                                        self.price * (1 + 150 * self.base_waving_range))
            self.hb = max(self.price, self.p_obj) * (1 + 20 * self.base_waving_range)
            self.lb = min(self.price, self.p_obj) * (1 - 20 * self.base_waving_range)
        self.wave_count = (self.wave_count + 1) % 3
        self.refresh_range_count = (self.refresh_range_count + 1) % 300
        print(
            'new price object is ' + str(self.p_obj) + 'high bound is ' + str(self.hb) + 'low bound is ' + str(self.lb))
        if self.refresh_range_count == 0 and self.status == 0:
            self.p_obj = random.uniform(self.price * (1 - 30 * self.base_waving_range),
                                        self.price * (1 + 150 * self.base_waving_range))
            self.hb = max(self.price, self.p_obj) * (1 + 20 * self.base_waving_range)
            self.lb = min(self.price, self.p_obj) * (1 - 20 * self.base_waving_range)
        if self.wave_count == 1:
            if self.status == 0:
                if self.price >= self.p_obj:
                    scale = random.uniform(1 - 2 * self.base_waving_range,
                                           1 + self.base_waving_range)
                else:
                    scale = random.uniform(1 - self.base_waving_range,
                                           1 + 2 * self.base_waving_range)
            elif self.status == 2:
                scale = random.uniform(1 - 5 * self.base_waving_range, 1 + 2 * self.base_waving_range)
            elif self.status == 1:
                if self.price >= self.p_obj:
                    scale = random.uniform(1 - self.price / self.p_obj * self.base_waving_range,
                                           1 + self.base_waving_range)
                else:
                    scale = random.uniform(1 - self.base_waving_range,
                                           1 + self.p_obj / self.price * self.base_waving_range)
            self.price = round(self.price * scale, self.decimal)
            if self.status == 1:
                self.price = max(min(self.price, self.hb), self.lb)
            return self.price
        else:
            return self.slight_wave(self.base_waving_range)
