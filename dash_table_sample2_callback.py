from dash import Dash, Input, Output, callback
import dash_table as dt
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import datetime

dt_now = datetime.datetime.now()

df = pd.read_csv('https://git.io/Juf1t')
i=1

df2 = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df2, x="sepal_width", y="sepal_length")

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
us_cities.head()
fig_map = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1(children='Hello Dash'),
    dbc.Label('Click a cell in the table:'),
    dt.DataTable(
        id='tbl', data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{Number of Solar Plants} > 100',
                #'column_id': 'Number of Solar Plants'
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        },
        ],
    ),
    dbc.Alert(id='tbl_out'),
    dcc.Graph(figure=fig_map),
    dcc.Graph(figure=fig),
    dcc.Interval(
        id='interval-component',
        interval=10*1000, # in milliseconds
        n_intervals=0
    )
])

# @callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
# def update_graphs(active_cell):
#     #return str(active_cell) if active_cell else "Click the table"
#     dt_now = datetime.datetime.now()
#     dtnow_str=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
#     return dtnow_str if active_cell else "Click the table"

@callback(Output('tbl_out', 'children')
        , Input('interval-component', 'n_intervals'))
def update_live(active_cell):
    #return str(active_cell) if active_cell else "Click the table"
    dt_now = datetime.datetime.now()
    dtnow_str='Live Update : '+ dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    df.iat[0,0]=dtnow_str
    return dtnow_str if active_cell else "Click the table"

@callback(Output('tbl', 'data')
        , Input('interval-component', 'n_intervals'))
def update_live(data):
    #return str(active_cell) if active_cell else "Click the table"
    dt_now = datetime.datetime.now()
    dtnow_str='Live Update : '+ dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    df.iat[0,0]=dtnow_str
    if df.iat[0,1]>100:
        df.iat[0,1]=50
    else:
        df.iat[0,1]=150
    data=df.to_dict('records')
    return data

if __name__ == "__main__":
    app.run_server(debug=True)
