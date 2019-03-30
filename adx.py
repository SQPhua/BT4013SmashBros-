### Quantiacs Trend Following Trading System Example
# import necessary Packages below:
import numpy

def wilder_smooth(prev, curr, adx_period):
    return prev - (prev/(1.0 * adx_period)) + curr

def calculate_TR(prevClose, currHigh, currLow):
    crit1 = currHigh - currLow
    crit2 = abs(currHigh - prevClose)
    crit3 = abs(prevClose - currLow)
#    print("prevClose, currHigh, currLow: ", prevClose, currHigh, currLow)
    return max(crit1,crit2,crit3)

def calculate_DM_plus(currHigh, currLow, prevHigh, prevLow):
    highDiff = currHigh - prevHigh
    if (highDiff<=0):
        return 0
    lowDiff = prevLow - currLow
    if (highDiff > lowDiff):
        return highDiff
    return 0

def calculate_DM_minus(currHigh, currLow, prevHigh, prevLow):
    lowDiff = prevLow - currLow
    if (lowDiff <=0):
        return 0
    highDiff = currHigh - prevHigh
    if (lowDiff > highDiff):
        return lowDiff
    return 0

def calculate_DX(plus, minus):
    return 100.0 * (abs(plus-minus)) / (plus + minus)

def calculate_ADX(market, HIGH, LOW, CLOSE, settings, ADX_period):
    #trade day undefined     
    trade_day = 0  #defined as today 
    tradeDayVals = {}
    
    # True range and directional movements for the current trade day
    tradeDayVals['TR'] = calculate_TR(CLOSE[trade_day-1][0], HIGH[trade_day][0], LOW[trade_day][0])
    tradeDayVals['+DM'] = calculate_DM_plus(HIGH[trade_day][0], LOW[trade_day][0], HIGH[trade_day-1][0], LOW[trade_day-1][0])
    tradeDayVals['-DM'] = calculate_DM_plus(HIGH[trade_day][0], LOW[trade_day][0], HIGH[trade_day-1][0], LOW[trade_day-1][0])
    
    # Wilder smooting techniques to calculate 14 day smoothed true range and directional movements
    if (market not in settings['TR14']): # initialise 
        settings['TR14'][market] = 0        
        settings['+DM14'][market] = 0
        settings['-DM14'][market] = 0
    settings['TR14'][market] = wilder_smooth(settings['TR14'][market], tradeDayVals['TR'],ADX_period)
    settings['+DM14'][market] = wilder_smooth(settings['+DM14'][market], tradeDayVals['+DM'],ADX_period)
    settings['-DM14'][market] = wilder_smooth(settings['-DM14'][market], tradeDayVals['-DM'],ADX_period)        
    

    #Directional Indices for the current trade day 
    tradeDayVals['+DI'] = 100.0 * settings['+DM14'][market] / settings['TR14'][market]
    tradeDayVals['-DI'] = 100.0 * settings['-DM14'][market] / settings['TR14'][market]
    tradeDayVals['DX'] = calculate_DX(tradeDayVals['+DI'], tradeDayVals['-DI'])
    
    # using old ADX
    ADX = ((settings['ADX'] * 13) + tradeDayVals['DX']) / 14 
    print("tradeDayVals['DX'] , ", tradeDayVals['DX'] )
    settings['ADX'] = ADX #update new adx
    return 

def execute_trade(adx, CLOSE, ADX_period,nMarkets):
    
    pos = numpy.zeros(nMarkets)
    fourteenDayAvePrice = numpy.nansum(CLOSE[-ADX_period:, :], axis=0)/ADX_period
    
    if (adx>25):
        if (fourteenDayAvePrice > CLOSE[0,:]) : 
            short = fourteenDayAvePrice > CLOSE[0,:]
            pos[short] = -adx
        else :
            long = fourteenDayAvePrice < CLOSE[0,:]
            pos[long] = adx
        
    weights = pos/numpy.nansum(abs(pos))     
    
    return weights
    
    
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
    # Calculating vals to be saved to Settings
    ADX_period = 14
    settings['TR14'] = {}
    settings['+DM14'] = {}
    settings['-DM14'] = {}
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
