# -*- coding: utf-8 -*-
"""GoldPrice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18sggAKS5PTTQG79jzSZmuiPxQF9lRcus
"""

pip install yfinance

# LinearRegression is a machine learning library for linear regression
from sklearn.linear_model import LinearRegression
# pandas and numpy are used for data manipulation
import pandas as pd
import numpy as np
# matplotlib and seaborn are used for plotting graphs
import matplotlib.pyplot as plt
import seaborn
# fix_yahoo_finance is used to fetch data
import yfinance as yf
import datetime
import warnings
warnings.filterwarnings('ignore')
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

Get_Facebook_information = yf.Ticker("META")
Get_Google_information = yf.Ticker("GOOGL")
Get_Amazon_information = yf.Ticker("AMZN")

print(Get_Facebook_information.info)
print(Get_Google_information.info)

print(Get_Google_information.history(period = "max"))

start_date = datetime.datetime(2004, 8, 19)
end_date = datetime.datetime(2022, 11, 25)

Data_frame = Get_Google_information.history(start = start_date, end = end_date)
print(Data_frame)

Data_frame['Close'].plot(title = "Google's Stock Price")

Data_frame = yf.download("GOOG", start_date, end_date)
print(Data_frame)

Data_frame = yf.download("GLD", start_date, end_date)

print(Data_frame)

Data_frame_closed_price_2D = Data_frame[["Close"]]
print(Data_frame_closed_price_2D.shape)

Data_frame_closed_price = Data_frame[["Close"]]

Data_frame_closed_price["Close"] = Data_frame["Close"]
Data_frame_closed_price["Month"], Data_frame_closed_price["Year"] = Data_frame.index.month, Data_frame.index.year
Data_frame_closed_price["Day"] = Data_frame.index.day
print(Data_frame_closed_price.head())

index_list = []
New_Data_frame = pd.DataFrame()    # create new empty data frame
for index in range(Data_frame_closed_price.shape[0]):
  if Data_frame_closed_price['Year'][index] == 2004:
    if Data_frame_closed_price['Month'][index] == 11 or Data_frame_closed_price['Month'][index] == 12:
      index_list.append(index)
      New_Data_frame = New_Data_frame.append(Data_frame_closed_price.iloc[index,:])

New_Data_frame["Close"].plot(color = "gold" , title = "Gold Price with Custom Year and Month filter")
plt.show()

Data_frame_for_model = Data_frame_closed_price.copy()
Data_frame_for_model['fake_data_3'] = Data_frame_for_model['Close'].rolling(window=3).mean()
Data_frame_for_model['fake_data_9'] = Data_frame_for_model['Close'].rolling(window=9).mean()
Data_frame_for_model['fake_data_21'] = Data_frame_for_model['Close'].rolling(window=21).mean()
Data_frame_for_model['Next_day_price'] = Data_frame_for_model['Close'].shift(-1)
Data_frame_for_model[:15]



Data_frame_for_model = Data_frame_for_model.dropna()
Data_frame_for_model.head()

X_data = Data_frame_for_model[["fake_data_3", "fake_data_9", "fake_data_21"]]
y_data = Data_frame_for_model['Next_day_price']
X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, test_size=0.2)
print(f"Shape of X train: {X_train.shape} \nShape of y train: {y_train.shape}")
print(f"Shape of X val: {X_val.shape} \nShape of y val:{y_val.shape}")

linear_reg = LinearRegression()
linear_reg.fit(X_train,y_train)
print("R2Score for Training", linear_reg.score(X_train, y_train))

y_pred = linear_reg.predict(X_val)

print("R2Score for testing", r2_score(y_val, y_pred))
print("MAE:", mean_absolute_error(y_val, y_pred))
print("MSE:", mean_squared_error(y_val, y_pred))

y_pred_df = pd.DataFrame(y_pred, index = y_val.index, columns=['Predicted Price'])
y_pred_df.plot(figsize=(15, 6))
y_val.plot(label = "Actual Price")
plt.legend()
plt.title("Gold ETF Price Predicitons")
plt.ylabel("Gold ETF Price")
plt.ylabel("Dates")
plt.xticks(rotation = "horizontal")
plt.show()

# import datetime and get today's date
current_date = datetime.datetime.now()
print("Current Date:", current_date)

data = yf.download('GLD', '2022-10-01', current_date, auto_adjust=True)
print(data[-5:])
print("Shape of test data frame", data.shape)


data['fake_data_3'] = data['Close'].rolling(window=3).mean()
data['fake_data_9'] = data['Close'].rolling(window=9).mean()
data['fake_data_21'] = data['Close'].rolling(window=21).mean()
data = data.dropna()

X_test = data[['fake_data_3', 'fake_data_9', 'fake_data_21']]
data['Predicted_gold_price'] = linear_reg.predict(X_test)

data["Predicted_gold_price"].tail()

data['Signal'] = np.where(data["Predicted_gold_price"].shift(1) < data["Predicted_gold_price"],"Buy","No Position")
data.tail(1)[['Signal','Predicted_gold_price']].T

y_test = data["Close"]
y_pred = data["Predicted_gold_price"]

y_pred.plot(label = "Predicted Price", figsize=(15, 6))
y_test.plot(label = "Actual Price")
plt.legend()
plt.title("Gold ETF Price Predicitons")
plt.ylabel("Gold ETF Price")
plt.xlabel("Dates")
plt.xticks(rotation = "horizontal")
plt.show()