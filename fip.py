### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy as np
import pandas as pd
import datetime
################################# MY FUNCTIONS #################################

def toDate(x):
    return datetime.datetime(int(str(x)[:4]), int(str(x)[4:6]), int(str(x)[6:8]))
#def calcMom(array_like):
#    return (10*math.log10((sum([10**(i/10) for i in array_like])))))
    

def calcMom(arr):
    mom = np.prod(arr) -1
    return mom 
def calcNeg(arr):
    
    return sum(arr<0)/len(arr)
def calcPos(arr):
    return sum(arr>0)/len(arr)
def preprocess_data(DATE,CLOSE,nMarkets):
    """
    Returns a prerpocessed data for the selected pair	
    """
    data = pd.DataFrame({'DATE' : DATE}) # ... create dataframe with the pair of assets, Num rows based on lookback
    data['DATE'] = data['DATE'].apply(toDate)
    data = data.set_index('DATE')
    
    
#    data['Month'] = str(data['DATE'][:4]) + "_" + str(data['DATE'][4:6])
    
    for mark in range(nMarkets):
        name = "market_" + str(mark)
        data[name] = CLOSE[:,mark]
        
    
    dataRaw = data.pct_change()
    data = data.resample("M").mean()
    
    for mark in range(nMarkets):
        name = "market_" + str(mark)
        updatedName = name + "_1+Ret"
        data[updatedName] = data[name] + 1
#        data = data.resample('Y').agg({ updatedName :'mean'})
#        data[updatedName + "_Momentum"] = data.resample("A").mean()  
        
    data = data.resample("Y").apply(calcMom)   
    
    return dataRaw, data

def calcFIP(dataRaw, data,nMarkets):
    for mark in range(nMarkets):
        name = "market_" + str(mark) 
        rets = dataRaw[name]
        mom = data[name +"_1+Ret" ].tail()[0]
        pctNegative = calcNeg(rets)
        pctPositive = calcPos(rets)
        fip = (pctNegative - pctPositive)
        if (mom<0):
            fip = fip * -1
        data['fip_' + str(mark)] = fip
    return data


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''
    nMarkets = CLOSE.shape[1]
    pos = np.zeros(nMarkets)
#    dateVal = toDate(DATE[-1]).day #.month or .year
    dataRaw, data = preprocess_data(DATE,CLOSE,nMarkets)
#    print(data.groupby('MONTH')['market_1'].mean())
#    print(data.resample("M").count())
    
    dataFIP = calcFIP(dataRaw,data, nMarkets)
    cols = range(nMarkets*2)
    newDf = dataFIP.drop(dataFIP.columns[cols], axis=1)
        
    lowest = np.argsort(np.array(newDf.tail()))[:5]
#    print(newDf, lowest)
    for i in lowest:
        pos[i] = 1 
        
#    periodLonger = 200
#    periodShorter = 40
#
#    # Calculate Simple Moving Average (SMA)
#    smaLongerPeriod = np.nansum(CLOSE[-periodLonger:, :], axis=0)/periodLonger
#    smaShorterPeriod = np.nansum(CLOSE[-periodShorter:, :], axis=0)/periodShorter
#
#    longEquity = smaShorterPeriod > smaLongerPeriod
#    shortEquity = ~longEquity
#

#    pos[longEquity] = 1
#    pos[shortEquity] = -1

    weights = pos/np.nansum(abs(pos))

    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}
    # Futures Contracts

    settings['markets'] = ['CASH','F_AD','F_BO','F_BP','F_C','F_CC','F_CD','F_CL','F_CT','F_DX','F_EC','F_ED','F_ES','F_FC','F_FV','F_GC','F_HG','F_HO','F_JY','F_KC','F_LB','F_LC','F_LN','F_MD','F_MP','F_NG','F_NQ','F_NR','F_O','F_OJ','F_PA','F_PL','F_RB','F_RU','F_S','F_SB','F_SF','F_SI','F_SM','F_TU','F_TY','F_US','F_W','F_XX','F_YM','F_AX','F_CA','F_DT','F_UB','F_UZ','F_GS','F_LX','F_SS','F_DL','F_ZQ','F_VX','F_AE','F_BG','F_BC','F_LU','F_DM','F_AH','F_CF','F_DZ','F_FB','F_FL','F_FM','F_FP','F_FY','F_GX','F_HP','F_LR','F_LQ','F_ND','F_NY','F_PQ','F_RR','F_RF','F_RP','F_RY','F_SH','F_SX','F_TR','F_EB','F_VF','F_VT','F_VW','F_GD','F_F']
    settings['lookback'] = 504
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['beginInSample'] = '20170112'
    settings['endInSample'] = '20190331'

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
