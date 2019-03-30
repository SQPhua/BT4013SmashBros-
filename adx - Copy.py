### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np
import talib


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
        nMarkets=CLOSE.shape[1] # this returns number of equities
        print('______________________________________________________________')
        print('Date:', DATE[0])
        for i in range(0, (len(settings['markets']))):
        # Calculate RSI
        out = talib.RSI(CLOSE[:200,i], 14)
        print(settings['markets'][i], len(CLOSE), i, out[14])
        
        
        pos=np.zeros(nMarkets)
        
        
        weights = pos/1
    return weights, settings


def mySettings():
''' Define your trading system settings here '''


settings= {}


# Python
stocksList = ['AAPL', 'ABBV']


settings['markets'] = stocksList
settings['beginInSample'] = '20150110'
settings['endInSample'] = '20180123'
settings['lookback']= 504
settings['budget']= 10**6
settings['slippage']= 0.05


return settings

    
def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    ADX_period = settings['ADX_period']
             
    nMarkets = CLOSE.shape[1]
    
    for market in range(nMarkets):
        end = settings['lookback']
        start = end - (2 * ADX_period)
        calculate_ADX(market, HIGH[start:end,market:market+1], LOW[start:end, market:market+1],CLOSE[start:end, market:market+1], settings, ADX_period)
    
    #execute trades based on tradings strategy
    weights = execute_trade(settings['ADX'], CLOSE, ADX_period,nMarkets)        

    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}

    # Futures Contracts

    settings['markets'] = ['CASH', 'F_AD', 'F_AE', 'F_AH', 'F_AX', 'F_BC', 'F_BG', 'F_BO', 'F_BP', 'F_C',  'F_CA',
                           'F_CC', 'F_CD', 'F_CF', 'F_CL', 'F_CT', 'F_DL', 'F_DM', 'F_DT', 'F_DX', 'F_DZ', 'F_EB',
                           'F_EC', 'F_ED', 'F_ES', 'F_F',  'F_FB', 'F_FC', 'F_FL', 'F_FM', 'F_FP', 'F_FV', 'F_FY',
                           'F_GC', 'F_GD', 'F_GS', 'F_GX', 'F_HG', 'F_HO', 'F_HP', 'F_JY', 'F_KC', 'F_LB', 'F_LC',
                           'F_LN', 'F_LQ', 'F_LR', 'F_LU', 'F_LX', 'F_MD', 'F_MP', 'F_ND', 'F_NG', 'F_NQ', 'F_NR',
                           'F_NY', 'F_O',  'F_OJ', 'F_PA', 'F_PL', 'F_PQ', 'F_RB', 'F_RF', 'F_RP', 'F_RR', 'F_RU',
                           'F_RY', 'F_S',  'F_SB', 'F_SF', 'F_SH', 'F_SI', 'F_SM', 'F_SS', 'F_SX', 'F_TR', 'F_TU',
                           'F_TY', 'F_UB', 'F_US', 'F_UZ', 'F_VF', 'F_VT', 'F_VW', 'F_VX',  'F_W', 'F_XX', 'F_YM',
                           'F_ZQ']

    settings['ADX'] = 0  # set to arbitary 0 
    settings['ADX_period'] = ADX_period
    settings['lookback'] = 2*ADX_period
    settings['budget'] = 10**6
    settings['slippage'] = 0.05

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
