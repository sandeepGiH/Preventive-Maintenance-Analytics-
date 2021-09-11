import pandas as pd
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset


#import os
#df = pd.read_csv(os.getcwd() + os.path.sep + "Beverage.csv")


def preprocess_data(df):
    df.drop(['Unnamed: 0','Co2', 'Date_coder', 'Day', 'Hour', 'Month', 'PSP', 'Palletizer', 'Plasmax', 'Preform', 'Uday', 'Week', 'Year', 'product', 'Filler'], axis = 1, inplace = True)
    df['time'] = pd.to_datetime(df['time'], format= "%Y-%m-%d %H:%M:%S")
    df.index = df['time']
    df1 = df.resample('H').sum()
    df1['Blower'] = df1['Blower'].apply(lambda x: x/2 if x>=36000 else x)
    return df1

#df = preprocess_data(df)


def forecast(df, equipment_name, forecast_time):
    # SARIMAX
    
    model = sm.tsa.statespace.SARIMAX(df[equipment_name],
                                      order = (1, 1, 1),
                                      seasonal_order = (1, 1, 1, 24),
                                      enforce_stationarity = False,
                                      enforce_invertibility = False)
    model_fit = model.fit()  
    print("Model AIC:  ", model_fit.aic)
    
    future_dates = [df.index[-1] + DateOffset(hours = x) for x in range(0, forecast_time)]
    future_dates = pd.DataFrame(index = future_dates[1:], columns = [(equipment_name + ' Forecast')])
    f_df = pd.concat([df, future_dates])
    f_df[(equipment_name + ' Forecast')] = model_fit.predict(start = future_dates.index[0],
                                                      end = future_dates.index[-1],
                                                      dynamic= True)
    f_df = f_df.fillna("")
    return f_df

#dataframe = forecast(df, equipment_name = 'Labeller', forecast_time = 24)
#equipment_name = 'Labeller'
#forecast_time = 8
