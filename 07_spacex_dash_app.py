# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os 
#os.chdir(/Users/rodrigo_vargas/Documents/GitHub/IBM_capstone/)

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("/Users/rodrigo_vargas/Documents/GitHub/IBM_capstone//spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
                 ],
                 value = 'ALL',
                 placeholder = "Select a Launch Site",
                 searchable = True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id = 'success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id = 'payload-slider',
                    min = min_payload, max=max_payload, step=1000,
                    marks = {i: f'{i}' for i in range(int(min_payload), int(max_payload)+1, 1000)},
                    value = [min_payload, max_payload]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        filtered_df = spacex_df.copy()
        counts = filtered_df['Booster Version Category'].value_counts()
        fig = px.pie(values = counts, 
                     names = counts.index,
                     title = 'Total Successful Launches By Site')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site)]
        counts = filtered_df['class'].value_counts()
        fig = px.pie(values= counts, 
                     names = counts.index,
                     title=f'Successful Launches Ratio for Site {entered_site}')
    return fig

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()