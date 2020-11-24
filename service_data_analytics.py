# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 18:44:31 2020

@author: Tejo
"""

# importing the libraries
import pandas as pd
import webbrowser
# !pip install dash
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc

import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo

# !pip install dash-bootstrap-components
import dash_bootstrap_components as dbc
import dash_table as dt


# Global variables
# [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name = None


def load_data():

    # the variable inside a function is local by default.
    call_dataset_name = "Call_data.csv"
    service_dataset_name = "Service_data.csv"
    device_dataset_name = "Device_data.csv"

    # We use a global keyword for a variable which is inside a function so that it can be modified.
    global call_data
    call_data = pd.read_csv(call_dataset_name)

    global service_data
    service_data = pd.read_csv(service_dataset_name)

    global device_data
    device_data = pd.read_csv(device_dataset_name)

    # [{'label': '2019-06-20', 'value': '2019-06-20'} ]
    global start_date_list
    temp_list = sorted(call_data['date'].dropna().unique().tolist())
    start_date_list = [{"label": str(i), "value": str(i)} for i in temp_list]

    # [{'label': '2019-06-20', 'value': '2019-06-20'} ]
    global end_date_list
    end_date_list = [{'label': str(i), 'value': str(i)} for i in temp_list]

    # [{'label': 'Hourly', 'value': 'Hourly'} ]
    temp_list = ["Hourly", "Daywise", "Weekly"]
    global report_type_list
    report_type_list = [{"label": str(i), "value": str(i)} for i in temp_list]


def open_browser():
    # Open the default web browser
    webbrowser.open_new('http://127.0.0.1:8050/')

# Layout of your page


def create_app_ui():
    # Create the UI of the Webpage here
    main_layout = html.Div(
        children=[
            html.Div(id='heading-div', children=[
                html.H1(id='heading', children='CDR Analysis with Insights', style={'text-align': 'center', 'color': 'white'})],
                style={'background': 'black', 'padding': 10}),

            dcc.Tabs(id="Tabs", value="Call Analytics tool", children=[

                dcc.Tab(label="Call Analytics tool", id="Call Analytics tool", value="Call Analytics tool",
                        children=[
                            dcc.Dropdown(
                                id='start-date-dropdown',
                                options=start_date_list,
                                placeholder="Select Starting Date here",
                                value="2019-06-20"
                            ),

                            dcc.Dropdown(
                                id='end-date-dropdown',
                                options=end_date_list,
                                placeholder="Select Ending Date here",
                                value="2019-06-25"
                            ),


                            dcc.Dropdown(
                                id='group-dropdown',
                                placeholder="Select group here",
                                multi=True
                            ),


                            dcc.Dropdown(
                                id='Report-type-dropdown',
                                options=report_type_list,
                                placeholder="Select Report Type",
                                value="Hourly"
                            ),

                            html.Br(),

                            dcc.Loading(
                                html.Div(id='visualization-object', children='Graph, Card, Table'))
                        ]),
                dcc.Tab(label="Device Analytics tool",
                        id="Device Analytics tool", value="Device Analytics tool",
                        children = [
                            dcc.Dropdown(id='Device-Analytics-Dropdown',
                                             options=start_date_list,
                                             placeholder='Select Date'),
                            html.Br(),
                            dcc.Loading(
                                html.Div(id = 'Device-Piechart', style={'marginLeft': '30%'})
                                )
                        ]),
                dcc.Tab(label="Service Analytics tool", id="Service Analytics tool", value="Service Analytics tool",
                        children = [
                            dcc.Dropdown(id='Service-Analytics-Dropdown',
                                             options=start_date_list,
                                             placeholder='Select Date'),
                            html.Br(),
                            dcc.Loading(
                                html.Div(id = 'Service-Piechart', style={'marginLeft': '30%'})
                                )
                            ])]
            )
        ],
        style = {'padding': 35})
    return main_layout


def create_card(title, content, color):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, style = {'text-align': 'center'}),
                html.Br(),
                html.Br(),
                html.H2(content, style = {'text-align': 'center'}),
                html.Br(),
            ]
        ),
        color=color, inverse=True,

    )
    return(card)

@app.callback(
    Output('Service-Piechart', 'children'),
    [
    Input('Service-Analytics-Dropdown', 'value') 
    ]    
    )
def update_service_piechart(date):
    new_data = service_data.groupby('FeatureEventDate')['FeatureName'].value_counts().reset_index(name="count")
    pie_data = new_data[new_data['FeatureEventDate']==date]
    labels = [i for i in pie_data['FeatureName']]
    values = [int(i) for i in pie_data['count']]
    
    figure = {'data' : [go.Pie(labels=labels, values=values)],
              'layout': go.Layout(height = 900, width = 900, autosize = False)
              }
    return dcc.Graph(figure = figure)
    
@app.callback(
    Output('Device-Piechart', 'children'),
    [
    Input('Device-Analytics-Dropdown', 'value') 
    ]    
    )
def update_device_piechart(date):
    
    
    dd_data = device_data.replace(to_replace = r'^Polycom(.*$)', value = 'Polycom', regex = True)
    dd_data = dd_data.replace(to_replace = r'(.*)Windows(.*$)', value = 'Windows', regex = True)
    dd_data = dd_data.replace(to_replace = r'^Yealink(.*$)', value = 'Yealink', regex = True)
    dd_data = dd_data.replace(to_replace = r'(.*)Android(.*$)', value = 'Android', regex = True)
    dd_data = dd_data.replace(to_replace = r'(.*)iPhone(.*$)', value = 'iPhone', regex = True)
    dd_data = dd_data.replace(to_replace = r'(.*)Aastra(.*$)', value = 'Aastra', regex = True)
    dd_data = dd_data.replace(to_replace = r'(.*)Mac(.*$)', value = 'Mac', regex = True)
    dd_data = dd_data.replace(to_replace = r'^Algo(.*$)', value = 'Algo', regex = True)
    dd_data = dd_data.replace(to_replace = r'^Linksys(.*$)', value = 'Linksys', regex = True)
    dd_data = dd_data.replace(to_replace = r'^CS2000(.*$)', value = 'CS2000 NGSS', regex = True)
    new_data = dd_data.groupby('DeviceEventDate')['UserDeviceType'].value_counts().reset_index(name="count")
    
    pie_data = new_data[new_data['DeviceEventDate']==date]
    labels = [i for i in pie_data['UserDeviceType']]
    values = [int(i) for i in pie_data['count']]
    
    figure = {'data' : [go.Pie(labels=labels, values=values, hole = .3)],
              'layout': go.Layout(height = 800, width = 800, autosize = False)
              }
    
    return dcc.Graph(figure = figure)



# Callback of your page
@app.callback(
    Output('visualization-object', 'children'),
    [
        Input('start-date-dropdown', 'value'),
        Input('end-date-dropdown', 'value'),
        Input("group-dropdown", 'value'),
        Input('Report-type-dropdown', 'value'),
    ]
)
def update_app_ui(start_date, end_date, group, report_type):

    print("Data Type of start_date value = ", str(type(start_date)))
    print("Data of start_date value = ", str(start_date))

    print("Data Type of end_date value = ", str(type(end_date)))
    print("Data of end_date value = ", str(end_date))

    print("Data Type of group value = ", str(type(group)))
    print("Data of group value = ", str(group))

    print("Data Type of report_type value = ", str(type(report_type)))
    print("Data of report_type value = ", str(report_type))

    # Filter the data as per the selection of the drop downs

    call_analytics_data = call_data[(call_data["date"] >= start_date) & (
        call_data["date"] <= end_date)]

    if group == [] or group is None:
        pass
    else:
        call_analytics_data = call_analytics_data[call_analytics_data["Group"].isin(
            group)]

    graph_data = call_analytics_data
    # Group the data based on the drop down
    if report_type == "Hourly":
        graph_data = graph_data.groupby("hourly_range")[
            "Call_Direction"].value_counts().reset_index(name="count")
        x = "hourly_range"

        content = call_analytics_data["hourly_range"].value_counts().idxmax()
        title = "Busiest Hour"

    elif report_type == "Daywise":
        graph_data = graph_data.groupby(
            "date")["Call_Direction"].value_counts().reset_index(name="count")
        x = "date"

        content = call_analytics_data["date"].value_counts().idxmax()
        title = "Busiest Day"

    else:
        graph_data = graph_data.groupby("weekly_range")[
            "Call_Direction"].value_counts().reset_index(name="count")
        x = "weekly_range"

        content = call_analytics_data["weekly_range"].value_counts().idxmax()
        title = "Busiest WeekDay"

    # Graph Section
    graph_dataf = call_analytics_data.groupby(x)['Call_Direction'].value_counts().unstack(fill_value=0).reset_index()
    figure = {'data': [go.Scatter(x = graph_dataf[x],
                                  y = graph_dataf[dir],
                                  mode = 'lines+markers',
                                  text = graph_data["Call_Direction"],
                                  fill='tozeroy') for dir in graph_data['Call_Direction'].unique()], 
    
                'layout': go.Layout(title = 'Call Analytics',
                                    xaxis = {'title': 'Hourly Range'},
                                    yaxis = {'title': 'Count'},
                                    template = 'plotly_dark')
            }
    
    # Card Section
    total_calls = call_analytics_data["Call_Direction"].count()
    card_1 = create_card("Total Calls", total_calls, "success")

    incoming_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"] == "Incoming"].count(
    )
    card_2 = create_card("Incoming Calls", incoming_calls, "primary")

    outgoing_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"] == "Outgoing"].count(
    )
    card_3 = create_card("Outgoing Calls", outgoing_calls, "primary")

    missed_calls = call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"] == 3].count(
    )
    card_4 = create_card("Missed Calls", missed_calls, "danger")

    max_duration = call_analytics_data["duration"].max()
    card_5 = create_card("Max Duration", f'{max_duration} min', "dark")

    card_6 = create_card(title, content, "primary")

    graphRow0 = dbc.Row([dbc.Col(md=2), dbc.Col(id='card1', children=[card_1], md=3), dbc.Col(md=2), dbc.Col(id='card2', children=[card_2], md=3), dbc.Col(md=2)])
    graphRow1 = dbc.Row([dbc.Col(md=2), dbc.Col(id='card3', children=[card_3], md=3), dbc.Col(md=2), dbc.Col(id='card4', children=[card_4], md=3), dbc.Col(md=2)])
    graphRow2 = dbc.Row([dbc.Col(md=2), dbc.Col(id='card5', children=[card_5], md=3), dbc.Col(md=2), dbc.Col(id='card6', children=[card_6], md=3), dbc.Col(md=2)])

    cardDiv = html.Div(
        [graphRow0, html.Br(), graphRow1, html.Br(), graphRow2],
        style = {'marginTop': 30, 'marginBottom': 30})

    # Data Table Section

    datatable_data = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])[
        "Call_Direction"].value_counts().unstack(fill_value=0).reset_index()

    if call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"] == 19].count() != 0:
        datatable_data["Missed Calls"] = call_analytics_data.groupby(
            ["Group", "UserID", "UserDeviceType"])["Missed Calls"].value_counts().unstack()[3]
    else:
        datatable_data["Missed Calls"] = 0

    datatable_data["Total_call_duration"] = call_analytics_data.groupby(
        ["Group", "UserID", "UserDeviceType"])["duration"].sum().tolist()

    datatable = dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in datatable_data.columns],
        data=datatable_data.to_dict('records'),
        page_current=0,
        page_size=20,
        page_action='native',
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    )

    return [
        dcc.Graph(figure=figure),
        html.Br(),
        cardDiv,
        html.Br(),
        datatable
    ]


@app.callback(
    Output("group-dropdown", "options"),
    [
        Input('start-date-dropdown', 'value'),
        Input('end-date-dropdown', 'value')
    ]
)
def update_groups(start_date, end_date):
    reformed_data = call_data[(call_data["date"] >= start_date) & (
        call_data["date"] <= end_date)]
    group_list = reformed_data["Group"].unique().tolist()
    group_list = [{"label": m, "value": m} for m in group_list]
    return group_list


# Flow of your Project
def main():
    load_data()

    open_browser()

    global app, project_name
    project_name = "CDR Analysis with Insights"
    app.layout = create_app_ui()
    app.title = project_name

    # go to https://www.favicon.cc/ and download the ico file and store in assets directory
    app.run_server()  # debug=True

    print("This would be executed only after the script is closed")

    app = None
    project_name = None

    global call_data, service_data, start_date_list, end_date_list, report_type_list
    call_data = None
    service_data = None
    start_date_list = None
    end_date_list = None
    report_type_list = None


if __name__ == '__main__':
    main()
