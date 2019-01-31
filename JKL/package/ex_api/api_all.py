from ex_api.api_bixin import api_bixin
from ex_api.api_binance import api_binance
from ex_api.api_zb import api_zb
from ex_api.api_bithumb import api_bithumb
from ex_api.api_coinw import api_coinw
from ex_api.api_huobi import api_huobi
from ex_api.api_coinegg import api_coinegg
from ex_api.api_tt import api_tt
from ex_api.api_vbtc import api_vbtc
from ex_api.api_hadax import api_hadax
from ex_api.api_bxx import api_bxx
from ex_api.api_okex import api_okex


def api(exchange_name, key):
    return eval('api_' + exchange_name + '(key)')
