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

#    for mark in newTop3:
#        pos[0,mark] = 1
#        
#    for mark in newBot3:
#        pos[0,mark] = -1 
        
    weights = pos/np.nansum(abs(pos))
    return weights, pos

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, settings):
    ''' Go long 3 currencies with strongest 12 month momentum against USD and
    go short 3 currencies with lowest 12 month momentum against USD. 
    Cash not used as margin invest on overnight rates. Rebalance monthly.'''
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
    
    
#    #find average volume over 12 mth per market
#    aveVol = np.mean(latestVol,axis=0) # list of nMaekts with average over prev 365 days 
#    longE = np.where(aveVol == np.nanmax(aveVol))
#    shortE = np.where(aveVol == np.nanmin(aveVol))
        
        
#    latestVol = VOL[-1:,:] #latest volume for all market [2D Matrix]
#    longE = numpy.where(latestVol[0] == numpy.nanmax(latestVol)) #get index of highest market
#    shortE = numpy.where(latestVol[0] == numpy.nanmin(latestVol))
#    pos[0,longE[0]] = 1
#    pos[0,shortE[0]] = -1
    

    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}

    settings['markets'] = ['CASH', 'F_AD', 'F_AE', 'F_AH','F_GX', 'F_HG', 'F_HO']
    
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

