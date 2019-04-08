# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 14:42:26 2019

@author: Xian Liang
"""

### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL,exposure, equity, settings,OI):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    nMarkets=CLOSE.shape[1]
    
    periodLonger=300 #%[280:30:500]#
    maxminPeriod=60 
    price_min = np.nanmin(CLOSE[-maxminPeriod,:],axis=0)
    price_max = np.nanmax(CLOSE[-maxminPeriod,:])
    pos = np.zeros((1, nMarkets), dtype=np.float)
    diff = price_max - price_min
    
    
    extremeRange = price_max - price_min
    hundred = extremeRange - price_min
    up_level1 = price_max - 0.236 * diff
    up_level2 = price_max - 0.382 * diff
    up_level3 = price_max - 0.618 * diff

    
    hundred_down = extremeRange + price_min
    down_level1 = price_min + 0.236 * diff
    down_level2 = price_min + 0.382 * diff
    down_level3 = price_min + 0.618 * diff

    
    for market in range(nMarkets):

        
        smaLongerPeriod = np.sum(CLOSE[-periodLonger:,market])/periodLonger
        
        currentPrice = CLOSE[-1, market]

        if currentPrice > smaLongerPeriod and currentPrice<hundred:
            pos[0, market] = -1
        elif currentPrice > smaLongerPeriod and currentPrice<up_level3:
            pos[0, market] = -0.6           
        elif currentPrice > smaLongerPeriod and currentPrice<up_level2:
            pos[0, market] = -0.5
        elif currentPrice > smaLongerPeriod and currentPrice<up_level1:
            pos[0, market] = -0.3
        else:
            if currentPrice < smaLongerPeriod and currentPrice>hundred_down:
                pos[0, market] = 1
            elif currentPrice < smaLongerPeriod and currentPrice>down_level3:
                pos[0, market] = 0.6           
            elif currentPrice < smaLongerPeriod and currentPrice>down_level2:
                pos[0, market] = 0.5
            elif currentPrice < smaLongerPeriod and currentPrice>down_level1:
                pos[0, market] = 0.3



    weights = pos/np.nansum(abs(pos))

    return (weights, settings)

def mySettings():
    ''' Define your trading system settings here '''

    settings= {}


    # Futures Contracts

    settings['markets']  = ['CASH','F_AD','F_BO','F_BP','F_C','F_CC','F_CD','F_CL','F_CT','F_DX',
                   'F_EC','F_ED','F_ES','F_FC','F_FV','F_GC','F_HG','F_HO','F_JY',
                   'F_KC','F_LB','F_LC','F_LN','F_MD','F_MP','F_NG','F_NQ','F_NR',
                   'F_O','F_OJ','F_PA','F_PL','F_RB','F_RU','F_S','F_SB','F_SF',
                   'F_SI','F_SM','F_TU','F_TY','F_US','F_W','F_XX','F_YM','F_AX',
                   'F_CA','F_DT','F_UB','F_UZ','F_GS','F_LX','F_SS','F_DL','F_ZQ',
                   'F_VX','F_AE','F_BG','F_BC','F_LU','F_DM','F_AH','F_CF','F_DZ','F_FB',
                   'F_FL','F_FM','F_FP','F_FY','F_GX','F_HP','F_LR','F_LQ','F_ND','F_NY',
                   'F_PQ','F_RR','F_RF','F_RP','F_RY','F_SH','F_SX','F_TR','F_EB','F_VF',
                   'F_VT','F_VW','F_GD','F_F']

    settings['beginInSample'] = '20170119'
    settings['endInSample']   = '20190331' #testing date
    #settings['beginInSample'] = '20161019'
    #settings['endInSample']   = '20181231' 


    settings['lookback']= 504 
    settings['budget']= 10**6
    settings['slippage']= 0.05


    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    from quantiacsToolbox import optimize
    #optimize()
    results = quantiacsToolbox.runts(__file__)
    
    
    

