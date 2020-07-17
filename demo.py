import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas_datareader.data as web
import datetime
import sqlite3
import pandas as pd

app = dash.Dash()

conn = sqlite3.connect('twitter.db')
df = pd.read_sql("select * from sentiment",conn)
        

app.layout = html.Div(children=[html.H1('Dash tutorial'),
                                dcc.Input(id='input',value='',type='text'),
                                html.Div(id='output-graph'),
                                dt.DataTable(id='output-table',
                                             columns = [{"name":i,"id":i} for i in df.columns],
                                             data= df.to_dict('records'))
                                
                                # dcc.Graph(id = 'example',
                                #           figure = {'data' : [
                                #               {'x':df.index,
                                #                'y':df.Close,
                                #                'type':'line','name':stock},
                                #               ],'layout' : {'title':stock}})
                                ])

# app.layout = html.Div(children=[
#     dcc.Input(id='input',value='Enter something',type='text'),
#     html.Div(id='output')    
# ])

@app.callback(
    [Output(component_id='output-graph',component_property='figure'),
    Output(component_id='output-table',component_property='children')],
    [Input(component_id='input',component_property='value')]
)
def update_value(input_data):
    start = datetime.datetime(2015,1,1)
    end = datetime.datetime.now()
    # input_data = 'sap'
    try:
        df = web.DataReader(input_data,'yahoo',start,end)
    except:
        return 'no graph'
    return [dcc.Graph(id = 'example',
                     figure = {'data' : [
                         {'x':df.index,
                          'y':df.Close,
                          'type':'line','name':input_data},
                         ],'layout' : {'title':input_data}}),
            dt.DataTable(data=df.to_dict('records'),
                         columns=[{"name": i, "id": i} for i in df.columns])]

# print(update_value(2))


if __name__ == '__main__':
    app.run_server(debug = True)

