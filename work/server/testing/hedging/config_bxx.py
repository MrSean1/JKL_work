# from price import *


def get_config(ex_name, symbol):
    ret = {
        'symbol': symbol,
        'quantity_scale_buy': 0.2,
        'quantity_scale_sell': 0.2,
        'total_quant_per_day_btc': 1000,
        'account_fee': 0.001
    }
    auto_price = False
    if symbol == ['BTC', 'USDT']:
        sym0 = 'BTC'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 10
        base_order_range_scale = 1
        avg_sym_btc = 1
        symbol_price_decimal = 2
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 2
        min_quant = 0.002
        msym = 'BTC'
        order_gap = 0
    elif symbol == ['ETH', 'USDT']:
        sym0 = 'ETH'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 150
        base_order_range_scale = 1
        avg_sym_btc = 1 / 15
        symbol_price_decimal = 4
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.03
        msym = 'ETH'
        order_gap = 0
    elif symbol == ['LTC', 'USDT']:
        sym0 = 'LTC'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 500
        base_order_range_scale = 1
        avg_sym_btc = 1 / 115
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.005
    elif symbol == ['CC', 'USDT']:
        sym0 = 'CC'
        sym_base0 = 'USDT'
        exchange_base = 'fixed'
        base_order_quantity_scale = 15000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 15000
        symbol_price_decimal = 8
        symbol_quant_decimal = 2
        symbol_quant_int_decimal = -1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.005
        auto_price = BaseWavingPrice(ex_name, symbol[0], symbol[1], symbol_price_decimal,
                                     0.03, 0.033, 0.027, 0.03, 0.001)
    elif symbol == ['ETH', 'BTC']:
        sym0 = 'ETH'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 100
        base_order_range_scale = 1
        avg_sym_btc = 1 / 15
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.03
        msym = 'ETH'
        order_gap = 0
    elif symbol == ['EMBC', 'ETH']:
        sym0 = 'EMBC'
        sym_base0 = 'ETH'
        exchange_base = 'fixed'
        base_order_quantity_scale = 20000
        base_order_range_scale = 2
        avg_sym_btc = 1 / 150000
        symbol_price_decimal = 8
        symbol_quant_decimal = 0
        symbol_quant_int_decimal = -2
        ret['quantity_scale_buy'] = 0.08
        min_quant = 10
        msym = 'ETH'
        order_gap = 0.01
        auto_price = BaseWavingPrice(ex_name, symbol[0], symbol[1], symbol_price_decimal,
                                     0.00002, 0.00003, 0.00001, 0.00002, 0.001)
    elif symbol == ['AE', 'USDT']:
        sym0 = 'AE'
        sym_base0 = 'BTC'
        exchange_base = 'binance'
        base_order_quantity_scale = 4000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 4000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                   sym0, sym_base0, 1, change_mode='m', change_sym='BTC', change_sym_base='USDT')
    elif symbol == ['TRX', 'USDT']:
        sym0 = 'TRX'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 180000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 200000
        symbol_price_decimal = 6
        symbol_quant_decimal = 1
        symbol_quant_int_decimal = -2
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
    elif symbol == ['VEN', 'USDT']:
        sym0 = 'VEN'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 4200
        base_order_range_scale = 1
        avg_sym_btc = 1 / 4500
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
    elif symbol == ['OMG', 'USDT']:
        sym0 = 'OMG'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 1000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1200
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
    elif symbol == ['ZRX', 'USDT']:
        sym0 = 'ZRX'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 6000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 10000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                   sym0, sym_base0, 1, change_mode='m', change_sym='BTC', change_sym_base='USDT')
    elif symbol == ['MKR', 'USDT']:
        sym0 = 'MKR'
        sym_base0 = 'USDT'
        exchange_base = 'okex'
        base_order_quantity_scale = 5
        base_order_range_scale = 1
        avg_sym_btc = 1 / 10
        symbol_price_decimal = 4
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.05
    elif symbol == ['ICX', 'USDT']:
        sym0 = 'ICX'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 7000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 7000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                   sym0, sym_base0, 1, change_mode='m', change_sym='BTC', change_sym_base='USDT')
    elif symbol == ['BTM', 'USDT']:
        sym0 = 'BTM'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 20000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 25000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
    elif symbol == ['REP', 'USDT']:
        sym0 = 'REP'
        sym_base0 = 'BTC'
        exchange_base = 'binance'
        base_order_quantity_scale = 300
        base_order_range_scale = 1
        avg_sym_btc = 1 / 250
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                   sym0, sym_base0, 1, change_mode='m', change_sym='BTC', change_sym_base='USDT')
    elif symbol == ['DGD', 'USDT']:
        sym0 = 'DGD'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 100
        base_order_range_scale = 1
        avg_sym_btc = 1 / 90
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                   sym0, sym_base0, 1, change_mode='m', change_sym='BTC', change_sym_base='USDT')
    elif symbol == ['BAT', 'USDT']:
        sym0 = 'BAT'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 25000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 30000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                   sym0, sym_base0, 1, change_mode='m', change_sym='BTC', change_sym_base='USDT')
    elif symbol == ['ZIL', 'USDT']:
        sym0 = 'ZIL'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 150000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 180000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
    elif symbol == ['DGD', 'ETH']:
        sym0 = 'DGD'
        sym_base0 = 'ETH'
        exchange_base = 'huobi'
        base_order_quantity_scale = 60
        base_order_range_scale = 1
        avg_sym_btc = 1 / 90
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['MKR', 'ETH']:
        sym0 = 'MKR'
        sym_base0 = 'ETH'
        exchange_base = 'okex'
        base_order_quantity_scale = 3
        base_order_range_scale = 1
        avg_sym_btc = 1 / 10
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.05
    elif symbol == ['ICX', 'ETH']:
        sym0 = 'ICX'
        sym_base0 = 'ETH'
        exchange_base = 'huobi'
        base_order_quantity_scale = 4000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 7000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.02
    elif symbol == ['ICX', 'BTC']:
        sym0 = 'ICX'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 5000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 7000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['ZRX', 'ETH']:
        sym0 = 'ZRX'
        sym_base0 = 'ETH'
        exchange_base = 'huobi'
        base_order_quantity_scale = 5000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 7000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['ZRX', 'BTC']:
        sym0 = 'ZRX'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 4000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 7000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['OMG', 'ETH']:
        sym0 = 'OMG'
        sym_base0 = 'ETH'
        exchange_base = 'huobi'
        base_order_quantity_scale = 1100
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['TRX', 'ETH']:
        sym0 = 'TRX'
        sym_base0 = 'ETH'
        exchange_base = 'huobi'
        base_order_quantity_scale = 170000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 200000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['AE', 'ETH']:
        sym0 = 'AE'
        sym_base0 = 'ETH'
        exchange_base = 'binance'
        base_order_quantity_scale = 3000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 4000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['REP', 'ETH']:
        sym0 = 'REP'
        sym_base0 = 'ETH'
        exchange_base = 'binance'
        base_order_quantity_scale = 250
        base_order_range_scale = 1
        avg_sym_btc = 1 / 250
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.02
    elif symbol == ['REP', 'BTC']:
        sym0 = 'REP'
        sym_base0 = 'BTC'
        exchange_base = 'binance'
        base_order_quantity_scale = 300
        base_order_range_scale = 1
        avg_sym_btc = 1 / 250
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['BTM', 'ETH']:
        sym0 = 'BTM'
        sym_base0 = 'ETH'
        exchange_base = 'huobi'
        base_order_quantity_scale = 17000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 25000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['OMG', 'BTC']:
        sym0 = 'OMG'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 1000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['BTM', 'BTC']:
        sym0 = 'BTM'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 22000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 25000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['TRX', 'BTC']:
        sym0 = 'TRX'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 250000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 200000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['AE', 'BTC']:
        sym0 = 'AE'
        sym_base0 = 'BTC'
        exchange_base = 'binance'
        base_order_quantity_scale = 9000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 4000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    elif symbol == ['HB', 'USDT']:
        sym0 = 'HB'
        sym_base0 = 'USDT'
        exchange_base = 'fixed'
        base_order_quantity_scale = 10000
        base_order_range_scale = 3
        avg_sym_btc = 1 / 200000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 0
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.005
        auto_price = BaseWavingPrice(ex_name, symbol[0], symbol[1], symbol_price_decimal,
                                     0.02, 0.04, 0.02, 0.027, 0.001)
    elif symbol == ['HB', 'BTC']:
        sym0 = 'HB'
        sym_base0 = 'USDT'
        exchange_base = 'bxx'
        base_order_quantity_scale = 4000
        base_order_range_scale = 3
        avg_sym_btc = 1 / 200000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 0
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.01
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, ex_name,
                                   sym0, sym_base0, 1, change_mode='d', change_sym='BTC', change_sym_base='USDT')
    elif symbol == ['HB', 'ETH']:
        sym0 = 'HB'
        sym_base0 = 'USDT'
        exchange_base = 'bxx'
        base_order_quantity_scale = 5000
        base_order_range_scale = 3
        avg_sym_btc = 1 / 200000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 0
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.01
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, ex_name,
                                   sym0, sym_base0, 1, change_mode='d', change_sym='ETH', change_sym_base='USDT')
    elif symbol == ['APV', 'ETH']:
        sym0 = 'APV'
        sym_base0 = 'ETH'
        exchange_base = 'fixed'
        base_order_quantity_scale = 2000
        base_order_range_scale = 2
        avg_sym_btc = 1 / 7500
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 0
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.005
        auto_price = BaseWavingPrice(ex_name, symbol[0], symbol[1], symbol_price_decimal,
                                     0.00073, 0.00208, 0.0001, 0.001, 0.001)
    #   开始  QTUM/USDT 4.44 ≈ 30.30 CNY 涨幅 -5.93% 高 5.08 低 4.41 24H量 569399 QTUM
    elif symbol == ['QTUM', 'USDT']:
        sym0 = 'QTUM'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 4500
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1500
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.005

    # EOS/USDT 5.8209 ≈ 39.66 CNY 涨幅 -2.55% 高 6.3391 低 5.7541 24H量 20249116 EOS
    elif symbol == ['EOS', 'USDT']:
        sym0 = 'EOS'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 4800
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1200
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.005
    # DASH/USDT177.00 ≈ 1205.37 CNY 涨幅 -6.87% 高 193.06 低 177.00 24H量 31304 DASH
    elif symbol == ['DASH', 'USDT']:
        sym0 = 'DASH'
        sym_base0 = 'USDT'
        exchange_base = 'huobi'
        base_order_quantity_scale = 150
        base_order_range_scale = 1
        avg_sym_btc = 1 / 40
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.005
    # XMX/BTC0.0000001015 ≈ 0.00474 CNY 涨幅 -2.30% 高 0.0000001074 低 0.0000001000 24H量 46881071 XMX
    elif symbol == ['XMX', 'USDT']:
        sym0 = 'XMX'
        sym_base0 = 'BTC'
        exchange_base = 'hadax'
        base_order_quantity_scale = 50000000
        base_order_range_scale = 2
        avg_sym_btc = 1 / 70000000
        symbol_price_decimal = 6
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
        auto_price = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                   sym0, sym_base0, 1, change_mode='m', change_sym='BTC', change_sym_base='USDT')
    # LTC/BTC0.008587 ≈ 406.34 CNY 涨幅 -0.59% 高 0.008709 低 0.008587 24H量 59025 LTC
    elif symbol == ['LTC', 'BTC']:
        sym0 = 'LTC'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 4800
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1200
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.005
    # XMX/BTC0.0000001017 ≈ 0.00482 CNY 涨幅 -1.54% 高 0.0000001046 低 0.0000001000 24H量 54112816 XMX
    elif symbol == ['XMX', 'BTC']:
        sym0 = 'XMX'
        sym_base0 = 'BTC'
        exchange_base = 'hadax'
        base_order_quantity_scale = 2000000
        base_order_range_scale = 2
        avg_sym_btc = 1 / 10000000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.02

    elif symbol == ['BNB', 'BTC']:
        sym0 = 'BNB'
        sym_base0 = 'BTC'
        exchange_base = 'binan'
        base_order_quantity_scale = 3000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 600
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.005
    # HT/BTC0.00030327 ≈ 14.37 CNY 涨幅 -1.02% 高 0.00031260 低 0.00030000 24H量 1390270 HT
    elif symbol == ['HT', 'BTC']:
        sym0 = 'HT'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 7000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 5000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.01
    # NAS/BTC0.00025783 ≈ 12.20 CNY 涨幅 -0.31% 高 0.00026457 低 0.00025591 24H量 481396 NAS
    elif symbol == ['NAS', 'BTC']:
        sym0 = 'NAS'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 10000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 4000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02
    # ZIL/BTC0.0000062821 ≈ 0.29 CNY 涨幅 +0.64% 高 0.0000065387 低 0.0000061612 24H量 6674737 ZIL 火币全球站
    elif symbol == ['ZIL', 'BTC']:
        sym0 = 'ZIL'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 240000
        base_order_range_scale = 2
        avg_sym_btc = 1 / 160000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.02

    elif symbol == ['AE', 'BTC']:
        sym0 = 'AE'
        sym_base0 = 'BTC'
        exchange_base = 'binan'
        base_order_quantity_scale = 5000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 6000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.02
    # CTXC/BTC0.00005709 ≈ 2.70 CNY 涨幅 +2.86% 高 0.00005829 低 0.00005468 24H量 1694492 CTXC
    elif symbol == ['CTXC', 'BTC']:
        sym0 = 'CTXC'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 15000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 20000
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.02
    # DASH/BTC0.026803 ≈ 1271.38 CNY 涨幅 +0.34% 高 0.026851 低 0.025535 24H量 16856 DASH
    elif symbol == ['DASH', 'BTC']:
        sym0 = 'DASH'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 250
        base_order_range_scale = 1
        avg_sym_btc = 1 / 50
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'ETH'
        order_gap = 0.01
    # EOS/BTC0.00085957 ≈ 40.78 CNY 涨幅 -1.49% 高 0.00087676 低 0.00085353 24H量 6229061 EOS
    elif symbol == ['EOS', 'BTC']:
        sym0 = 'EOS'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 6000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1250
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'BTC'
        order_gap = 0.005
    # elif symbol == ['HSR', 'BTC']:
    # QTUM/BTC0.000656 ≈ 31.18 CNY 涨幅 -0.75% 高 0.000669 低 0.000650 24H量 48683 QTUM
    elif symbol == ['QTUM', 'BTC']:
        sym0 = 'QTUM'
        sym_base0 = 'BTC'
        exchange_base = 'huobi'
        base_order_quantity_scale = 1000
        base_order_range_scale = 1
        avg_sym_btc = 1 / 1600
        symbol_price_decimal = 8
        symbol_quant_decimal = 4
        symbol_quant_int_decimal = 1
        min_quant = 0.0001
        msym = 'LTC'
        order_gap = 0.02
    ret['sym0'] = sym0
    ret['sym_base0'] = sym_base0
    ret['exchange_base'] = exchange_base
    ret['base_order_quantity_scale'] = base_order_quantity_scale
    ret['base_order_range_scale'] = base_order_range_scale
    ret['avg_sym_btc'] = avg_sym_btc
    ret['symbol_price_decimal'] = symbol_price_decimal
    ret['symbol_quant_decimal'] = symbol_quant_decimal
    ret['symbol_quant_int_decimal'] = symbol_quant_int_decimal
    ret['min_quant'] = min_quant
    ret['msym'] = msym
    ret['order_gap'] = order_gap
    if not auto_price:
        ret['auto_price'] = FixScalePrice(ex_name, symbol[0], symbol[1], symbol_price_decimal, -10000, exchange_base,
                                          sym0, sym_base0, 1)
    else:
        ret['auto_price'] = auto_price
    return ret
