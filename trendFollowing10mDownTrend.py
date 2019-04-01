### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np

def diffPct(close,ave): 
    pct = float((ave-close)/ave)
    return pct

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    nMarkets = CLOSE.shape[1]
    pos = np.zeros(nMarkets)
    periodLonger = int(365/12) * 10 # 10 months
    # Calculate Simple Moving Average (SMA)
    smaLongerPeriod = np.nansum(CLOSE[-periodLonger:, :], axis=0)/periodLonger # 1D list of sma for 89 markets

    periodShort= int(365/12) * 1 # 1
    # Calculate Simple Moving Average (SMA)
    smaDown = np.nansum(CLOSE[-periodShort:, :], axis=0)/periodShort # 1D list of sma for 89 markets
    
    for mark in range(nMarkets): #try range of down if at least decrease by 5% 
        difference = diffPct(CLOSE[-1: , mark],smaDown[mark])
        if (difference > 0.05): #how to pred a very sharp drop  in close price? 
            pos[mark] = -1
        elif (CLOSE[-1: , mark] > smaLongerPeriod[mark]) and (CLOSE[-2:-1, mark] > smaLongerPeriod[mark]):
            pos[mark] = 1

            
#    longEquity = CLOSE[-1] > smaLongerPeriod
#    shortEquity = ~longEquity

#    pos[longEquity] = 1
#    pos[shortEquity] = -1

    weights = pos/np.nansum(abs(pos))

    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}

    # Futures Contracts
    futuresList = ['CASH','F_AD','F_BO','F_BP','F_C','F_CC','F_CD','F_CL','F_CT','F_DX','F_EC','F_ED','F_ES','F_FC','F_FV','F_GC','F_HG','F_HO','F_JY','F_KC','F_LB','F_LC','F_LN','F_MD','F_MP','F_NG','F_NQ','F_NR','F_O','F_OJ','F_PA','F_PL','F_RB','F_RU','F_S','F_SB','F_SF','F_SI','F_SM','F_TU','F_TY','F_US','F_W','F_XX','F_YM','F_AX','F_CA','F_DT','F_UB','F_UZ','F_GS','F_LX','F_SS','F_DL','F_ZQ','F_VX','F_AE','F_BG','F_BC','F_LU','F_DM','F_AH','F_CF','F_DZ','F_FB','F_FL','F_FM','F_FP','F_FY','F_GX','F_HP','F_LR','F_LQ','F_ND','F_NY','F_PQ','F_RR','F_RF','F_RP','F_RY','F_SH','F_SX','F_TR','F_EB','F_VF','F_VT','F_VW','F_GD','F_F']

    settings['markets'] = futuresList

    settings['lookback'] = int(365/12) * 10
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['beginInSample'] = '20070101'
    settings['endInSample'] = '20081231'

    return settings


# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)