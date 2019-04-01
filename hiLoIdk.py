### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, OI, settings):
    '''The contract is defined as the high- (low-) volume contract 
    if the contract's volume changes between period from t-1 to t 
    and period from t-2 to t-1 is above (below) the median volume
    change of all contracts (weekly trading volume is detrended by 
    dividing the trading volume by its sample mean to make the volume 
    measure comparable across markets).
    
    All contracts are also assigned to either high-open interest 
    (top 50% of changes in open interest) or low-open interest groups 
    (bottom 50% of changes in open interest) based on lagged changes 
    in open interest between period from t-1 to t and period from t-2 to t-1. 
    
    The investor goes long (short) on futures from the high-volume, 
    low-open interest group with the lowest (greatest) returns in the previous week. 
    
    The weight of each contract is proportional to the difference between the return 
    of the contract over the past 1 week and the equal-weighted average of returns 
    on the N (number of contracts in group) contracts during that period.'''
    
    period = 7 #weekly
    lag = 1
    #find top vol over period of 12 year and return corresponding market
    
    nMarkets = len(settings['markets'])
    pos = np.zeros((1, nMarkets), dtype=np.float)
    
    # if volume of that market is the top 3, long it 
    latestVol = VOL[-period:, :]
    #find average volume over 12 mth per market
    aveVol = np.mean(latestVol,axis=0) # list of nMaekts with average over prev 7 days 
    
    firstLagVol = VOL[-lag:, :] #t-1 to t    
    secondLagVol = VOL[-2*lag:-lag,:] #t-2 to t-1
    
    firstLagOi = OI[-lag:,:]
    secondLagOi = OI[-2*lag:-lag,:]
    OiDiff = np.diff([firstLagOi,secondLagOi],axis=0)[0] #1 x nmarkets matrix

    #find top 50% diffs
    top50Diff = OiDiff[0].argsort()[-int(nMarkets*0.5):][::-1]    #list 44 markets (top 50)
    bot50Diff = ~top50Diff 
    
    settings["topOI"] = top50Diff
    settings["botOI"] = bot50Diff
    
#    settings["highContract"] = [] #clear old list 
#    settings["lowContract"].
    highContract = [] #initialise
    lowContract = []
    for market in range(nMarkets):

#        print("First Second Ave VOL ", firstLag[0,market], secondLag[0,market], aveVol[market], market )
        if (firstLagVol[0,market] > aveVol[market] and secondLagVol[0,market] > aveVol[market]):
#            settings["highContract"].append(market)
            highContract.append(market)
        else:
#           settings["lowContract"].append(market) 
            lowContract.append(market)
    #check if high contract in top OI , if yes, long, else short
    #def Long E and Short E
    '''    The investor goes long (short) on futures from the high-volume, 
    low-open interest group with the lowest (greatest) returns in the previous week. '''
    
    #check if high contract in top50 diff
#    top50Diff 
    marketsLong = list(set(highContract).intersection(top50Diff))
    marketsShort = list(set(lowContract).intersection(bot50Diff))
    
    for marketL in marketsLong:
        lowestRet = np.nanmin(CLOSE[-period:, marketL])
        pos[0,marketL] = lowestRet
        
    for marketS in marketsShort:
        highestRet = np.nanmax(CLOSE[-period:, marketS])    
        pos[0,marketS] = highestRet     
            
    weights = pos/np.nansum(abs(pos))
    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}

    settings['markets'] = ['CASH','F_AD','F_BO','F_BP','F_C','F_CC','F_CD','F_CL','F_CT','F_DX','F_EC','F_ED','F_ES','F_FC','F_FV','F_GC','F_HG','F_HO','F_JY','F_KC','F_LB','F_LC','F_LN','F_MD','F_MP','F_NG','F_NQ','F_NR','F_O','F_OJ','F_PA','F_PL','F_RB','F_RU','F_S','F_SB','F_SF','F_SI','F_SM','F_TU','F_TY','F_US','F_W','F_XX','F_YM','F_AX','F_CA','F_DT','F_UB','F_UZ','F_GS','F_LX','F_SS','F_DL','F_ZQ','F_VX','F_AE','F_BG','F_BC','F_LU','F_DM','F_AH','F_CF','F_DZ','F_FB','F_FL','F_FM','F_FP','F_FY','F_GX','F_HP','F_LR','F_LQ','F_ND','F_NY','F_PQ','F_RR','F_RF','F_RP','F_RY','F_SH','F_SX','F_TR','F_EB','F_VF','F_VT','F_VW','F_GD','F_F']
    
    settings["highContract"] = []
    settings["lowContract"] = []
    settings["topOI"] = None
    settings["topOI"] = None 
    settings['lookback'] = 504
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['beginInSample'] = '20150506'
    settings['endInSample'] = '20180506'

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)

