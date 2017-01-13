#Introduction to Stock Market Data Analysis with Python
##Part 2

###Referenced from this [blogpost](https://ntguardian.wordpress.com/2016/09/26/introduction-stock-market-data-python-2/)

##Introduction

This portion covers trading strategies using moving averages and exit strategies adopted for a trading position. The evaluation of a strategy is also elaborated by the use of backtesting. 

##Trading strategy

**Open position**: A trade that will be terminated in the future when a condition is met. 
**Long position**: A position where a profit is made if the financial instrument traded increases in value
**Short position**: A position where a profit is made if the financial asset being traded decreases in value. 
When trading stocks directly, all long positions are bullish and all short position are bearish. However, a bullish attitude need not be accompanied by a long position, and a bearish attitude need not be accompanied by a short position (Which is particularly true when trading stock options).

For instance: If you buy a stock expecting the stock will increase in value, and plan to sell the stock at a higher price. This is a long position: you are holding a financial asset for which you will profit if the asset increases in value. Your potential profit is unlimited, and your potential losses are limited by the price of the stock since stock prices never go below zero. 
On the other hand, if you expect a stock to decrease in value, you may borrow the stock from a brokerage firm and sell it, with the expectation of buying the stock back later at a lower price, thus earning you a profit. This is called **shorting a stock**, and is a short position, since you will earn a profit if the stock drops in value. The potential profit from shorting a stock is limited by the price of the stock (the best you can do is have the stock become worth nothing;you buy it back for free), while the losses are unlimited, since you could potentially spend a large amount of money just to buy the stock back.

A set of rules determining the amount of money to bet on any single trade must be in place. For example, a trader may decide that no more than 10% of her portfolio would be bet on a trade. Additionally, in any trade, a trader must have an **exit strategy**, a set of conditions determining the exit from the position, for either profit or loss. A trader may set a target, which is the minimum profit that will induce the trader to leave the position. Likewise, a trader must have a maximum loss she is willing to tolerate; if potential losses go beyond this amount, the trader will exit the position in order to prevent any further loss (this is usually done by setting a **stop-loss order**, an order that is triggered to prevent further losses).

Overall, a **trading strategy** consists of: 
- Trading signals for prompting trades
- Rules on the portfolio risk amount for any particular strategy 
- A complete exit strategy for any trade

##Moving Averages Strategy

A **moving average crossover strategy** is outlined as follows, using a 20-day moving average and a 50-day moving average as the *"fast"*/*"slow"* moving averages.
- Trade the asset when the fast moving average cross over the slow moving average
- Exit the trade when the fast moving average cross over the slow moving average again.  

A long trade will be prompted when the fast moving average crosses from below to above the slow moving average, and the trade will be exited when the fast moving average crosses below the slow moving average later. A short trade will be prompted when the fast moving average crosses below the slow moving average, and the trade will be exited when the fast moving average later crosses above the slow moving average.

Chart of the moving averages for Google's stock:

![Image](/figure_6.png)

The quality of the strategy can be evaluated through backtesting, which is to look at how profitable the strategy is on historical data. For example, looking at the above chart’s performance on Google stock, if the 20-day moving average is the fast moving average and the 50-day moving average the slow, this strategy appears to be ambivalent.

##Trading Signals

Regime changes provide the presence of **trading signals**. When a bullish regime begins, a buy signal is triggered, and when it ends, a sell signal is triggered. The converse is true for bearish regimes. (Buy signals for bearish regimes is for shorting stocks, or derivatives like stock options to bet against the market).