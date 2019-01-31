import pandas as pd

account_info = dict()
account_info['BXX'] = {
    'USDT': {
        'BTC': [],
        'ETH': [],
        'ZIL': [],
        'TRX': [],
        'OMG': [],
        'ZRX': [],
        'REP': [],
        'ICX': [],
        'AE': [],
    },
    'BTC': {
        'ETH': [],
        'REP': [],
        'ICX': [],
        'AE': [],
    },
    'ETH': {
        'EMBC': [],
        'OMG': [],
        'REP': [],
        'ICX': [],
        'AE': [],
        'APV': [],
    }
}
account_info['TEST'] = {
    'USDT': {
        'BTC': [],
        'ETH': []
    },
    'BTC': {
        'ETH': []
    }
}
account_info['TTEX'] = {
    'USDT': {
        'BTC': [],
        'ETH': [],
        'TRX': [],
        'REP': [],
        'BTM': []
    },
    'BTC': {
        'ETH': [],
        'OMG': [],
        'TRX': [],
        'AE': [],
        'BTM': [],
    },
    'ETH': {
        'BTM': [],
        'REP': [],
        'AE': [],
        'OMG': [],
        'TRX': []
    }
}
account_info['DAPP'] = {
    'USDT': {
        'AE': [],
        'TRX': [],
        'VEN': [],
        'OMG': [],
        'ZRX': [],
        'MKR': [],
        'ICX': [],
        'BTM': [],
        'BAT': [],
        'DGD': [],
        'BTC': [],
        'ETH': [],
    },
    'BTC': {
        'ETH': [],
    },
    'ETH': {
        'MKR': [],
        'DGD': [],
        'ICX': [],
        'ZRX': [],
    }
}
account_info['HBANK'] = {
    'BTC': {
        'ETH': [],
        'HB': [],
    },
    'USDT': {
        'BTC': [],
        'ETH': [],
        'HB': [],
    },
    'ETH': {
        'HB': [],
    }
}
account_info['COINFLY'] = {
    'USDT': {
        'BTC': [],
        'ETH': [],
    },
    'BTC': {
        'ETH': [],
        'AE': [],
        'TRX': [],
        'OMG': [],
        'ZRX': [],
        'ICX': [],
        'BTM': [],
    },
    'ETH': {
        'AE': [],
        'TRX': [],
        'OMG': [],
        'ZRX': [],
        'ICX': [],
        'BTM': [],
    }
}
account_info['COINX'] = {
    'USDT': {
        'BTC': [],
        'ETH': [],
        'EOS': [],
        'LTC': [],
        'DASH': [],
        'QTUM': [],
        'DOGE': [],
        'HPY': [],
        'CNXX': [],
        'HPS': [],
        'XMX': [],
        'GATC': [],
        'DVC': [],
        'HC': [],
    },
    'BTC': {
        'ETH': [],
        'LTC': [],
        'EOS': [],
        'QTUM': [],
        'DASH': [],
        'HPS': [],
        'CNXX': [],
        'NAS': [],
        'BNB': [],
        'HT': [],
        'XMX': [],
        'TRX': [],
        'AE': [],
        'CTXC': [],
        'ZIL': [],
    }
}

# BXX account
# ac = pd.read_csv('accounts_bxx.csv')
ac = pd.read_csv('D:\\work\\DKL\\ex_api\\accounts_bxx.csv')
ac.columns = ['user', 'pw', '1', '2', '3', '4']

for i in range(38):
    account_info['BXX']['USDT']['BTC'].append(['BXX', ac.loc[i, 'user'], ac.loc[i, 'pw']])

for i in range(38, 76):
    account_info['BXX']['USDT']['ETH'].append(['BXX', ac.loc[i, 'user'], ac.loc[i, 'pw']])

for i in range(76, 114):
    account_info['BXX']['BTC']['ETH'].append(['BXX', ac.loc[i, 'user'], ac.loc[i, 'pw']])

for i in range(36):
    account_info['BXX']['ETH']['EMBC'].append(['BXX', str(14012340001 + i), '1234Rty77899x'])

for i in range(38):
    account_info['BXX']['ETH']['OMG'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['BXX']['USDT']['OMG'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['BXX']['USDT']['TRX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(114, 152):
    account_info['BXX']['USDT']['ZRX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(152, 190):
    account_info['BXX']['USDT']['ZIL'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(190, 228):
    account_info['BXX']['ETH']['ICX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(228, 266):
    account_info['BXX']['ETH']['REP'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(266, 304):
    account_info['BXX']['ETH']['AE'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(304, 342):
    account_info['BXX']['BTC']['ICX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(342, 380):
    account_info['BXX']['BTC']['REP'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(380, 418):
    account_info['BXX']['BTC']['AE'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(418, 456):
    account_info['BXX']['USDT']['REP'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(456, 494):
    account_info['BXX']['USDT']['ICX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(494, 532):
    account_info['BXX']['USDT']['AE'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(532, 570):
    account_info['BXX']['ETH']['APV'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

# TEST account
for i in range(38):
    account_info['TEST']['USDT']['BTC'].append(['TEST', str(17700000001 + i), 'AbcD7890'])

for i in range(38, 76):
    account_info['TEST']['USDT']['ETH'].append(['TEST', str(17700000001 + i), 'AbcD7890'])

for i in range(76, 114):
    account_info['TEST']['BTC']['ETH'].append(['TEST', str(17700000001 + i), 'AbcD7890'])

# TTEX account
for i in range(38):
    account_info['TTEX']['USDT']['BTC'].append(['TTEX', str(14012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['TTEX']['USDT']['ETH'].append(['TTEX', str(14012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['TTEX']['BTC']['ETH'].append(['TTEX', str(14012340001 + i), '1234Rty77899x'])

for i in range(38):
    account_info['TTEX']['BTC']['OMG'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['TTEX']['BTC']['TRX'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['TTEX']['BTC']['AE'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(114, 152):
    account_info['TTEX']['BTC']['BTM'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(152, 190):
    account_info['TTEX']['ETH']['OMG'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(190, 228):
    account_info['TTEX']['ETH']['TRX'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(228, 266):
    account_info['TTEX']['ETH']['AE'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(266, 304):
    account_info['TTEX']['ETH']['REP'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(304, 342):
    account_info['TTEX']['ETH']['BTM'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(342, 380):
    account_info['TTEX']['USDT']['TRX'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(380, 418):
    account_info['TTEX']['USDT']['REP'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(418, 456):
    account_info['TTEX']['USDT']['BTM'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])
