from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

df = px.data.iris()

app = Dash(external_stylesheets=[dbc.themes.SLATE])

def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

navbar_style = {
    'text-align': 'left',
    'color': '#bda5bd',
    'margin-left': '20px',
    'padding': '5px'
}

app.layout = html.Div([
    dbc.Row([
        dbc.Navbar(children=[
            html.H4('S&P 500 Dashboard', style=navbar_style),
            html.A(href='https://github.com/morganlbruce/stock-dashboard', children=[html.Img(src='assets/github-mark-white.svg',  style={'height': '30px', 'align': ''})]),
        ],
        color='primary',
        dark=True,)
    ]),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawText()
                ], width=4),
                dbc.Col([
                    drawText()
                ], width=8),
            ], align='center'), 
            html.Br(),
        ])
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
