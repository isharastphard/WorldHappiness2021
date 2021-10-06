import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.io as pio

from dash.dependencies import Output, Input 

data = pd.read_csv("world-happiness-report-2021.csv")
df = pd.read_csv("world-happiness-report.csv")
agg = pd.read_csv("happiness-aggregations.csv")

external_stylesheets = [
    'style.css', 
    {
        'href' : 'https://fonts.googleapis.com/css2?family=Oswald:wght@300&display=swap',
        'rel' : 'stylesheet',
    }
]

fig = px.bar(data, x = "Country name", y = "Ladder score", color = "Regional indicator", labels = {'y' : "Ranking out of 10"})
correl = px.scatter(data, x ="Country name", y = "Logged GDP per capita", size = "Logged GDP per capita", color = "Regional indicator", title = "How rich are the citizens?")
correl2 = px.scatter(data, x ="Country name", y = "Social support", size = "Ladder score", color = "Regional indicator", title = "How is this country's social programs?")
correl3 = px.scatter(data, x ="Country name", y = "Healthy life expectancy", size = "Ladder score", color = "Regional indicator", title = "Life expectancy")
correl4 = px.scatter(data, x ="Country name", y = "Freedom to make life choices", size = "Ladder score", color = "Regional indicator", title = "Can you be who you are without shame? Can you do what you please?")
correl5 = px.scatter(data, x ="Country name", y = "Generosity", size = "Ladder score", color = "Regional indicator", title = "How would a citizen rank their felllow citizen's generosity?")
correl6 = px.scatter(data, x ="Country name", y = "Perceptions of corruption", size = "Ladder score", color = "Regional indicator", title = "How does society perceive their government?")
lastly = px.area(df, x = "year", y = "Life Ladder", color = "Country name", line_group = "Country name")
aggreg = px.bar(agg, x = "Regional indicator", y = "Mode", color = "Regional indicator", title = "The amount of countries surveyed in a particular Region")
aggreg2 = px.bar(agg, x = "Regional indicator", y = "Regional Average", color = "Regional indicator", title = "The average of the ladder score of the regions")

data2 = data.copy()

data2 = [dict(
    type = 'scatter',
    x = data2["Regional indicator"],
    y = data2["Ladder score"],
    mode = 'markers',
    transforms = [dict(
        type = 'aggregate',
        groups = data2["Regional indicator"],
        aggregations = [dict(
            target = 'y', func = 'sum', enabled = True
        )]
    )]
)]

fig_dict = dict(data2=data2)

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SOLAR])
app.title = "Where are we happiest?"

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='by Region', children=[
           html.H1(children = "Let's See Where The Happiest People on the Planet Live in 2021",
    style = {'text-align' : 'center'}
                  ),

    dcc.Graph(
    id = "first graph",
    figure = fig
        )], 
        ),
        dcc.Tab(label=' by GDP', children=[
            html.H1(children = "Let's take a look at some of the metrics surveyed in 2021?",
            style = {'text-align' : 'center'}),
            dcc.Graph(
                id = "second graph",
                figure = correl
            ),    
            dcc.Graph(
                id = "social support graph",
                figure = correl2
            ),    
            dcc.Graph(
                id = "healthy life graph",
                figure = correl3
            ),    
            dcc.Graph(
                id = "choices graph",
                figure = correl4
            ),    
            dcc.Graph(
                id = "generosity graph",
                figure = correl5
            ),    
            dcc.Graph(
                id = "perception graph",
                figure = correl6
            ),    
        ]),
        dcc.Tab(label='Over Time', children=[
            html.H1(children = "Let's look at world happiness from 2008 to 2020",
            style = {'text-align' : 'center'}),
            dcc.Graph(
                id = "third graph",
                figure = lastly 
            ),
            html.H2(children = "It seems as though on a global scale, something caused world happiness to decline from 2019 onward."),
        ]),
        dcc.Tab(label = "Aggregation", children =[
            html.H1(children = "Who comes out on top?",
            style = {'text-align' : 'center'}),
            dcc.Graph(
                id = "fourth graph",
                figure = aggreg
            ),
            dcc.Graph(
                id = "fifth Graph",
                figure = aggreg2
            )
        ])
    ]),
])

if __name__ == "__main__":
    app.run_server()                             