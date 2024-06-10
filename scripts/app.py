import dash
import pandas as pd
import os
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool,QueuePool
import plotly.express as px

# Instantiate the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
#app.title = "COVID-19 Dashboard"
app.config.suppress_callback_exceptions = True  # Suppress callback exceptions

# Connecting to the datasource: PostgreSQL
connection_string = "postgresql://root:root@172.20.0.2:5432/covidnineteen"
engine = create_engine(connection_string, poolclass=QueuePool)

# Create a connection instance if needed
with engine.connect() as connection:
    t = text('SELECT * FROM covid_datatable')
    df = pd.read_sql(t, con=engine)

# Define the navbar with inline styles for the brand and background color
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", style={"color": "#FFFFFF"})),
        dbc.NavItem(dbc.NavLink("Analytics", href="/analytics", style={"color": "#FFFFFF"})),
        dbc.NavItem(dbc.NavLink("Archives", href="/archives", style={"color": "#FFFFFF"})),
    ],
    brand="COVID-19 Dashboard",
    brand_href="/",
    style={
        "backgroundColor": "transparent",  # Transparent background
        "boxShadow": "none"  # Remove shadow
    },
    brand_style={"color": "#FFFFFF"} 
)

# Define the home layout with a background image
home_layout = html.Div(
    style={
        "backgroundImage": "url('../assets/covid_19.jpg')",  # Reference the local image
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "color": "white",
        "textAlign": "center"
    },
    children=[
        html.Div([
            html.P("Welcome to the COVID-19 Dashboard", style={'fontSize':'35px'})
        ])
    ]
)

# Define the analytics layout
analytics_layout = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Cases Confirmed', style={'textAlign':'center'}),
                    html.P(id='cases-confirmed', children='...', style={'textAlign':'center','color':'#F8F8FF ','fontSize':'26px'})
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Deaths', style={'textAlign':'center'}),
                    html.P(id='deaths', children='...',style={'textAlign':'center','color':'#F8F8FF ','fontSize':'26px'})
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Recovered', style={'textAlign':'center'}),
                    html.P(id='recovered', children='...', style={'textAlign':'center','color':'#F8F8FF ','fontSize':'26px'})
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('New Cases', style={'textAlign':'center'}),
                    html.P(id='new-cases', children='...',style={'textAlign':'center','color':'#F8F8FF ','fontSize':'26px'})
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('New Deaths', style={'textAlign':'center'}),
                    html.P(id='new-deaths', children='...',style={'textAlign':'center','color':'#F8F8FF ','fontSize':'26px'})
                ])
            ])
        ])
    ]),
    html.Br(),
    html.Br(),
    #draws the map of the entire world showing the distribution of covid nineteen cases
    # dbc.Row([
    #     dbc.Col([
    #         dcc.Graph(id='map-world')
    #     ])
    # ])
    dbc.Row([
        dbc.Col([
            dcc.Dropdown([])
        ])
    ])
])

# Define the archives layout
archives_layout = html.Div([
    html.H1("Archives Page"),
    html.P("Archives content goes here."),
    # Add your archives content here
])

# Define the app layout for the whole application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every minute
        n_intervals=0
    )
])

# Callback function to update page layout based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/analytics':
        return analytics_layout
    elif pathname == '/archives':
        return archives_layout
    else:
        return home_layout
    
# Callback function to update the "Cases Confirmed" card with info from the database
@app.callback(
    Output('cases-confirmed', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_total_cases_confirmed(n):
    if not n:
        raise PreventUpdate
    with engine.connect() as connection:
        t = text('''
            WITH stg_confirmed_cases AS (
                SELECT "Confirmed" AS confirmed
                FROM covid_datatable
            )
            SELECT SUM(confirmed) AS total_cases_confirmed
            FROM stg_confirmed_cases
        ''')
        df = pd.read_sql(t, con=engine)
        if not df.empty:
             total_cases_confirmed = df['total_cases_confirmed'].iloc[0]
        return total_cases_confirmed
    
#callback function to update deaths
@app.callback([Output('deaths','children')],
               [Input('interval-component','n_intervals')])
def update_total_deaths(n):
    if not n:
        raise PreventUpdate
    with engine.connect() as connection:
        t = text(
            '''
        WITH stg_deaths as(
           SELECT
               "Deaths" as deaths
           FROM covid_datatable
        )
        SELECT
           SUM(deaths) as total_deaths
        FROM stg_deaths
            '''   
        )
        df = pd.read_sql(t, con=engine)
        if not df.empty:
            total_deaths = df['total_deaths'].iloc[0]
        return [total_deaths]
    
#callback function to update recovered
@app.callback(Output('recovered','children'),
              Input('interval-component','n_intervals'))
def update_recovered_cases(n):
    if not n:
        raise PreventUpdate
    with engine.connect() as connection:
        t = text(
            '''
            WITH stg_recovered as (
            SELECT
               "Recovered" as recovered
            FROM covid_datatable
            )
            SELECT
              SUM(recovered) total_recovered_cases
            FROM stg_recovered
            '''
        )
        df = pd.read_sql(t, con=engine)
        if not df.empty:
            total_recovered = df['total_recovered_cases'].iloc[0]
        return total_recovered

#callback fncton to update new cases
@app.callback(Output('new-cases','children'),
              Input('interval-component','n_intervals'))
def update_new_cases(n):
    if not n:
        raise PreventUpdate
    with engine.connect() as connection:
         t = text('''
            WITH stg_new_cases as (
             SELECT
                "New cases" as new_cases
             FROM covid_datatable
             )
             SELECT 
               SUM(new_cases) as total_new_cases
             FROM stg_new_cases

             ''')
         df = pd.read_sql(t,con=engine)
         if df is not None:
             total_new_cases = df['total_new_cases'].iloc[0]
         return [total_new_cases]
   
  
#callback function to update new deaths
@app.callback(Output('new-deaths','children'),
              Input('interval-component','n_intervals'))
def update_new_deaths(n):
    if not n:
        raise PreventUpdate
    with engine.connect() as connection:
        t = text('''
                 SELECT
                    SUM("New deaths") as new_deaths
                 FROM covid_datatable
                  ''')
        df = pd.read_sql(t, con=engine)
        if not df.empty:
            new_deaths = df['new_deaths']
            return new_deaths
        
#callback function for the map-world graph
@app.callback(Output('map-world','figure'),
              Input('interval-component','n_intervals'))
def plot_world_map(n):
    if n is None:
        raise PreventUpdate
    with engine.connect() as connection:
        t = text('''
                 SELECT
                     "Country/Region" as country,
                     "Confirmed" as cases_confirmed
                 FROM covid_datatable
                 GROUP BY country,cases_confirmed
                 ''') 
        df = pd.read_sql(t, con=engine)
        if df is not None:
            # fig = px.choropleth(df,
            #                     locations='country',
            #                     title='Covid Cases Per Country',
            #                     hover_name='country',
            #                     color_continuous_scale='cividis',
            #                     height=650
            #                     )
            # fig.layout.geo.showframe = False
            # fig.layout.geo.showcountries = True
            # fig.layout.geo.projection.type= 'natural earth'
            # fig.layout.geo.lataxis.range = [-53, 76]
            # fig.layout.geo.lonaxis.range = [-137, 168]
            # fig.layout.geo.landcolor = 'white'
            # fig.layout.geo.bgcolor = '#E5ECF6'
            # fig.layout.paper_bgcolor = '#E5ECF6'
            # fig.layout.geo.countrycolor = 'gray'
            # fig.layout.geo.coastlinecolor = 'gray'
            fig = px.line(df,
                          )


        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
