from pos_sistem.modules.ml.data_loader import load_data
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
#from pmdarima import auto_arima

def get_daily_sales():
    """
    Consulta las ventas diarias y llena los días sin ventas con cero.
    """
    query = """
        SELECT DATE(created_at) AS sale_date, SUM(total) AS total_sales
        FROM sales
        GROUP BY DATE(created_at)
        ORDER BY sale_date
    """
    df = load_data(query)
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df.set_index('sale_date', inplace=True)
    df = df.asfreq('D')  # Asegura frecuencia diaria
    df['total_sales'] = df['total_sales'].fillna(0)  # Llena días vacíos
    return df

def train_arima_model(df):
    """
    Entrena un modelo ARIMA (p=5, d=1, q=0) sobre la serie temporal.
    """
    model = ARIMA(df['total_sales'], order=(5, 1, 0))  # Puedes ajustar (p,d,q)
    model_fit = model.fit()
    return model_fit

def predict_future_sales_arima(model_fit, df, days=7):
    """
    Genera predicción para una cantidad de días futuros.
    """
    forecast = model_fit.forecast(steps=days)
    future_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=days, freq='D')
    future_df = pd.DataFrame({'predicted_sales': forecast}, index=future_index)
    return future_df
# from pmdarima import auto_arima

# def train_arima_model(df):
#     model = auto_arima(df['total_sales'], seasonal=False, stepwise=True, suppress_warnings=True)
#     return model
