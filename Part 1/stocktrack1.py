#!/usr/bin/env python
import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator, date2num
from matplotlib.finance import candlestick_ohlc

# Stock prices range over the past year from January 1, 2016 to January 1, 2017
start = datetime.date(2016, 1, 1)
end = datetime.date(2017, 1, 1)

# Getstock data by its ticker symbol "GOOG"
google = web.DataReader("GOOG", "yahoo", start, end)
twitter = web.DataReader("TWTR", "yahoo", start, end)
paypal = web.DataReader("PYPL", "yahoo", start, end)

#google.plot(grid=True)

# Create a DataFrame consisting of the adjusted closing price of
# these stocks, first by making a list of these objects and using the join
# method
stocks = pd.DataFrame({"TWTR": twitter["Adj Close"],
                       "PYPL": paypal["Adj Close"],
                       "GOOG": google["Adj Close"]})

print(stocks.head())

# df.apply(arg) will apply the function arg to each column in df, and return a DataFrame with the result
# stock return is price at current time over price at the beginning
stock_return = stocks.apply(lambda x: x / x[0])
#stock_return.plot(grid= True).axhline(y=1, color ="black", lw=2)
# plt.show()


def pandas_candlestick_ohlc(dat, stick="day", otherseries=None):
    """
    :param dat: pandas DataFrame object with datetime64 index, and float columns "Open", "High", "Low", and "Close", likely created via DataReader from "yahoo"
    :param stick: A string or number indicating the period of time covered by a single candlestick. Valid string inputs include "day", "week", "month", and "year", ("day" default), and any numeric input indicates the number of trading days included in a period
    :param otherseries: An iterable that will be coerced into a list, containing the columns of dat that hold other series to be plotted as lines

    This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
    """
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    dayFormatter = DateFormatter('%d')      # e.g., 12

    # Create a new DataFrame which includes OHLC data for each period
    # specified by stick input
    transdat = dat.loc[:, ["Open", "High", "Low", "Close"]]
    if isinstance(stick, str):
        if stick == "day":
            plotdat = transdat
            stick = 1  # Used for plotting
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(
                    lambda x: x.isocalendar()[1])  # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(
                    lambda x: x.month)  # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(
                lambda x: x.isocalendar()[0])  # Identify years
            # Group by year and other appropriate variable
            grouped = transdat.groupby(list(set(["year", stick])))
            # Create empty data frame containing what will be plotted
            plotdat = pd.DataFrame(
                {"Open": [], "High": [], "Low": [], "Close": []})
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0, 0],
                                                       "High": max(group.High),
                                                       "Low": min(group.Low),
                                                       "Close": group.iloc[-1, 3]},
                                                      index=[group.index[0]]))
            if stick == "week":
                stick = 5
            elif stick == "month":
                stick = 30
            elif stick == "year":
                stick = 365

    elif (isinstance(stick,int) and stick >= 1):
        transdat["stick"] = [np.floor(i / stick)
                             for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        # Create empty data frame containing what will be plotted
        plotdat = pd.DataFrame(
            {"Open": [], "High": [], "Low": [], "Close": []})
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0, 0],
                                                   "High": max(group.High),
                                                   "Low": min(group.Low),
                                                   "Close": group.iloc[-1, 3]},
                                                  index=[group.index[0]]))

    else:
        raise ValueError(
            'Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)

    ax.grid(True)

    # Create the candlestick chart
    candle_list = list(zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                           plotdat["Low"].tolist(), plotdat["Close"].tolist()))
    candlestick_ohlc(ax, candle_list, colorup="black",
                     colordown="red", width=stick * .4)

    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:, otherseries].plot(ax=ax, lw=1.3, grid=True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(),
             rotation=45, horizontalalignment='right')

    plt.show()
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
pandas_candlestick_ohlc(
    google.loc['2016-01-04':'2017-01-02', :], otherseries=["20d", "50d", "200d"])
