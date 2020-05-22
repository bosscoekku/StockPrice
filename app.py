import os
import sys
import dash 
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input,Output,State
import pandas_datareader.data as web
import pandas as pd
from datetime import datetime

os.environ["ALPHAVANTAGE_API_KEY"] = "UYGV8I8OA3NOLHI7"
app  = dash.Dash()
nsdp = pd.read_csv("data/NASDAQcompanylist.csv") 
nsdp.set_index("Symbol",inplace = True)
options = []
for tic in nsdp.index:
    #{"Label":"user sees","value":"script sees"}
    mydict = {}
    mydict["label"] = nsdp.loc[tic]["Name"] + " " + tic # Apple Co. APPL
    mydict["value"] = tic
    options.append(mydict)

app.layout = html.Div([
                html.H1("Stock Ticker Dashboard"),
                html.Div([
                    html.H3("Enter a stock symbol:",style = {"paddingRight":"30px"}),
                     dcc.Dropdown(id = "my_stock_picker",
                            options = options,
                            value = ["TSLA"],
                            multi = True
                        )
                ],style = {"display":"inline-block","verticalAlign":"top","width":"30%"}),
                html.Div([html.H3("Select a start and end date:"),
                        dcc.DatePickerRange(id = "my_date_picker",
                                            min_date_allowed = datetime(2015,1,1),
                                            max_date_allowed = datetime.today(),
                                            start_date       = datetime(2020,1,1),
                                            end_date         = datetime.today()
                        ),
                        html.Button(id = "submit-button",
                                n_clicks =  0,
                                children = "เช็คข้อมูล",
                                style = {"fontSize":27,"marginLeft":"8px"}),
                ],style = {"display":"inline-block"}),
                
                dcc.Graph(id = "my_graph",
                            figure = {"data":[
                                {
                                    'x':[1,2],
                                    'y':[3,1]
                                }
                            ],"layout":{"title":"Default title"}}
                
                )
                

])
@app.callback(Output("my_graph","figure"),
            [Input("submit-button","n_clicks")],
            [State("my_stock_picker","value"),
             State("my_date_picker","start_date"),
             State("my_date_picker","end_date")])
def update_graph(n_clicks,stock_ticker,start_date,end_date):
    start = datetime.strptime(start_date[:10],"%Y-%m-%d")
    end   = datetime.strptime(end_date[:10],"%Y-%m-%d")
    
    traces = []
    for tic in stock_ticker:
        df    = web.DataReader(tic,"av-daily",start,end)
        traces.append({
            'x':df.index,
            'y':df["close"],
            "name":tic
        })

    fig = {
        "data":traces,
        "layout":{"title":stock_ticker}
    }
    return fig
if __name__ == "__main__":
    app.run_server()