import Engulf_project
import pandas as pd
import plotly.graph_objects as plt
import testchart


from Engulf_project import df
from Engulf_project import tradeind # importing index list of engulfing candles from the dataframe
from plotly.subplots import make_subplots
from testchart import act_win_data
from testchart import prediction_data


#df = df.set_index(pd.DatetimeIndex(df['date'].values)) #indexing by date

# figure to display the candlestick chart
ind = tradeind

open_data = df['open']
high_data = df['high']
low_data = df['low']
close_data = df['close']
dates = df['date']

#first trace to display all candlesticks
trace = plt.Candlestick(
    x=dates,
    open=open_data,
    high=high_data,
    low=low_data,
    close=close_data,
    name='Normal candles'
)

highlight_index = ind #variable to carry index list of engulfing candles extracted from the dataframe

#second trace to display highlighted engulfing candles
candle_highlight = plt.Candlestick(
    x=[dates[i] for i in highlight_index],
    open=[open_data[i] for i in highlight_index],
    high=[high_data[i] for i in highlight_index],
    low=[low_data[i] for i in highlight_index],
    close=[close_data[i] for i in highlight_index],
    increasing={'line': {'color': 'yellow'}},
    decreasing={'line': {'color': 'purple'}},
    name='Engulfing candle'
)

figure = plt.Figure(data = [trace, candle_highlight])


figure.update_layout(xaxis_rangeslider_visible = False,
                     title = "EURUSD CHART 2003 to 2019 with highlighted engulfing candles",
                     yaxis_title = "Price($)",
                     xaxis_title = "Date"
)

# variables and calculations used to plot win and loss info
bullwins= len(df[(df['Win']==1) & (df['signal1']==1)]) #counts number of bullish engulfing winning trades
bullloss = len(df[(df['loss']==1) & (df['signal1']==1)])   #counts number of bullish engulfing losing trades
bearwins = len(df[(df['Win']==1) & (df['signal1']==2)])  #counts number of  bearish engulfing winning trades
bearloss = len(df[(df['signal1']==2) & (df['loss']==1)] )  #counts number of  bearish engulfing losing trades


#Fig first bar chart displaying ratios
x=['Bullish', 'Bearish']
fig = plt.Figure(plt.Bar(x=x, y=[bullloss,bearloss], name='Losses'))
fig.add_trace(plt.Bar(x=x, y=[bullwins,bearwins], name='Wins'))


fig.update_layout(barmode='stack',
                    title = 'Wins to Losses ratios'
                  )
fig.update_xaxes(categoryorder='array', categoryarray= ['Bullish','Bearish'])

#FIG1 chart showing yearly data
df['date'] = pd.to_datetime(df['date'],dayfirst=True) #parsing to date format
yeardata = df.groupby(df.date.dt.year)[['Win', 'loss']].sum() # putting data to a dataframe called yeardata

years = yeardata.index.tolist() # converting years to list to plot the graph

fig1 = plt.Figure()
fig1.add_trace(plt.Bar(x=years,
                y=yeardata['Win'].tolist(),
                name='Winning Trades',
                marker_color='rgb(0,191,255)'
                ))
fig1.add_trace(plt.Bar(x=years,
                y=yeardata['loss'].tolist(),
                name='Losing Trades',
                marker_color='rgb(220,20,60)'
                ))

fig1.update_layout(
    title='Engulfing data grouped by year',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Signals',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.1, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
#fig1.show()

#Charts to show results from machine learning
fig2 = make_subplots(rows=1, cols=2,
                     subplot_titles=("Prediction Plots", "Actual Data Plots"))

fig2.add_trace(
    plt.Scatter(x=prediction_data['Predictions'].index.tolist(), y=prediction_data['Predictions']),
    row=1, col=1
)

fig2.add_trace(
    plt.Scatter(x=act_win_data['ActualWins'].index.tolist(), y=act_win_data['ActualWins']),
    row=1, col=2
)

fig2.update_xaxes(title_text="Trade index", row=1, col=1)
fig2.update_xaxes(title_text="Trade index",  row=1, col=2)

fig2.update_yaxes(title_text="Prediction line plot 0 or 1",range=[0,1.25],  row=1, col=1)
fig2.update_yaxes(title_text="Actual data line plot 0 or 1",range=[0,1.25],  row=1, col=2)

fig2.update_layout(height=600, width=800, title_text="RandomForestClassifier model predictions vs Actual trade outcome")
#fig2.show()