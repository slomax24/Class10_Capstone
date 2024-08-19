# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
    dcc.Dropdown(id='site-dropdown', 
        options=[
            {'label':'All SItes','value':'ALL'},
            {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
            {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
            {'label':'KSC LC-39A','value':'KSC LC-39A'},
            {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
        marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
        value=[min_payload,max_payload]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value')
)
def success_pie_chart(entered_site):
    if entered_site=='ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
        title='Total Successful Launches by Site')
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site'] == entered_site]
        fig=px.pie(filtered_df, names='class',
        title='Total Successful Launches by Site {}'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property='value')])
def success_payload_scatter_chart(entered_site, payload_range):
    filtered_df=spacex_df[(spacex_df['Payload Mass (kg)']>=payload_range[0])&
                            (spacex_df['Payload Mass (kg)']<=payload_range[1])]
    if entered_site=='ALL':
        fig=px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color="Booster Version Category",
                        label={'Payload Mass (kg)':'Payload Mass', 'class':'Launch Outcome'},
                        title='Payload Mass vs Launch Outcome')
    else:
        filtered_df=filtered_df[filtered_df['Launch Site']== entered_site]
        fig=px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color="Booster Version Category",
                        label={'Payload Mass (kg)':'Payload Mass', 'class':'Launch Outcome'},
                        title='Payload Mass vs Launch Outcome for {}'.format(entered_site))
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
