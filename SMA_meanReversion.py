### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy
import statistics 


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, 	OI,exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''
    nMarkets=CLOSE.shape[1]

    periodLonger=340 #%[220:30:360]#
    
    pos = numpy.zeros((1, nMarkets), dtype=numpy.float)
    for market in range(nMarkets):
        
        # Calculate Simple Moving Average (SMA)
        smaLongerPeriod = numpy.sum(CLOSE[-periodLonger:,market])/periodLonger

        smaVar = statistics.stdev(CLOSE[-periodLonger:, market])
    
        pastPrice= CLOSE[-periodLonger,market]
        currentPrice = CLOSE[-1, market]       
        
        if currentPrice<pastPrice:
            if currentPrice < smaLongerPeriod:
                pos[0, market] = 1
            elif currentPrice < smaLongerPeriod - smaVar:
                pos[0, market] = 0.75
        elif currentPrice > pastPrice:
            if currentPrice > smaLongerPeriod:
                pos[0, market] = -1
            elif currentPrice > smaLongerPeriod + smaVar:
                pos[0, market] = -0.55

    

    #weights = pos/numpy.nansum(abs(pos))

    return pos, settings


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
    settings['endInSample']   = '20190331'#testing date
    #settings['beginInSample'] = '20161019'
    #settings['endInSample']   = '20181231' 

    settings['lookback']= 504
    settings['budget']= 10**6
    settings['slippage']= 0.05

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    #from quantiacsToolbox import optimize
    #optimize()
    results = quantiacsToolbox.runts(__file__)

