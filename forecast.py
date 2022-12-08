import pandas as pd
import io
from statsforecast import StatsForecast
from statsforecast.models import ETS, AutoETS
import datetime 
import matplotlib.pyplot as plt
import seaborn as sns

def clean_data(df):
    # Fill the null values
    df = df.fillna(method='ffill').fillna(method='bfill')

    # Make it a tall-dataframe from a widedataframe
    df = df.melt(id_vars = ["Month"], var_name = "Product", value_name = "y")

    # Make it compatible with ETS
    df['ds'] = df['Month']
    df['unique_id'] = df['Product']
    df.set_index('unique_id', inplace = True)
    df = df.drop(columns = ['Month', 'Product'])

    return df

def forecasting(df, prediction_length = 6, season_length = 12, freq = 'M'):
    models = [AutoETS(season_length = season_length, model = 'ZMZ')]
    model = StatsForecast(df = df, models = models, freq = freq)
    fc = model.forecast(prediction_length)

    # Merging the Predicted Values and Existing values
    df['actual'] = [True]*len(df)
    fc['y'] = fc['AutoETS']
    fc = fc.drop(['AutoETS'], axis = 1)
    fc['actual'] = [False]*len(fc)
    df['ds'] = pd.to_datetime(df['ds'])
    final_df = pd.concat([df, fc])
    final_df['date'] = final_df['ds']
    final_df['price'] = final_df['y']

    return final_df