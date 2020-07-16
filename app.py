import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import sqlite3
import time

import threading 

app = dash.Dash(__name__)
server = app.server
  
import twitter
class thread(threading.Thread): 
    def __init__(self, thread_name, thread_ID): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 
    def run(self): 
        # print(str(self.thread_name) +"  "+ str(self.thread_ID)); 
        twitter.get_tweets()
  
thread1 = thread("", 1001)   
thread1.start() 


app.layout = html.Div(
    [
        dcc.Input(id='term',value='car',type='text'),
        dcc.Graph(id = 'live-graph',animate = True),
        dcc.Interval(id = 'graph',interval=1000,n_intervals = 0)
    ]
)

@app.callback(Output('live-graph','figure'),
              [Input('term','value'),
               Input('graph','n_intervals')])
def update_graph(term,n):
    conn = sqlite3.connect('twitter.db')
    df = pd.read_sql("select * from sentiment where tweet like '%"+term+"%' order by unix desc limit 1000",conn)
   
    df['unix'] = pd.to_datetime(df['unix'],unit='ms')
    df.sort_values('unix',inplace=True)
    df.set_index('unix',inplace=True)
    
    df['smoothe_sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()
    
    df = df.resample('2s').mean()
    df.dropna(inplace=True)
            
    X = df.index[-100:]
    Y = df.smoothe_sentiment.values[-100:]
    # print(df['smoothe_sentiment'][-1])
    # print(Y)
    # print('--------------------')
    # print(len(df))
    # print(min(Y))
    # print(max(Y))
    # global X
    # global Y
    # X.append(X[-1]+1)
    # Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    
    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
    )
    
    layout = go.Layout(xaxis = dict(range=[min(X),max(X)]),
                       yaxis = dict(range=[min(Y),max(Y)]))
    
    return {'data':[data],'layout':layout}


if __name__ == "__main__":
    app.run_server(debug=True)
