import pandas as pd
import streamlit as st
import charts


from charts import df
from charts import figure
from charts import fig
from charts import fig1
from Engulf_project import chartdata
from charts import fig2


st.title("Engulfing pattern data analyser")
st.write("The DataFrame used for this analysis is EURUSD forex pair from MAY 2003 to October 2019 in the daily timeframe")

st.plotly_chart(figure)
st.plotly_chart(fig)
st.plotly_chart(fig1)

st.write("The chart below displays the the trading results with a risk to reward ratio of 1:2. "
         "equity line is without scalling in on winning positions, "
         "equity1 line is when scalling with 1 position "
         "and the equity2 line is when scaled in with 2 more positions. "
         "Scalling is done when trade is half way through to target")
st.line_chart(chartdata)

st.write("The charts before show prediction results trained from dataframe of only winning trades(to increase accuracy) so the model"
         " would predict which of the engulfing pattern would most likely be successful for the purposes "
         "of scalling in to increase returns on winning trades. The training to test ratio was nearly 1:6 "
         "and the prediction result were shown below comparing the plots which were either 1 for winning and 0 for losing.")
st.plotly_chart(fig2)


