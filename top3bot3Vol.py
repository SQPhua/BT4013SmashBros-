### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np

def rebalance(pos,newTop3,newBot3,settings):
    #get curr list 
    currTopList = settings["topList"]
    currBotList = settings["botList"]
    
    #check TopList first
    newMarketsTop = np.where(currTopList != newTop3)[0] #returns indices of new market
    if (len(newMarketsTop) != 0): #new markets added
        for markInd in newMarketsTop:
            pos[0, newTop3[markInd]] = 1 #long new added 
            pos[0, currTopList[markInd]] = -1 #short old 
            settings["topList"] = newTop3 #replace list

    #check BotList next
    newMarketsBot = np.where(currBotList != newBot3)[0] #returns indices of new market
    if (len(newMarketsBot) != 0): #new markets added
        for markInd in newMarketsBot:
            pos[0, newBot3[markInd]] = 1 #long new added 
            pos[0, currBotList[markInd]] = -1 #short old 
            settings["botList"] = newBot3 #replace list

    weights = pos/np.nansum(abs(pos))
    return weights, pos

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, settings):
    ''' Go long 3 currencies with strongest 12 month momentum against USD and
    go short 3 currencies with lowest 12 month momentum against USD. 
    Cash not used as margin invest on overnight rates. Rebalance DAILY.'''
    period = int(365/2)
    #find top vol over period of 12 year and return corresponding market
    
    nMarkets = len(settings['markets'])
    pos = np.zeros((1, nMarkets), dtype=np.float)
    
    # if volume of that market is the top 3, long it 
    latestVol = VOL[-period:, :]
    #find average volume over 12 mth per market
    aveVol = np.mean(latestVol,axis=0) # list of nMaekts with average over prev 365 days 
    newTop3 = aveVol.argsort()[-3:][::-1]
    newBot3 = aveVol.argsort()[:3]
    
    weights, pos = rebalance(pos,newTop3,newBot3, settings) 

    return weights, settings

def mySettings():
    ''' Define your trading system settings here '''

    settings = {}

    settings['markets'] = ['CASH','F_AD','F_BO','F_BP','F_C','F_CC','F_CD','F_CL','F_CT','F_DX','F_EC','F_ED','F_ES','F_FC','F_FV','F_GC','F_HG','F_HO','F_JY','F_KC','F_LB','F_LC','F_LN','F_MD','F_MP','F_NG','F_NQ','F_NR','F_O','F_OJ','F_PA','F_PL','F_RB','F_RU','F_S','F_SB','F_SF','F_SI','F_SM','F_TU','F_TY','F_US','F_W','F_XX','F_YM','F_AX','F_CA','F_DT','F_UB','F_UZ','F_GS','F_LX','F_SS','F_DL','F_ZQ','F_VX','F_AE','F_BG','F_BC','F_LU','F_DM','F_AH','F_CF','F_DZ','F_FB','F_FL','F_FM','F_FP','F_FY','F_GX','F_HP','F_LR','F_LQ','F_ND','F_NY','F_PQ','F_RR','F_RF','F_RP','F_RY','F_SH','F_SX','F_TR','F_EB','F_VF','F_VT','F_VW','F_GD','F_F']
    
    # create a dictionary to store momentum indicators for all symbols 
    #initialise top3 and bot3 list
    settings['topList'] = [0,0,0]
    settings['botList'] = [0,0,0]    
    settings['lookback'] = 504
    settings['budget'] = 10**6
    settings['slippage'] = 0.05

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)

