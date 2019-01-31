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
        'NBXX': [],
    },
    'BTC': {
        'ETH': [],
        'REP': [],
        'ICX': [],
        'AE': [],
        'NBXX': [],
    },
    'ETH': {
        'EMBC': [],
        'OMG': [],
        'REP': [],
        'ICX': [],
        'AE': [],
        'APV': [],
        'NBXX': [],
    },
    'NBXX': {
        'LPAY': [],
        'EPAY11': [],
        'NBPAY': [],
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
        'ZRX': [],
        'ZIL': [],
        'BAT': [],
        'ICX': [],
        'REP': [],
        'WTC': [],
        'GNT': [],
        'SNT': [],
        'IOST': [],
        'LINK': [],
        'ELF': [],
        'QASH': [],
        'CMT': [],
        'POLY': [],
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
        'REP': [],
    },
    'ETH': {
        'MKR': [],
        'DGD': [],
        'ICX': [],
        'ZRX': [],
        'REP': [],
    }
}
account_info['HBANK'] = {
    'BTC': {
        'ETH': [],
        'HB': [],
        'BTM': [],
        'ZIL': [],
        'IOST': [],
        'CTXC': [],
    },
    'USDT': {
        'BTC': [],
        'ETH': [],
        'HB': [],
        'BTM': [],
        'ZIL': [],
        'IOST': [],
        'CTXC': [],
    },
    'ETH': {
        'HB': [],
        'BTM': [],
        'ZIL': [],
        'IOST': [],
        'CTXC': [],
    }
}
account_info['COINFLY'] = {
    'USDT': {
        'BTC': [],
        'ETH': [],
        'DUH': [],
        'TTGS': [],
        'PTIT': [],
        'FGBL': [],
        'LCOC': [],
        'ICWF': [],
        'ZVX': [],
        'TUOD': [],
        'JLO': [],
        'NCBS': [],
    },
    'BTC': {
        'ETH': [],
        'AE': [],
        'TRX': [],
        'OMG': [],
        'ZRX': [],
        'ICX': [],
        'BTM': [],
        'BAT': [],
        'DGD': [],
        'DUH': [],
        'TTGS': [],
        'PTIT': [],
        'FGBL': [],
        'LCOC': [],
        'ICWF': [],
        'ZVX': [],
        'TUOD': [],
        'JLO': [],
        'NCBS': [],
    },
    'ETH': {
        'AE': [],
        'TRX': [],
        'OMG': [],
        'ZRX': [],
        'ICX': [],
        'BTM': [],
        'BAT': [],
        'DGD': [],
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
        'COTO': [],
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
account_info['GT210'] = {
    'USDT': {
        'BTC': [],
        'ETH': [],
        'EOS': [],
        'XRP': [],
        'LTC': [],
        'TRX': [],
        'ADA': [],
        'BTM': [],
        "ONT": [],
        'NEO': [],
    }
}

# BXX account
ac = pd.read_csv('D:/work/all_jkl/code_1009/accounts_bxx.csv')
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

for i in range(570, 608):
    account_info['BXX']['USDT']['NBXX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(608, 646):
    account_info['BXX']['BTC']['NBXX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(646, 684):
    account_info['BXX']['ETH']['NBXX'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(684, 722):
    account_info['BXX']['NBXX']['LPAY'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(722, 760):
    account_info['BXX']['NBXX']['EPAY11'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

for i in range(760, 798):
    account_info['BXX']['NBXX']['NBPAY'].append(['BXX', str(12012340001 + i), '1234Rty77899x'])

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

for i in range(456, 494):
    account_info['TTEX']['BTC']['ZRX'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(494, 532):
    account_info['TTEX']['BTC']['ZIL'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(532, 570):
    account_info['TTEX']['BTC']['BAT'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(570, 608):
    account_info['TTEX']['BTC']['ICX'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(608, 646):
    account_info['TTEX']['BTC']['REP'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(646, 684):
    account_info['TTEX']['BTC']['WTC'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(684, 722):
    account_info['TTEX']['BTC']['GNT'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(722, 760):
    account_info['TTEX']['BTC']['SNT'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(760, 798):
    account_info['TTEX']['BTC']['IOST'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(798, 836):
    account_info['TTEX']['BTC']['LINK'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(836, 874):
    account_info['TTEX']['BTC']['ELF'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(874, 912):
    account_info['TTEX']['BTC']['QASH'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])
#  新加的
for i in range(912, 950):
    account_info['TTEX']['BTC']['CMT'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

for i in range(950, 988):
    account_info['TTEX']['BTC']['POLY'].append(['TTEX', str(12012340001 + i), '1234Rty77899x'])

# DAPP account
for i in range(38):
    account_info['DAPP']['USDT']['AE'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['DAPP']['USDT']['TRX'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['DAPP']['USDT']['VEN'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(114, 152):
    account_info['DAPP']['USDT']['OMG'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(152, 190):
    account_info['DAPP']['USDT']['ZRX'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(190, 228):
    account_info['DAPP']['USDT']['MKR'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(228, 266):
    account_info['DAPP']['USDT']['ICX'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(266, 304):
    account_info['DAPP']['USDT']['BTM'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(304, 342):
    account_info['DAPP']['USDT']['BAT'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(342, 380):
    account_info['DAPP']['USDT']['DGD'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(380, 418):
    account_info['DAPP']['USDT']['BTC'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(418, 456):
    account_info['DAPP']['USDT']['ETH'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(456, 494):
    account_info['DAPP']['ETH']['MKR'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(494, 532):
    account_info['DAPP']['ETH']['DGD'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(532, 570):
    account_info['DAPP']['BTC']['ETH'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(570, 608):
    account_info['DAPP']['ETH']['ICX'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(608, 646):
    account_info['DAPP']['ETH']['ZRX'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(646, 684):
    account_info['DAPP']['BTC']['REP'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

for i in range(684, 722):
    account_info['DAPP']['ETH']['REP'].append(['DAPP', str(12012340001 + i), '1234Rty77899x'])

# HBANK account
for i in range(38):
    account_info['HBANK']['BTC']['ETH'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['HBANK']['USDT']['BTC'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['HBANK']['USDT']['ETH'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(114, 152):
    account_info['HBANK']['USDT']['HB'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(152, 190):
    account_info['HBANK']['BTC']['HB'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(190, 228):
    account_info['HBANK']['ETH']['HB'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(228, 266):
    account_info['HBANK']['USDT']['BTM'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(266, 304):
    account_info['HBANK']['BTC']['BTM'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(304, 342):
    account_info['HBANK']['ETH']['BTM'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(342, 380):
    account_info['HBANK']['USDT']['ZIL'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(380, 418):
    account_info['HBANK']['BTC']['ZIL'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(418, 456):
    account_info['HBANK']['ETH']['ZIL'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(456, 494):
    account_info['HBANK']['USDT']['IOST'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(494, 532):
    account_info['HBANK']['BTC']['IOST'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(532, 570):
    account_info['HBANK']['ETH']['IOST'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(570, 608):
    account_info['HBANK']['USDT']['CTXC'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(608, 646):
    account_info['HBANK']['BTC']['CTXC'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

for i in range(646, 684):
    account_info['HBANK']['ETH']['CTXC'].append(['HBANK', str(12012340001 + i), '1234Rty77899x'])

# COINFLY account
for i in range(38):
    account_info['COINFLY']['USDT']['BTC'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['COINFLY']['USDT']['ETH'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['COINFLY']['BTC']['ETH'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(114, 152):
    account_info['COINFLY']['BTC']['AE'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(152, 190):
    account_info['COINFLY']['ETH']['AE'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(190, 228):
    account_info['COINFLY']['BTC']['TRX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(228, 266):
    account_info['COINFLY']['ETH']['TRX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(266, 304):
    account_info['COINFLY']['BTC']['OMG'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(304, 342):
    account_info['COINFLY']['ETH']['OMG'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(342, 380):
    account_info['COINFLY']['BTC']['ZRX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(380, 418):
    account_info['COINFLY']['ETH']['ZRX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(418, 456):
    account_info['COINFLY']['BTC']['ICX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(456, 494):
    account_info['COINFLY']['ETH']['ICX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(494, 532):
    account_info['COINFLY']['BTC']['BTM'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(532, 570):
    account_info['COINFLY']['ETH']['BTM'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(570, 608):
    account_info['COINFLY']['BTC']['BAT'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(608, 646):
    account_info['COINFLY']['BTC']['DGD'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(646, 684):
    account_info['COINFLY']['ETH']['DGD'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(684, 722):
    account_info['COINFLY']['ETH']['BAT'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(722, 760):
    account_info['COINFLY']['BTC']['DUH'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(760, 798):
    account_info['COINFLY']['BTC']['TTGS'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(798, 836):
    account_info['COINFLY']['BTC']['PTIT'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(836, 874):
    account_info['COINFLY']['BTC']['FGBL'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(874, 912):
    account_info['COINFLY']['BTC']['LCOC'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(912, 950):
    account_info['COINFLY']['BTC']['ICWF'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(950, 988):
    account_info['COINFLY']['BTC']['ZVX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(988, 1026):
    account_info['COINFLY']['BTC']['TUOD'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1026, 1064):
    account_info['COINFLY']['BTC']['JLO'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1064, 1102):
    account_info['COINFLY']['BTC']['NCBS'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1102, 1140):
    account_info['COINFLY']['USDT']['DUH'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1140, 1178):
    account_info['COINFLY']['USDT']['TTGS'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1178, 1216):
    account_info['COINFLY']['USDT']['PTIT'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1216, 1254):
    account_info['COINFLY']['USDT']['FGBL'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1254, 1292):
    account_info['COINFLY']['USDT']['LCOC'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1292, 1330):
    account_info['COINFLY']['USDT']['ICWF'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1330, 1368):
    account_info['COINFLY']['USDT']['ZVX'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1368, 1406):
    account_info['COINFLY']['USDT']['TUOD'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1406, 1444):
    account_info['COINFLY']['USDT']['JLO'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

for i in range(1444, 1482):
    account_info['COINFLY']['USDT']['NCBS'].append(['COINFLY', str(12012340001 + i), '1234Rty77899x'])

# COINX
for i in range(38):
    account_info['COINX']['USDT']['BTC'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['COINX']['USDT']['ETH'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['COINX']['USDT']['LTC'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(114, 152):
    account_info['COINX']['USDT']['EOS'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(152, 190):
    account_info['COINX']['USDT']['DASH'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(190, 228):
    account_info['COINX']['USDT']['QTUM'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(228, 266):
    account_info['COINX']['USDT']['DOGE'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(266, 304):
    account_info['COINX']['USDT']['CNXX'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(304, 342):
    account_info['COINX']['USDT']['HPY'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(342, 380):
    account_info['COINX']['USDT']['HPS'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(380, 418):
    account_info['COINX']['USDT']['GATC'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(1104, 1140):
    account_info['COINX']['USDT']['DVC'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(456, 494):
    account_info['COINX']['USDT']['XMX'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(494, 532):
    account_info['COINX']['BTC']['ETH'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(532, 570):
    account_info['COINX']['BTC']['LTC'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(570, 608):
    account_info['COINX']['BTC']['EOS'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(608, 646):
    account_info['COINX']['BTC']['DASH'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(646, 684):
    account_info['COINX']['BTC']['QTUM'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(684, 722):
    account_info['COINX']['BTC']['CNXX'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(722, 760):
    account_info['COINX']['BTC']['HPS'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(760, 798):
    account_info['COINX']['BTC']['TRX'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(798, 836):
    account_info['COINX']['BTC']['ZIL'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(836, 874):
    account_info['COINX']['BTC']['AE'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(874, 912):
    account_info['COINX']['BTC']['CTXC'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(912, 950):
    account_info['COINX']['BTC']['XMX'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(950, 988):
    account_info['COINX']['BTC']['HT'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(988, 1026):
    account_info['COINX']['BTC']['BNB'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(1026, 1064):
    account_info['COINX']['BTC']['NAS'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(1064, 1102):
    account_info['COINX']['USDT']['HC'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

for i in range(1140, 1178):
    account_info['COINX']['USDT']['COTO'].append(['COINX', str(12012340001 + i), '1234Rty77899x'])

# GT210
for i in range(38):
    account_info['GT210']['USDT']['BTC'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(38, 76):
    account_info['GT210']['USDT']['ETH'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(76, 114):
    account_info['GT210']['USDT']['EOS'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(114, 152):
    account_info['GT210']['USDT']['XRP'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(152, 190):
    account_info['GT210']['USDT']['LTC'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(190, 228):
    account_info['GT210']['USDT']['TRX'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(228, 266):
    account_info['GT210']['USDT']['ADA'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(266, 304):
    account_info['GT210']['USDT']['BTM'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(304, 342):
    account_info['GT210']['USDT']['ONT'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])

for i in range(342, 380):
    account_info['GT210']['USDT']['NEO'].append(['GT210', str(12012340001 + i), '1234Rty77899x'])


