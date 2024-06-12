import pandas as pd
import os
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import dash_table
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy import text
from dash.exceptions import PreventUpdate
from flask_caching import Cache
import random

# Instantiate the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN],suppress_callback_exceptions=True)

# Create a Flask cache
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple'  # Use 'redis' or other type of cache for production
})
CACHE_TIMEOUT = 300  # Cache timeout in seconds

#creating a connection to my database ,postgres for this case
con_string =  "postgresql://root:root@172.21.0.2:5432/covidnineteen"

#create a engine
engine = create_engine(con_string, poolclass=NullPool)
engine.connect()

#opening connecton to get the countries data
with engine.connect() as connection:
    t = text('''
             select
	            who_region
             from dim_who_region
             ''')
    df = pd.read_sql(t, con=engine)
    

# Create the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home",style={'color': 'darkblue'})),
        dbc.NavItem(dbc.NavLink("About", href='/about',style={'color': 'darkblue'})),
        dbc.NavItem(dbc.NavLink('Contact Us', href='/contact-us',style={'color': 'darkblue'}))
    ],
    brand="Covid Nineteen Analytics",
    brand_href="#",
    color="FF1493",
    dark=False,
    brand_style={'color': 'darkblue'}  # Add style to the brand text
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Copyright © 2024 Covid Nineteen Analytics | All Rights Reserved', className='mr-2',style={'color':'darkblue'}),
                    # html.A(
                    #     html.I(className='fab fa-github-square mr-1'), href='https://github.com/your-github-account',
                    #     target='_blank', style={'color': 'darkblue'}
                    # ),
                    # html.A(
                    #     html.I(className='fab fa-linkedin mr-1'), href='https://www.linkedin.com/your-linkedin-account',
                    #     target='_blank', style={'color': 'darkblue'}
                    # ),
                    # html.A(
                    #     html.I(className='fas fa-envelope-square mr-1'), href='mailto:your-email@example.com',
                    #     style={'color': 'darkblue'}
                    # ),
                ],
                className='lead'
            )
        )
    )
)


#define my applications layout
home_layout = html.Div([
    html.P('Welcome to Covid-19 Analytics Dashboard',style={'color':'darkblue'}),
    dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4('Cases', style={'color':'#0000FF', 'textAlign':'center'}),
                html.P(id='total-cases', children=0, style={'textAlign':'center'})
            ])
        ])
    ]),
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4('Deaths', style={'color':'#0000FF', 'textAlign':'center'}),
                html.P(id='total-deaths', children=0, style={'textAlign':'center'})
            ])
        ])
    ]),
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4('Recovered', style={'color':'#0000FF', 'textAlign':'center'}),
                html.P(id='total-recovered', children=0, style={'textAlign':'center'})
            ])
        ])
    ]),
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4('New Cases', style={'color':'#0000FF', 'textAlign':'center'}),
                html.P(id='total-new-cases', children=0, style={'textAlign':'center'})
            ])
        ])
    ]),
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4('New Recovered', style={'color':'#0000FF', 'textAlign':'center'}),
                html.P(id='total-new-recovered', children=0, style={'textAlign':'center'})
            ])
        ])
    ]),
]),
html.Br(),
html.Br(),
dcc.Graph(id='country-choropleth'),
html.Br(),
html.Br(),
html.Div(
        dcc.Markdown(
            """
            - The region with the highest number of COVID-19 cases is Americas with a total of 8,839,286 cases
            - The region with the highest number of COVID-19 cases is Western Pacific with a total of 292,428 cases
            """
        ),
        style={'color': 'darkblue'}
    ),
# dcc.Markdown("""
# ##### - The region with the highest number of covid nineteen cases is Americas with a total of 8839286 cases
# ##### - The region with the highest number of covid nineteen cases is Western Pacific with a total of 292428 cases
#              """,style={'color': 'darkblue'}),
html.Br(),
html.Br(),
dbc.Row([
    dbc.Col([
        dcc.Dropdown(id='who-region-dropdown',options=[{
            'label': region,
            'value': region
        } for region in df['who_region'].unique()],placeholder='Select region'),
        html.Br(),
        html.Br(),
        dcc.Graph(id='cases-barchart'),
        html.Br(),
        html.Br(),
        dcc.Graph(id='death-countries-heatmap'),
        html.Br(),
        html.Br(),
        dbc.Col([
            dcc.Graph(id='one-week-change-per-region')

        ])
        
        
    ])
])



])

about_layout = html.Div([
    html.H3('About Covid Nineteen Analytics', style={'color': 'darkblue'}),
    html.P(
        "Covid Nineteen Analytics is a dashboard designed to provide insights and visualizations "
        "related to the Covid-19 pandemic. Our goal is to help users better understand the "
        "impact of the virus globally and regionally, as well as track key metrics such as "
        "total cases, deaths, and recoveries."
    ),
    html.H4('Our Team', style={'color': 'darkblue'}),
    html.Ul([
        html.Li('Ahona Victor - Lead Developer'),
        html.Li('Ahona Victor - Data Analyst'),
        html.Li('Ahona Victor - Data Engineer'),
        html.Li('Ahona Victor- BI Analyst'),
        html.Li('Kish Kishoyian - UI/UX Designer'),
        # Add more team members as needed
    ]),
    html.H4('Acknowledgments', style={'color': 'darkblue'}),
    html.P(
        "We would like to acknowledge the contributions of the open-source community and "
        "the various data sources that have made this project possible. Special thanks to "
        "the World Health Organization (WHO) and Johns Hopkins University for providing "
        "valuable Covid-19 data."
    ),
    html.H4('Technical Details', style={'color': 'darkblue'}),
    html.P(
        "Covid Nineteen Analytics is built using Dash, a Python web framework for building "
        "analytical web applications. We use Plotly for data visualization and SQLAlchemy for "
        "database interactions. The application is hosted on a Flask server and deployed using "
        "Heroku."
    )
]),

contact_layout = html.Div([
    # html.H2("Contact Us", style={'text-align': 'center'}),
    html.H4("Contact Us", style={'color': 'darkblue'}),
    html.P("If you have any questions or feedback, please feel free to reach out to us.", style={'color':'darkblue'}),
    html.Div([
        html.H4("Contact Information",style={'color':'darkblue'}),
        html.P("Email: contact@example.com",style={'color':'darkblue'}),
        html.P("Phone: +1234567890",style={'color':'darkblue'}),
        html.P("Address: 123 Main Street, City, Country",style={'color':'darkblue'})
    ], style={'margin': '20px auto', 'width': '50%'}),
    html.Div([
        #
        dcc.Input(placeholder='Your Name', type='text', style={'margin': '10px 0', 'display': 'block','color':'darkblue', 'width': '100%','height': '30px'}),
        dcc.Input(placeholder='Your Email', type='email', style={'margin': '10px 0', 'display': 'block','color':'darkblue', 'width': '100%','height': '30px'}),
        dcc.Textarea(placeholder='Your Message', style={'margin': '10px 0', 'display': 'block','color':'darkblue', 'width': '100%'}),
        dbc.Button("Send Message", color="primary", className="mr-2", style={'margin': '10px 0', 'display': 'block'})
    ], style={'margin': '20px auto', 'width': '50%', 'text-align': 'center'})
])

# Make the layout
app.layout = html.Div([
    navbar,
    dcc.Location(id='url',refresh=False), #most important 
    html.Div(id='page-content'), #displays the entire layout of my application,
    dcc.Interval(
      id='interval-component',
      interval=60000,  # Update every second
      n_intervals=0
),
html.Div(style={'height': '250px'}),
footer
])               #,style={'backgroundColor': '#3CB371'}),  #style={'backgroundColor': '#C0C0C0'})
#CALLBACK FUNCTIONS
#callback function for the app layout
@app.callback(Output('page-content','children'),
              Input('url','pathname'))
def display_the_necessary_pages(pathname):
    if pathname is None:
        raise PreventUpdate
    if pathname == "/home":
        return home_layout
    elif pathname == "/about":
        return about_layout
    else:
        return contact_layout
    
#callback functions for my kpis
#total-cases
@app.callback(Output('total-cases','children'),
              [Input('interval-component','n_intervals'),
               Input('who-region-dropdown','value')])
def update_total_cases(n, region):
    if n is None:
        raise PreventUpdate

    # get the total cases confirmed data
    with engine.connect() as connection:
        if region:
            t = text(
                '''
                select
                   sum(total_cases_confirmed) as total_cases
                from dim_confirmed as c
                left join dim_country as cn on c.rn = cn.rn
                left join dim_who_region as w on cn.rn = w.rn
                where w.who_region = :region
                '''
            )
            # Provide the value for the region parameter
            df = pd.read_sql(t, con=engine, params={"region": region})
        else:
            t = text(
                '''
                select
                    sum(total_cases_confirmed) as total_cases
               from dim_confirmed
                '''
            )
            df = pd.read_sql(t, con=engine)

        if df is None:
            return ''
        else:
            total_cases = df['total_cases'].iloc[0]
        return total_cases
#total-deaths
@app.callback(
    Output('total-deaths', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('who-region-dropdown', 'value')]
)
def update_total_deaths(n, region):
    if n is None:
        raise PreventUpdate
    # Get the total deaths that occurred
    with engine.connect() as connection:
        if region:
            t = text('''
                     select
                        sum(total_deaths) as total_deaths
                     from dim_deaths as d
                     left join dim_who_region as w on d.rn = w.rn
                     where w.who_region = :region
                     ''')
            df = pd.read_sql(t, con=engine, params={"region": region})
        else:
            t = text(
                '''
                select
                    sum(total_deaths) as total_deaths
                from dim_deaths
                '''
            )
            df = pd.read_sql(t, con=engine)
        if df is None:
            return ''
        else:
            total_deaths = df['total_deaths'].iloc[0]
        return total_deaths
    
#total-recovered
@app.callback(Output('total-recovered','children'),
              [Input('interval-component','n_intervals'),
               Input('who-region-dropdown','value')])
def update_total_recovered(n,region):
    if n is None:
        raise PreventUpdate
    #get the total recovered data
    with engine.connect() as connection:
        if region:
              t = text(
                  '''
                  select
                      sum(d.totally_recovered) as totally_recovered
                  from dim_recovered as d
                  left join dim_who_region as w on w.rn = d.rn
                  where who_region = :region
                  '''
              )
        
              df = pd.read_sql(t,con=engine,params={"region": region})
        else:
            t = text(
                '''
                select
                    sum(totally_recovered) as totally_recovered
                from dim_recovered
                '''
            )
            df = pd.read_sql(t,con=engine)

        if df is None:
            return ''
        else:
            totally_recovered = df['totally_recovered']
        return totally_recovered
    
#total-new-cases
@app.callback(Output('total-new-cases','children'),
              [Input('interval-component','n_intervals'),
               Input('who-region-dropdown','value')])
def update_total_new_cases(n,region):
    if n is None:
        raise PreventUpdate
    #get the total-new-cases-data
    with engine.connect() as connection:
        if region:
            t = text('''
                     select
                          sum(d.total_new_cases) as total_new_cases
                     from dim_new_cases d
                     left join dim_who_region w on w.rn = d.rn
                     where who_region = :region
                     ''')
            df = pd.read_sql(t, con=engine, params={"region": region})
        else: 
             t = text('''
                 select 
	              sum(total_new_cases) as total_new_cases
                 from dim_new_cases
                 ''')
             df = pd.read_sql(t, con=engine)
       
        if df is None:
            return ''
        else:
            total_new_cases = df['total_new_cases'].iloc[0]
        return total_new_cases
    
#total-new-recovered
@app.callback(Output('total-new-recovered','children'),
              [Input('interval-component','n_intervals'),
               Input('who-region-dropdown','value')])
def update_total_new_recovered(n,region):
    if n is None:
        raise PreventUpdate
    #get the total-new-recovered-data
    with engine.connect() as connection:
        if region:
            t = text('''
                     select
                         sum(total_new_recovered) as total_new_recovered
                     from dim_new_recovered d
                     left join dim_who_region w on w.rn = d.rn
                     where who_region = :region
                     ''')
            df = pd.read_sql(t, con=engine, params={"region": region})
        else:
            t = text('''
                  select
	                  sum(total_new_recovered) as total_new_recovered
                  from dim_new_recovered

                 ''')
            df = pd.read_sql(t,con=engine)

        if df is None:
            return ''
        else:
            total_new_recovered = df['total_new_recovered'].iloc[0]
        return total_new_recovered
    

#callback function for the  choropleth plot
@app.callback(Output('country-choropleth','figure'),
              Input('interval-component','n_intervals'))
def plot_choropleth(n):
    if n is None:
        raise PreventUpdate
    #get the data to plot choropleth;country and total confirmed cases
    with engine.connect() as connection:
        t = text('''
                 select
	                 c.country as country,
	                 p.total_cases_confirmed as total_cases_confirmed	 
                 from dim_confirmed p
                 left join dim_country c on p.rn = c.rn
                 group by country,total_cases_confirmed
                 order by total_cases_confirmed desc
                 ''')
        df = pd.read_sql(t,con=engine)
        if df is None:
            return ''
        else:
          
           fig = px.choropleth(
                     df,
                     locations='country',  # Use country names for locations
                     locationmode='country names',  # Specify that the locations are country names
                     color='total_cases_confirmed',
                     hover_name='country',
                     hover_data={'total_cases_confirmed': True},
                     color_continuous_scale='Viridis',  # Change the color scale here
                     title='Total COVID-19 Cases Confirmed per Country',
                     height=650
                    )

    # Update layout for better interactivity and aesthetics
           fig.update_layout(
                title={
                 'text': 'Total COVID-19 Cases Confirmed per Country',
                 'font': {
                 'color': 'darkblue'  # Set the title font color to black (or dark)
            }
           },
           geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
           ),
            coloraxis_colorbar=dict(
            title='Total Cases'
          )
    )

    return fig
    
#callback function to plot country cases barchart
@app.callback(Output('cases-barchart','figure'),
              Input('who-region-dropdown','value'))
def plot_cases_barchart(region):
    with engine.connect() as connection:
        t = '''
            select
                c.country AS country,
                w.who_region AS who_region,
                d.total_cases_confirmed AS total_cases_confirmed
            from dim_who_region w
           left join dim_country c ON w.rn = c.rn
           left join dim_confirmed d ON w.rn = d.rn
            group by country, who_region, total_cases_confirmed
        '''
        df = pd.read_sql(t, con=engine)

    if region is None:
        # If no region is selected, select a random region
        random_region = random.choice(df['who_region'].unique())
        df_region = df[df['who_region'] == random_region]
    else:
        df_region = df[df['who_region'] == region]

    if df_region.empty:
        return {}

    # Plot bar chart
    fig = px.bar(df_region, x='country', y='total_cases_confirmed', title=f'Total Cases Confirmed for {region} region')

    # Update layout
    fig.update_layout(
        xaxis_title='Countries',
        yaxis_title='Total Cases Confirmed',
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.1,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='darkblue'),
    )
    fig.update_traces(marker_color='blue',width=0.8)
    # fig.update_traces(marker=dict(colorscale='Viridis'), width=0.8)

    return fig

#callback function for the death-countries-heatmap
@app.callback(Output('death-countries-heatmap','figure'),
              Input('interval-component','n_intervals'),
              Input('who-region-dropdown','value'))
def plot_deaths_and_countries_heatmap(n,region):
    if n is None:
        return "You you gotta work for this buddy, watchout!!!"
    #connecting to the datasource to get the deaths and countries data
    with engine.connect() as connection:
        if region:
             t = text('''
                      select
	                     c.country as country,
	                     w.who_region as region,
	                     d.total_deaths as deaths
                      from dim_deaths d
                      left join dim_country c on d.rn = c.rn
                      left join dim_who_region w on w.rn = c.rn
                      where w.who_region = :region
                      group by country,deaths,region
                      order by deaths desc
                      ''')
             df = pd.read_sql(t, con=engine, params={"region": region})
        else:
             t = text('''
                 select
	                c.country as country,
	                d.total_deaths as deaths
                 from dim_deaths d
                 left join dim_country c on d.rn = c.rn
                 group by country,deaths
                 order by deaths desc
                 ''')
             df = pd.read_sql(t,con=engine)
        if not df.empty:
             fig = px.density_heatmap(df, x='country', y='deaths',
                                     title='Total Deaths by Country',
                                     color_continuous_scale='Viridis')
             fig.update_layout(
                # paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                # plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area background
                # font_color="white",             # White font color
                # xaxis_title="Country",          # X-axis title
                # yaxis_title="Deaths",
                xaxis_title_font_color="darkblue",  # Dark blue X-axis title color
                yaxis_title_font_color="darkblue",   # Dark blue Y-axis title color
                title_font_color="darkblue"           # Y-axis title
            )
        return fig

@app.callback(Output('one-week-change-per-region', 'figure'),
              [Input('who-region-dropdown', 'value'),
               Input('interval-component', 'n_intervals')])
def plot_pie_chart_for_one_week_change_per_region(region, n):
    if n is None:
        raise PreventUpdate

    # Connecting to the data source to get the one week change data and region data
    with engine.connect() as connection:
        if region:
            t = text('''
                     select
                        c.country as country,
                        w.who_region as region,
                        sum(d.one_week_change) as one_week_change
                     from dim_who_region w
                     left join dim_one_week_change d on w.rn = d.rn
                     left join dim_country c on w.rn = c.rn
                     where w.who_region = :region
                     group by region,country
                     ''')
            df = pd.read_sql(t, con=engine, params={"region": region})
        else:
            t = text('''
                     select
                        c.country as country,
                        w.who_region as region,
                        sum(d.one_week_change) as one_week_change
                     from dim_who_region w
                     left join dim_one_week_change d on w.rn = d.rn
                     left join dim_country c on w.rn = c.rn
                     group by region,country
                     ''')
            df = pd.read_sql(t, con=engine)

            if not df.empty:
                # Randomly highlight a region if no region is selected
                #df['highlight'] = 'Other'
                random_region = random.choice(df['region'].unique())
                df.loc[df['region'] == random_region] #, 'highlight'] = 'Randomly Selected Region'

    if not df.empty:
        fig = px.pie(df, values='one_week_change', names='country',
                     title='One Week Change per Region',
                     color='country',  # Use the 'region' column to color the pie chart
                     #color_discrete_map={'Randomly Selected Region': 'blue', 'Other': 'lightblue'},
                     color_discrete_sequence=px.colors.sequential.Viridis)
         # Update layout for larger figure and better text properties
        fig.update_layout(
            # width=800,  # Increase the width
            # height=800,  # Increase the height
            title_font_color='darkblue',
            title_font_size=20,  # Increase the title font size
            legend=dict(
                font=dict(size=15)  # Increase the legend font size
            )
        )
        
        # Update the text properties for the pie chart
        fig.update_traces(
            textposition='inside',  # Position the text inside the slices
            textinfo='percent+label',  # Show percentage and label
            textfont_size=15  # Increase the text font size
        )
        return fig
# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
