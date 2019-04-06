import numpy
from pyramid.arima import auto_arima
import time
import pandas as pd

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    
    nMarkets=CLOSE.shape[1]
    period = 10

    CLOSE_df = pd.DataFrame(CLOSE, columns = settings['markets'])
    CLOSE_df = CLOSE_df.fillna(0)
    longEquity = []
    shortEquity = []
    pos=numpy.zeros(nMarkets)

    for future in CLOSE_df.columns:
        future_list = CLOSE_df[future].tolist()

        model = auto_arima(future_list, error_action='ignore', trace=1,
                      seasonal=True, m=12)

        model.fit(future_list)
        future_forecast = model.predict(n_periods=1)

        prediction = future_forecast[0]

        avg = numpy.mean(future_list[-period:])
        std = numpy.std(future_list[-period:])

        if prediction > avg:
            longEquity.append(True)
            shortEquity.append(False)
        elif prediction < avg - std:
        	longEquity.append(False)
        	shortEquity.append(True)
        else:
            longEquity.append(False)
            shortEquity.append(False)

    
    pos[longEquity]=1
    pos[shortEquity]=-1
    weights = pos/numpy.nansum(abs(pos))
    
    return weights, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings= {}


    # Futures Contracts

    settings['markets']  = ['CASH','F_AD','F_BO','F_BP','F_C','F_CC','F_CD',
            'F_CL','F_CT','F_DX','F_EC','F_ED','F_ES','F_FC','F_FV','F_GC',
            'F_HG','F_HO','F_JY','F_KC','F_LB','F_LC','F_LN','F_MD','F_MP',
            'F_NG','F_NQ','F_NR','F_O','F_OJ','F_PA','F_PL','F_RB','F_RU',
            'F_S','F_SB','F_SF','F_SI','F_SM','F_TU','F_TY','F_US','F_W',
            'F_XX','F_YM','F_AX','F_CA','F_DT','F_UB','F_UZ','F_GS','F_LX',
            'F_SS','F_DL','F_ZQ','F_VX','F_AE','F_BG','F_BC','F_LU','F_DM',
            'F_AH','F_CF','F_DZ','F_FB','F_FL','F_FM','F_FP','F_FY','F_GX',
            'F_HP','F_LR','F_LQ','F_ND','F_NY','F_PQ','F_RR','F_RF','F_RP',
            'F_RY','F_SH','F_SX','F_TR','F_EB','F_VF','F_VT','F_VW','F_GD','F_F']


    settings['beginInSample'] = '20170119'
    settings['endInSample']   = '20190331'

    settings['lookback']= 504
    settings['budget']= 10**6
    settings['slippage']= 0.05

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    start_time = time.time()
    results = quantiacsToolbox.runts(__file__)
    indexes = list(map(lambda x: [x], list(range(len(results["stats"])))))
    elapsed_time = time.time() - start_time
    time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    df = pd.DataFrame(results["stats"], index=indexes)
    df.to_csv("G:/Trendfollowing-Sample-Strategy-master/output_autoarima.csv", index=False)