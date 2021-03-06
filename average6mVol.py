### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, settings):

    period = int(365/2)
    #find top vol over period of 1/2 year and return corresponding market
    
    nMarkets = len(settings['markets'])
    pos = np.zeros((1, nMarkets), dtype=np.float)

    latestVol = VOL[-period:, :]
    #find average volume over 6 mth per market
    aveVol = np.mean(latestVol,axis=0) # list of nMaekts with average over prev days 
    
    #find average volume over 6 mth per market s
    aveVol = np.mean(latestVol,axis=0) # list of nMaekts with average over prev days 
    longE = np.where(aveVol == np.nanmax(aveVol))
    shortE = np.where(aveVol == np.nanmin(aveVol))

    pos[0,longE[0]] = 1
    pos[0,shortE[0]] = -1
    
    weights = pos/np.nansum(abs(pos))
    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}

    settings['markets'] = ['CASH','F_AD','F_BO','F_BP','F_C','F_CC','F_CD','F_CL','F_CT','F_DX','F_EC','F_ED','F_ES','F_FC','F_FV','F_GC','F_HG','F_HO','F_JY','F_KC','F_LB','F_LC','F_LN','F_MD','F_MP','F_NG','F_NQ','F_NR','F_O','F_OJ','F_PA','F_PL','F_RB','F_RU','F_S','F_SB','F_SF','F_SI','F_SM','F_TU','F_TY','F_US','F_W','F_XX','F_YM','F_AX','F_CA','F_DT','F_UB','F_UZ','F_GS','F_LX','F_SS','F_DL','F_ZQ','F_VX','F_AE','F_BG','F_BC','F_LU','F_DM','F_AH','F_CF','F_DZ','F_FB','F_FL','F_FM','F_FP','F_FY','F_GX','F_HP','F_LR','F_LQ','F_ND','F_NY','F_PQ','F_RR','F_RF','F_RP','F_RY','F_SH','F_SX','F_TR','F_EB','F_VF','F_VT','F_VW','F_GD','F_F']
    
    # create a dictionary to store momentum indicators for all symbols 
    settings['lookback'] = 504
    settings['budget'] = 10**6
    settings['slippage'] = 0.05]    
    settings['beginInSample'] = '20170119'
    settings['endInSample']   = '20190331' #testing date
    #settings['beginInSample'] = '20161019'
    #settings['endInSample']   = '20181231' 

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)

