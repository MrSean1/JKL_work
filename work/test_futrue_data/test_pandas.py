# *_*coding:utf-8 *_*
"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS


def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # Record tracking variables at the end of each day.
    algo.schedule_function(
        record_vars,
        algo.date_rules.every_day(),
        algo.time_rules.market_close(),
    )
    context.future = continuous_future('YM', offset=0, roll='volume', adjustment='mul')


def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    a = data.history([context.future], fields=['open', 'high', 'low', 'close', 'volume'], bar_count=1440 * 365 * 6,
                     frequency='1m')
    b = a.ix[:, :, 0]
    # for i in range(1440):
    # print(b.columns)
    c = str(b.columns.tolist()).replace(' ', '') + ','
    for i in range(len(b.values)):
        value_str = str(b.values[i]).replace(' ', '') + ','
        c += value_str
    print(c)
    # print(b.iloc[0].values)
    # print(b.iloc[-1].values)


def record_vars(context, data):
    """
    Plot variables at the end of each day.
    """
    # a=data_NK_HS-YM.history(context.future,fields=['open', 'high', 'low', 'close', 'volume'], bar_count=1440, frequency='1m')
    # print(a)


def handle_data(context, data):
    """
    Called every minute.
    """
    # b = data_NK_HS-YM.current(context.future,fields=['open', 'high', 'low', 'close', 'volume'])
    # a=data_NK_HS-YM.history(context.future,fields=['open', 'high', 'low', 'close', 'volume'], bar_count=1, frequency='1m')
    # print(a)


