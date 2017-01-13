#!/usr/bin/env python
import datetime

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
# Stock prices range over the past year from January 1, 2016 to January 1, 2017
start = datetime.date(2016, 1, 1)
end = datetime.date(2017, 1, 1)

# Getstock data by its ticker symbol "GOOG"
google = web.DataReader("GOOG", "yahoo", start, end)
twitter = web.DataReader("TWTR", "yahoo", start, end)
paypal = web.DataReader("PYPL", "yahoo", start, end)

# Get larger amount of GOOG data due to rolling average slow start
new_start = datetime.datetime(2010, 1, 1)
google = web.DataReader("GOOG", "yahoo", new_start, end)
# 20-day(one month) moving average for Google data alongside the
# candlestick graph
google["20d"] = np.round(google["Close"].rolling(
    window=20, center=False).mean(), 2)
google["50d"] = np.round(google["Close"].rolling(
    window=50, center=False).mean(), 2)
google["200d"] = np.round(google["Close"].rolling(
    window=200, center=False).mean(), 2)

# Identify when 20day average is below 50day average
google['20d-50d']= google['20d']-google['50d']
#print(google.tail())

# Regime: Difference btw 2 averages
# np.where() is a vector if-else function, where condition is checked for each component of a vector, and the first argument passed is used when the condition holds, and the other passed if it does not
google["Regime"] = np.where(google['20d-50d'] > 0, 1, 0)
# Bullish regimes: 1, Everything else:0 Bearish regimes: -1. To maintain the rest of the vector, the second argument is google["Regime"]
google["Regime"] = np.where(google['20d-50d'] < 0, -1, google["Regime"])
google.loc['2016-01-01':'2017-01-01',"Regime"].plot(ylim=(-2,2)).axhline(y=0, color="black", lw = 2)
#plt.show()
#print(google["Regime"].value_counts())

# To ensure all trades close out, regime of the last row = 0
# google["Signal"]= np.sign(google["Regime"] - google["Regime"].shift(1))
#print(google["Signal"].value_counts())

# Create DataFrame with trades, includin price at trade and regime which trade occurs
google_signals=pd.concat([pd.DataFrame({"Price": google.loc[google["Signal"] == 1, "Close"],
                     "Regime": google.loc[google["Signal"] == 1, "Regime"],
                     "Signal": "Buy"}),
        pd.DataFrame({"Price": google.loc[google["Signal"] == -1, "Close"],
                     "Regime": google.loc[google["Signal"] == -1, "Regime"],
                     "Signal": "Sell"}),
    ])
google_signals.sort_index(inplace = True)
google_signals