from taipy.gui import Gui, notify
from datetime import date
import yfinance as yf

import talib
import pandas as pd
import pandas_ta as ta
import numpy as np

####################################################################§
# Parameters for retrieving the stock data
start_date = "2021-01-01"
end_date = date.today().strftime("%Y-%m-%d")
selected_stock = 'AAPL'
time= ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
inter = time[8]
rsi_value = 14
window = 14
window_2 = 21
# Constants
#Z_THRESH = 1.6
window_3 = 30
lookback = 14
window_4 = 10
###################################################################
# get data
def get_stock_data(ticker, start, end, inter):
    ticker_data = yf.download(ticker, start, end, interval = inter)  # downloading the stock data
    ticker_data.reset_index(inplace=True)  # put date in the first column
    #ticker_data['Date'] = ticker_data['Date'].dt.tz_localize(None)
    return ticker_data
    

def get_data_from_range(state):
    print("GENERATING HIST DATA")
    print(state.start_date)
    state.data = get_stock_data(state.selected_stock, state.start_date, state.end_date, state.inter)
    notify(state, 's', 'Historical data has been updated!')
# indicators def
def add_RSI(data, rsi_value): 
    data['RSI'] = talib.RSI(data['Close'], timeperiod=rsi_value)
    return data

def add_EMA(data, window): 
    data['EMA'] = talib.EMA(data['Close'], timeperiod=window)
    return data

def add_EMA_2(data, window_2):
    data['EMA_2'] = talib.EMA(data['Close'], timeperiod=window_2)
    return data

def calculate_z_scores(data, window_3): #Calculates Z-scores for given periods.
    data['z_score'] = data.ta.zscore(length=window_3, append=True)
    return data

def get_ci(high, low, close, lookback):
    tr1 = pd.DataFrame(high - low).rename(columns = {0:'tr1'})
    tr2 = pd.DataFrame(abs(high - close.shift(1))).rename(columns = {0:'tr2'})
    tr3 = pd.DataFrame(abs(low - close.shift(1))).rename(columns = {0:'tr3'})
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').dropna().max(axis = 1)
    atr = tr.rolling(1).mean()
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    data['ci_14'] = 100 * np.log10((atr.rolling(lookback).sum()) / (highh - lowl)) / np.log10(lookback)
    return data


#taipy states
def forecast_display(state):
    notify(state, 'i', 'Predicting...')
    state.data = add_RSI(state.data, state.rsi_value)
    notify(state, 's', 'Done! Data has been updated!')

def forecast_display2(state):
    notify(state, 'i', 'Predicting...')
    state.data = add_EMA(state.data, state.window)
    notify(state, 's', 'Done! Data has been updated!')

def forecast_display3(state):
    notify(state, 'i', 'Predicting...')
    state.data = add_EMA_2(state.data, state.window_2)
    notify(state, 's', 'Done! Data has been updated!')

def forecast_display4(state):
    notify(state, 'i', 'Predicting...')
    state.data = calculate_z_scores(state.data, state.window_3)
    notify(state, 's', 'Done! Data has been updated!')

def forecast_display5(state):
    notify(state, 'i', 'Predicting...')
    state.data = get_ci(state.data['High'], state.data['Low'], state.data['Close'], state.lookback)
    notify(state, 's', 'Done! Data has been updated!')


################################################################################################################



################################################################################################################
#### Getting the data, make initial forcast and build a front end web-app with Taipy GUI
data = get_stock_data(selected_stock, start_date, end_date, inter)
data = add_RSI(data, rsi_value)
data = add_EMA(data, window)
data = add_EMA_2(data, window_2)
data = calculate_z_scores(data, window_3)
data = get_ci(data['High'], data['Low'], data['Close'], lookback)

##################################################################
#taipy layout


layout = {
  "shapes": [
    
    #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 30, "x1": end_date , "y1": 30,
      
      "line": {
        "color": 'rgb(50, 171, 96)',
        "dash": 'dashdot'
      }
    },
     #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 70, "x1": end_date , "y1": 70,
      
      "line": {
        "color": 'rgb(255, 0, 0)',
        "dash": 'dashdot'
      }
    },
     #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 50, "x1": end_date , "y1": 50,
      
      "line": {
        "color": 'rgb(160, 160, 160)',
        "dash": 'dot'
      }
    }
  
  ]
}
layout2 = {
  "shapes": [
    
    #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 0, "x1": end_date , "y1": 0,
      
      "line": {
        "color": 'rgb(160, 160, 160)',
        "dash": 'dot'
      }
    },
     #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 2, "x1": end_date , "y1": 2,
      
      "line": {
        "color": 'rgb(255, 0, 0)',
        "dash": 'dashdot'
      }
    },
  #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 3, "x1": end_date , "y1": 3,
      
      "line": {
        "color": 'rgb(255, 0, 0)',
        "dash": 'dashdot'
      }
    },
   
     #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": -2, "x1": end_date , "y1": -2,
      
      "line": {
        "color": 'rgb(20, 171, 96)',
        "dash": 'dashdot'
      }
    },
  #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": -3, "x1": end_date , "y1": -3,
      
      "line": {
        "color": 'rgb(20, 171, 96)',
        "dash": 'dashdot'
      }
    }
  ]
}
stylekit = {
  "color_primary": "#BADA55",
  "color_secondary": "#C0FFE"
}
###############
options = {
    # Candlesticks that show decreasing values are orange
    "decreasing": {
        "line": {
            "color": "orange"
        }
    },
    # Candlesticks that show decreasing values are blue
    "increasing": {
        "line": {
            "color": "green"
        }
    }
}

layout3 = {
   
    "xaxis": {
        # Hide the range slider
        "rangeslider": {
            "visible": True
        }
    }
}
layout4 = {
  "shapes": [
    
    #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 38.2, "x1": end_date , "y1": 38.2,
      
      "line": {
        "color": 'rgb(50, 171, 96)',
        "dash": 'dashdot'
      }
    },
     #Line Horizontal
    {
      "type": 'line',
      "x0": start_date, "y0": 61.8, "x1": end_date , "y1": 61.8,
      
      "line": {
        "color": 'rgb(255, 0, 0)',
        "dash": 'dashdot'
      }
    },
     #Line Horizontal
    
  ]
}
#taipy main page
#######################
root_md="<|navbar|>"
show_dialog = False

page =  """<|toggle|theme|>

<|container|

# Simple stock Price **Analyzor**{: .color-primary}
<|layout|columns=1 2 1|gap=40px|class_name=card p2|

<dates|
#### Select **dates**{: .color-primary}
From:
<|{start_date}|date|>  
To:
<|{end_date}|date|> 
<br/>
Select interval:
<|{inter}|selector|lov={time}|dropdown=True|width=100%|>

<br/>
<br/>
<|Update dates and ticker|button|on_action=get_data_from_range|>
|dates>


<ticker|
#### Selected **Ticker**{: .color-primary}
Please enter a valid ticker: 
<|{selected_stock}|input|label=Stock|>
<br/> 
or choose a popular one:
<|{selected_stock}|toggle|lov=MSFT;GOOG;AAPL; AMZN; META; WBD; SPY|>
|ticker>


<indicators|
RSI Value:
<|{rsi_value}|slider|min=2|max=50|>
<|CALCULATE RSI|button|on_action=forecast_display|>

EMA:
<|{window}|slider|min=5|max=200|>
<|CALCULATE EMA|button|on_action=forecast_display2|>

SECOND EMA:
<|{window_2}|slider|min=5|max=200|>
<|CALCULATE EMA|button|on_action=forecast_display3|>

Z_SCORE:
<|{window_3}|slider|min=5|max=200|>
<|CALCULATE Z_SCORE|button|on_action=forecast_display4|>

CHOP INDEX:
<|{lookback}|slider|min=5|max=200|>
<|CALCULATE CHOP INDEX|button|on_action=forecast_display5|>
|indicators>
|>
|>
<|Click here to expand and view data frame|expandable|expanded=False|
<|
### **Whole**{: .color-primary} historical data: <|{selected_stock}|>
<|{data}|table|width=100%|height=50%|>
|>
|>
<|
### Historical **closing**{: .color-primary} price
<|{data}|chart|type=candlestick|x=Date|open=Open|close=Close|low=Low|high=High|options={options}|layout={layout3}|>
|>

<|
### Historical **daily**{: .color-primary} trading volume
<|{data}|chart|mode=line|x=Date|y=Volume|>
|>







<|
### Historical **closing**{: .color-primary} price with EMA
<|{data}|chart|mode=line|x=Date|y[1]=Close|y[2]=EMA|y[3]=EMA_2|>
|>
<br/>
<|
### RSI **indicator**{: .color-primary} line
<|{data}|chart|mode=line|x=Date|y=RSI|layout = {layout}|>
|>
<br/>
<|
### Z-SCORE **indicator**{: .color-primary} line
<|{data}|chart|mode=line|x=Date|y=ZS_30|layout = {layout2}|>
|>

<br/>
<|
### CHOP INDEX **indicator**{: .color-primary} line
###### - Readings above **61.8%**{: .color-primary} indicate a choppy market that is bound to breakout. We should be ready for some directional.
###### - Readings below **38.2%**{: .color-primary} indicate a strong trending market that is bound to stabilize. Hence, it may not be the best idea to follow the trend at the moment.
<|{data}|chart|mode=line|x=Date|y=ci_14|layout = {layout4}|>
|>



"""


# Run Taipy GUI
gui = Gui(page)
#partial = gui.add_partial(partial_md)
gui.run(dark_mode=True, port=5001,stylekit=stylekit)
