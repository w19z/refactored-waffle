import mlflow
import pandas as pd
import numpy as np
from sktime.performance_metrics.forecasting import  MeanAbsolutePercentageError, MeanSquaredError
from sktime.forecasting.fbprophet import Prophet
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.utils import mlflow_sktime 


smape = MeanAbsolutePercentageError(symmetric = True)


file = '/opt/apps/eda/data/combined.csv'
df = pd.read_csv(file, index_col='Date', parse_dates=True)

mlflow.set_tracking_uri("http://127.0.0.1:5000")

y_train, y_test = temporal_train_test_split(df['Adj Close'])


forecaster = Prophet(freq='1d',
                    seasonality_mode='additive',
                     n_changepoints=int(len(df) / 12),
                     add_country_holidays={'country_name': 'USA'},
                     weekly_seasonality=True,
                     )

forecaster.fit(y_train)
fh = ForecastingHorizon(y_test.index, is_relative=False)
y_pred = forecaster.predict(fh)



score = smape(y_pred.values, y_test.values)

with mlflow.start_run():
    mlflow.sklearn.log_model(forecaster, "prophet")
    mlflow.log_metric("symmetric_mean_absolute_percentage_error", score)
    mlflow_sktime.save_model(
        sktime_model=forecaster,
        path="models/prophet/run_2")


fh = pd.date_range(start='2023-11-1', periods=5, freq='B')
data = pd.DataFrame(forecaster.predict(fh))
data['date'] = data.index
data['symbol'] = 'AAPL'
data['close_price'] = data['Adj Close']
data.drop('Adj Close', axis=1, inplace=True)
data.to_csv('models/prophet/run_2/predicted.csv', index=False)