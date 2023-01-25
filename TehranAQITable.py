from pydoc import classname
from attr import NOTHING
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_leaflet as dl
from dash import no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash
from dash import dash_table
import plotly.graph_objects as go


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'TehranAQITable'
load_figure_template("bootstrap")


# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

fig_names = ['CO', 'O3', 'NO2', 'SO2', 'PM10', 'PM2.5']
Table_Header = ['Name', 'CO', 'O3', 'NO2', 'SO2', 'PM10', 'PM2.5']
PAGE_SIZE = 15

#AQI Table for Stations in 1/24/2023 at 11 AM 
df =  pd.read_excel('TehranAQITable.xlsx', engine='openpyxl')


app.layout = (html.Div(children=[ 
                                html.H1('Tehran Air Pollution', className="pricing-header p-3 pb-md-4 mx-auto text-center"),
                                html.H2('Air Quality Index (AQI) for Stations in 1/24/2023 ', className="fs-5 text-muted text-center"),
                                
                                html.Div([ 
                                    html.Div([
                                        html.Hr(className="my=4"), 
                                        html.Div([
                                            html.Div( 
                                                [
                                                html.H3(' Select Index: ', className="col-md-7 col-lg-8")
                                                ]
                                            ),
                                            dcc.Dropdown(id='input-year', 
                                                        options=[{'label': i, 'value': i} for i in fig_names],
                                                        placeholder="Select Index",
                                                        className="form-select"),
                                                ], className="col-6 themed-grid-col"),                                      
                                    html.Div([
                                            html.Div(
                                                [
                                                html.H3(' Map Style: ', className="form-label")
                                                ]
                                            ),
                                            dcc.Dropdown(id='input-type',
                                                        options=[
                                                                {'label': 'Map Style 1 ', 'value': 'OPT1'},
                                                                {'label': 'Map Style 2 ', 'value': 'OPT2'},
                                                                {'label': 'Map Style 3 ', 'value': 'OPT3'},
                                                                {'label': 'Map Style 4 ', 'value': 'OPT4'},
                                                                {'label': 'Map Style 5 ', 'value': 'OPT5'}
                                                                ],
                                                        placeholder='Select a Map type',
                                                        className="form-select"),
                                            ], className="col-6 themed-grid-col")
                                    ],className="row mb-3 text-center"),
                                ],className="container themed-container text-center"),

                                html.Div([ ], id='plot1', className ="container-fluid themed-container text-center"),
                                
                                
                                html.Div([
                                          html.Div([ ], id='plot2'),
                                          html.Div([ ], id='plot3')
                                         ]),
                                html.Hr(className="my=4"),   
                                html.Div([     
                                        dash_table.DataTable(
                                                id='table',
                                                columns=[{"name": i, "id": i} for i in Table_Header],
                                                data=df.to_dict('records'),
                                                filter_action="native",
                                                sort_mode="single",
                                                page_size=PAGE_SIZE,    
                                                page_current=0,
                                                ) 
                                         ], className="container themed-container text-center")
                                ])
                                
             )             

@app.callback(Output('datatable-paging', 'page_size'),    
             [Input('select_page_size', 'value')])    
def update_graph(page_size):    
    return page_size
    

@app.callback( [Output(component_id='plot1', component_property='children')],
               [Input(component_id='input-type', component_property='value'),
                Input(component_id='input-year', component_property='value')],
               [State("plot1", 'children')])
def get_graph(chart, year,children):
      
       
        if chart == 'OPT1':

            fig = px.scatter_mapbox(df, lat="lat", lon="lon", color=df[year], size=df[year],
                            color_continuous_scale=px.colors.cyclical.IceFire
                                    , size_max=40
                                    , zoom=10
                                    , hover_name="Name")
            fig.update_layout(mapbox_style="carto-positron",
                            mapbox_center_lon=51.368642, 
                            mapbox_center_lat=35.688167,
                            mapbox_zoom=11)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650)


            return [dcc.Graph(figure=fig)
                   ]


        elif chart == 'OPT2':
            
            fig = px.density_mapbox(df
                                    ,lat=df['lat']
                                    ,lon=df['lon']
                                    ,z=df[year]
                                    ,center=dict(lat=35, lon=51)
                                    ,zoom=10
                                    ,mapbox_style="carto-positron"
                                    ,opacity = 0.6
                                    ,radius = 70.5
                                    ,range_color = [df[year].min(),df[year].max()]
                                    ,color_continuous_scale='inferno'

                                )
            fig.add_trace(
                go.Scattermapbox(
                    lat=df["lat"],
                    lon=df["lon"],
                    mode="markers",
                    showlegend=False,
                    hoverinfo="skip",
                    marker={
                        "color": df["PM2.5"],
                        "size": df["PM2.5"].fillna(5),
                        "coloraxis": "coloraxis",
                        "sizeref": (df[year].max()),
                        "sizemode": "area"},))

            fig.update_layout(mapbox_style="open-street-map",
                            mapbox_center_lon=51.368642, 
                            mapbox_center_lat=35.698167,
                            mapbox_zoom=10)

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650)


            
            return [dcc.Graph(figure=fig)
                   ]

        elif chart == 'OPT3':
            fig = px.density_mapbox(df
                    ,lat=df['lat']
                    ,lon=df['lon']
                    ,z=df[year]
                    ,center=dict(lat=35, lon=51)
                    ,zoom=10
                    ,mapbox_style="carto-positron"
                    ,opacity = 0.4
                    ,radius = 75.5
                    ,range_color = [df[year].min(),df[year].max()]
                    ,color_continuous_scale='deep'
                    )
            fig.add_trace(
                go.Scattermapbox(
                    lat=df["lat"],
                    lon=df["lon"],
                    mode="markers",
                    showlegend=False,
                    hoverinfo="skip",
                    
                    marker={
                        "color": df[year],
                        "size": df[year].fillna(5),
                        "coloraxis": "coloraxis",
                        "sizeref": (df[year].max()*2),
                        "sizemode": "area",},))

            fig.update_layout(mapbox_style="carto-positron",
                            mapbox_center_lon=51.368642, 
                            mapbox_center_lat=35.698167,
                            mapbox_zoom=10)

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650)
            
            return [dcc.Graph(figure=fig)
                   ]


        elif chart == 'OPT4':
            fig = go.Figure(go.Densitymapbox(lat=df['lat'], 
                                 lon=df['lon'], 
                                 z=df[year],
                                 radius=40,
                                 colorscale=[[0.0, 'blue',],[0.3,'lime'],[0.5,'yellow'],[0.7,'orange'],[1.0, 'red']],
                                 zmin=0.0,
                                 zmax=100.0,
                                )
               )
            fig.update_layout(mapbox_style="carto-positron",
                            mapbox_center_lon=51.368642, 
                            mapbox_center_lat=35.718167,
                            mapbox_zoom=10)

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650)


            return [dcc.Graph(figure=fig)
                   ]

        elif chart == 'OPT5':
            
            # You must enter your token here
            mapbox_access_token = ""
            
            fig = go.Figure(go.Scattermapbox(
                                lat=df['lat'], 
                                lon=df['lon'],
                                mode='markers',
                                marker=go.scattermapbox.Marker(
                                    size=20,
                                    color='blue',
                                    symbol='marker',
                                ),
                                text=[df['Name']],
                            ))
            fig.update_layout(
                            autosize=False,
                            hovermode='closest',
                            mapbox_center_lon=51.368642, 
                            mapbox_center_lat=35.718167,
                            mapbox_zoom=10,
                            mapbox=dict(
                                accesstoken=mapbox_access_token,
                                bearing=0,),
                )


            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650)

            return [dcc.Graph(figure=fig)
                   ]


        else:
                fig = go.Figure(go.Densitymapbox()
                )
                fig.update_layout(mapbox_style="carto-positron",
                                mapbox_center_lon=51.368642, 
                                mapbox_center_lat=35.718167,
                                mapbox_zoom=12)

                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650)
                return [dcc.Graph(figure=fig)
                   ]


if __name__ == '__main__':
    app.run_server(debug=False)
