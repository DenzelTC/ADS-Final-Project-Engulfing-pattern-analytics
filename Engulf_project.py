import pandas as pd
import numpy as np


#df = pd.read_csv(r"C:\Code X\Python\ADS_Final_Project_Engulfing\EURUSD_Candlestick_1_D_ASK_05.05.2003-19.10.2019.csv")#
url = "https://github.com/DenzelTC/ADS-Final-Project-Engulfing-pattern-analytics/blob/main/EURUSD_Candlestick_1_D_ASK_05.05.2003-19.10.2019.csv"
df = pd.read_csv(url)#

print(df.tail())

print(df.isna().sum())


def Revsignal1(df1):
    length = len(df1)
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    signal = [0] * length
    bodydiff = [0] * length
    candlesize = [0] * length
    stoploss = [0] * length
    takeprof = [0] * length
    trade = [0] * length

    # print(df1.head())

    for row in range(1, length):
        bodydiff[row] = abs(open[row] - close[row])
        bodydiffmin = 0.003
        if (bodydiff[row] > bodydiffmin and bodydiff[row - 1] > bodydiffmin and
                open[row - 1] < close[row - 1] and
                open[row] > close[row] and
                # open[row]>=close[row-1] and close[row]<open[row-1]):
                (open[row] - close[row - 1]) >= +0e-5 and close[row] < open[row - 1]):  # condition for the buy signal

            candlesize[row] = high[row] - low[row]
            signal[row] = 1
            trade[row] = 1
            takeprof[row] = close[row] + (candlesize[row] *2)  # takeprofit value is twice the engulfing candle size
            stoploss[row] = close[row] - candlesize[row] # stoploss value is the same as the engulfing candle value

        elif (bodydiff[row] > bodydiffmin and bodydiff[row - 1] > bodydiffmin and
              open[row - 1] > close[row - 1] and
              open[row] < close[row] and
              # open[row]<=close[row-1] and close[row]>open[row-1]):
              (open[row] - close[row - 1]) <= -0e-5 and close[row] > open[row - 1]):  # condition for the sell signal

            candlesize[row] = high[row] - low[row]
            signal[row] = 2
            trade[row] = 1
            takeprof[row] = close[row] - (candlesize[row] *2)  # takeprofit value is twice the engulfing candle size
            stoploss[row] = close[row] + candlesize[row]# stoploss value is the same as the engulfing candle value

        else:
            signal[row] = 0

        # signal[row]=random.choice([0, 1, 2])
        # signal[row]=1
    return signal, takeprof, stoploss, trade


df['signal1'], df['takeprofit'], df['stoploss'], df['trade'] = Revsignal1(df)
print(df.tail(100))


def mytarget(df1):
    length = len(df1)
    bars = 26
    lines = length
    high = list(df1['high'])
    low = list(df1['low'])
    close = list(df1['close'])
    open = list(df1['open'])
    takeprof = list(df1['takeprofit'])
    stoploss = list(df1['stoploss'])
    signal1 = list(df1['signal1'])
    tradeclose = list(df1['date'])
    # tradeclose = list(df1['date'])
    win = [0] * length
    loss = [0] * length
    equity = [0] * length
    money = [0] * length


    equity[0] = 10000
    for line in range(0, length):
        if equity[line] == 0.0: equity[line] = equity[line - 1]
        for i in range(1, bars + 1):

            if signal1[line] == 1:

                if high[line + i] >= takeprof[line] and win[line] == 0 and loss[line] == 0:
                    money[line] = (takeprof[line] - close[line]) * 10000
                    win[line] = 1
                    equity[line] = equity[line] + money[line]
                    tradeclose[line] = tradeclose[line + i]



                elif low[line + i] <= stoploss[line] and win[line] == 0 and loss[line] == 0:
                    money[line] = ( stoploss[line] - close[line]) * 10000
                    loss[line] = 1
                    equity[line] = equity[line] + money[line] #adds amount to equity
                    tradeclose[line] = tradeclose[line + i]


            elif signal1[line] == 2:

                if high[line + i] >= stoploss[line] and win[line] == 0 and loss[line] == 0:

                    money[line] = (close[line]- stoploss[line]) * 10000 #calculates loss
                    loss[line] = 1
                    equity[line] = equity[line] + money[line]
                    tradeclose[line] = tradeclose[line + i]


                elif low[line + i] <= takeprof[line] and win[line] == 0 and loss[line] == 0:
                    money[line] = (close[line] - takeprof[line]) * 10000 #calculate win
                    win[line] = 1
                    equity[line] = equity[line] + money[line] #adds amount to equity
                    tradeclose[line] = tradeclose[line + i]


#closes trades after 26 days
    for line in range(0, length):
       # if equity[line] == 0.0: equity[line] = equity[line - 1]
        for i in range(1, bars + 1):
            if money[line] == 0:

                if signal1[line] == 1:
                    if close[line] <= close[line + i]:
                        money[line] = (close[line + i] - close[line]) * 10000
                        win[line] = 1
                        equity[line] = equity[line] + money[line]
                        tradeclose[line] = tradeclose[line + i]

                    else:
                        money[line] = (close[line+i] - close[line]) * 10000 #calculate loss
                        loss[line] = 1
                        equity[line] = equity[line] + money[line]
                        tradeclose[line] = tradeclose[line + i]
                        break

                elif signal1[line] == 2:
                    if close[line] >= close[line + i]:
                        money[line] = (close[line] - close[line+i]) * 10000
                        win[line] = 1
                        equity[line] = equity[line] + money[line]
                        tradeclose[line] = tradeclose[line + i]

                    else:
                        money[line] = (close[line] - close[line+i]) * 10000 #calculate loss
                        loss[line] = 1
                        equity[line] = equity[line] + money[line]
                        tradeclose[line] = tradeclose[line + i]




    return tradeclose, money, win, loss, equity


df['Tradeclose'], df['money'], df['Win'], df['loss'], df['equity'] = mytarget(df)
print(df.tail())

def scallingin(df4):
    length1 = len(df4)
    bars1 = 26
    wintrade = list(df4['Win'])
    losstrade = list(df4['loss'])
    money1 = list(df4['money'])
    equity1 =[0] * length1
    equity2 =[0] * length1

    equity1[0]=10000
    equity2[0]=10000

    for line in range(0, length1):
        if equity1[line] == 0.0: equity1[line] = equity1[line - 1]  # takes previous value if there is no calculation
        if equity2[line] == 0.0: equity2[line] = equity2[line - 1]  # takes previous value if there is no calculation
        for i in range(1, bars1 + 1):
            if wintrade[line] == 1:
                equity1[line] = equity1[line] + (money1[line]*1.5)   #add another position when the first winning one has moved half the trade
                equity2[line] = equity2[line] + (money1[line]*2)   #add another position when the first winning one has moved half the trade
                break
            elif losstrade[line]==1:
                equity1[line] = equity1[line] + money1[line]
                equity2[line] = equity2[line] + money1[line]
                break
            else:0


    return equity1,equity2

df['equity1'], df['equity2']= scallingin(df)
#print(df.to_string())

equity= df['equity']
equity1= df['equity1']
equity2= df['equity2']
chartdata = df[['equity','equity1','equity2']].copy()
print(chartdata)

trades = df.groupby(df.trade)

df2 = trades.get_group(1) # extracting a dataframe called df2 of all the trades

tradeind = df2.index.tolist() # creating a list called tradeind and assigning all the indexes in the trades dataframe(df2)
#print(tradeind)

#print(df2.head(200))
df2.to_csv(r'C:\Users\denze\Downloads\ach1\trades.csv') # converting trades (df2) dataframe to csv for excel analysis

#print(df.to_string())
# print(df.head(200))

#print(df[df['Win'] == 1].count())

#print(df[df['loss'] == 1].count())

# print(df[df['signal1']==1].count())

# print(df[df['signal1']==2].count())
