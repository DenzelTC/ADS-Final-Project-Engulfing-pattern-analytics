import Engulf_project
import plotly.graph_objs as plt
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score


from Engulf_project import df

df1 = df
def candlediff (df6):
    length = len(df6)
    bars = 26
    high = list(df6['high'])
    low = list(df6['low'])
    close = list(df6['close'])
    open = list(df6['open'])
    signal = list(df6['signal1'])
    win = list(df6['Win'])

    bodydiff = [0] * length
    sizediff = [0] * length

    #loop to calculate body difference and candlesize between the two candles in the pattern
    for line in range(0, length):

        for i in range(1, bars + 1):
            if win[line]==1 and signal[line]==1:
                bodydiff[line] = abs((close[line] - open[line])- (open[line-i] - close[line]-i))
                sizediff[line] = abs((high[line] - low[line])- (high[line-i] - low[line-i]))

            elif win[line]==1 and signal[line]==2:
                bodydiff[line] = abs((open[line] - close[line])- (close[line-i] - open[line-i]))
                sizediff[line] = abs((high[line] - low[line])- (high[line-i] - low[line-i]))

    return sizediff, bodydiff #functions return the 2 values to be added to the dataframe

df1['candlediff'], df1['bodydiff'] = candlediff(df1)

df1.drop(columns=[ 'Tradeclose','equity','equity1' , 'equity2'], inplace=True) #removal of the unnecessary columns
#print(df1.head())

wintrades = df1.groupby(df1.Win) # creating dataframe called wintrades which carries all winning trades data
windf = wintrades.get_group(1)

#windf= df1
windf['date'] = pd.to_datetime(windf['date'], dayfirst=True)
#print(windf.to_string())
#print(len(windf))

rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

train = windf[windf['date']<'2005-01-21']
test = windf[windf['date']>='2005-01-21']

predictors = [ 'open','high','low','close','money', 'volume','candlediff','bodydiff'] #data columns to be used for prediction

rf.fit(train[predictors], train['Win'])

preds= rf.predict(test[predictors])

accu= accuracy_score(test['Win'],preds)
print(accu)
#print(len(preds))
#print(len(test['Win']))

#creating a crosstab to analyze predictions vs actual
combined = pd.DataFrame(dict(actual= test['Win'], prediction= preds))
print(pd.crosstab(index=combined['actual'], columns=combined['prediction']))

print(precision_score(test['Win'],preds))

#act_win_data = test['Win']


testD_ind =  test['Win'].index.tolist() #extract index to list
#print(testD_ind)

act_win_data = pd.DataFrame().assign(ActualWins=test['Win']) #dataframe for Actual wins
prediction_data = pd.DataFrame(preds, index=testD_ind,columns=['Predictions']) #dataframe for ML model predictions
#print(act_win_data)
#print(act_win_data)
