from dash import Dash, Input, Output, callback
import dash_table as dt
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import datetime
import os

#マップ作成関数
def CreateMap():
    fig_map = px.scatter_mapbox(df_sensor, lat="lat", lon="lon", color="Sensor_value", size="Sensor_value",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=17,hover_name ='Sensor'
                  ,hover_data=["level"],mapbox_style="carto-positron")
    return fig_map


#カレントディレクトリの取得
#current_path = os.getcwd()

#現在時刻を取得
dt_now = datetime.datetime.now()

i=1

df2 = px.data.iris()  # iris is a pandas DataFrame
fig = px.scatter(df2, x="sepal_width", y="sepal_length")

#read sensor data
df_sensor=pd.read_csv('examples\\dash_table_sample_callback\\setting_sensordata.csv')

#map dataをグラフ化
print(df_sensor)
fig_map=CreateMap()
# fig_map = px.scatter_mapbox(df_sensor, lat="lat", lon="lon", color="level", size="Sensor_value",
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=17,hover_name ='Sensor'
#                   ,hover_data=["level"],mapbox_style="carto-positron")

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#dashboard layout
app.layout = dbc.Container([
    html.H1(children='Sensor Dashboard'),
    dbc.Label('Sensor data in the table:'),
    dt.DataTable(
        id='tbl', data=df_sensor.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_sensor.columns],
        style_data_conditional=[
        {
            #caution
            'if': {
                'filter_query': '{Sensor_value} > 80',
                #'column_id': 'Value'
            },
            'backgroundColor': 'yellow',
            'color': 'black'
        },
        {
            #NG
            'if': {
                'filter_query': '{Sensor_value} > 130',
                #'column_id': 'Value'
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        },
        ],
    ),
    dbc.Alert(id='tbl_out'),
    dcc.Graph(figure=fig_map,id='graph_map'),
    dcc.Graph(figure=fig),
    dcc.Interval(
        id='interval-component',
        interval=10*1000, # in milliseconds
        n_intervals=0
    )
])

#update table data
@callback(Output('tbl_out', 'children')
        , Input('interval-component', 'n_intervals'))
def update_live(active_cell):
    #return str(active_cell) "
    dt_now = datetime.datetime.now()
    dtnow_str='Live Update : '+ dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    #df_sensor.iat[0,0]=dtnow_str
    return dtnow_str if active_cell else "Click the table"
#update table data
@callback(Output('tbl', 'data')
        , Input('interval-component', 'n_intervals'))
def update_live(data):
    #return str(active_cell) if active_cell else "Click the table"
    dt_now = datetime.datetime.now()
    dtnow_str='Live Update : '+ dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    #df_sensor.iat[0,0]=dtnow_str
    if df_sensor.iat[0,2]>100:
        df_sensor.iat[0,1]='OK'
        df_sensor.iat[0,2]=50
    else:
        df_sensor.iat[0,1]='NG'
        df_sensor.iat[0,2]=150
    data=df_sensor.to_dict('records')
    return data

#update graph map
@app.callback(Output('graph_map', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    fig_map=CreateMap()
    return fig_map

if __name__ == "__main__":
    app.run_server(debug=True)
