import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

airport_traffic = pd.read_csv(DATA_PATH.joinpath('2011_february_us_airport_traffic.csv'))

layout = html.Div([

html.Div([
        html.Div([


            html.P('US Airport Arrivals Data', className = 'fix_label', style = {'color': 'black', 'margin-top': '2px'}),
            dcc.Dropdown(id = 'select_state1',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'AL',
                         placeholder = 'Select state',
                         options = [{'label': c, 'value': c}
                                    for c in (airport_traffic['state'].unique())], className = 'dcc_compon'),

            ], className = "create_container2 four columns", style = {'margin-bottom': '20px', "margin-top": "20px"}),

    ], className = "row flex-display"),

            html.Div([
                html.Div([

                    dcc.Graph(id = 'map_5',
                              config = {'displayModeBar': 'hover'}),

                ], className = "create_container2 eight columns"),

            ], className = "row flex-display"),




], id="mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(Output('map_5', 'figure'),
              [Input('select_state1', 'value')])
def update_graph(select_state1):
    airport_traffic1 = airport_traffic.groupby(['state', 'city', 'airport', 'lat', 'long'])['cnt'].sum().reset_index()
    airport_traffic2 = airport_traffic1[airport_traffic1['state'] == select_state1]

    return {
        'data': [go.Scattergeo(
            lon = airport_traffic2['long'],
            lat = airport_traffic2['lat'],
            locationmode = 'USA-states',
            mode = 'markers',
            marker = dict(
                size = 12,
                color = airport_traffic2['cnt'],
                colorscale = 'HSV',
                showscale = False,
                line_color = 'rgb(40,40,40)',
                line_width = 0.5,),


            hoverinfo = 'text',
            hovertext =
            '<b>State</b>: ' + airport_traffic2['state'].astype(str) + '<br>' +
            '<b>City</b>: ' + airport_traffic2['city'].astype(str) + '<br>' +
            '<b>Airport</b>: ' + airport_traffic2['airport'].astype(str) + '<br>' +
            '<b>Lat</b>: ' + [f'{x:.4f}' for x in airport_traffic2['lat']] + '<br>' +
            '<b>Long</b>: ' + [f'{x:.4f}' for x in airport_traffic2['long']] + '<br>' +
            '<b>Total Arrivals</b>: ' + [f'{x:,.0f}' for x in airport_traffic2['cnt']] + '<br>'

        )],

        'layout': go.Layout(
            margin = {"r": 0, "t": 0, "l": 0, "b": 0},
            plot_bgcolor = '#e6e6e6',
            paper_bgcolor = '#e6e6e6',
            hovermode = 'closest',

            geo = dict(
                scope='usa',
                countrywidth = 0.5,
                subunitwidth = 0.5,
                showframe = False,
                showcountries = True,
                countrycolor = 'rgb(40,40,40)',
                showocean = True,
                oceancolor = "LightBlue",
                showcoastlines = True,
                coastlinecolor = "RebeccaPurple",
                showland = True,
                landcolor = 'rgb(217, 217, 217)',
                showlakes = True,
                lakecolor = 'rgb(85,173,240)',
                projection = {'type': 'albers usa'}
            ),

        )

    }
