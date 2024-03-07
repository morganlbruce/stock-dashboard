"""File to run dashboard server"""

from ctypes.wintypes import RGB
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go  

app = Dash(__name__)

df = pd.read_csv(r'data/all_stocks_5yr.csv')
df = df[df['Name'] == 'AAL']

app = Dash(external_stylesheets=[dbc.themes.SLATE])


def draw_figure(df):
    """Plot graph"""
    data = [{
        'type': 'scatter',
        'x': df['date'].values,
        'y': df['open'].values,
    }]
    layout = go.Layout(
        title=go.layout.Title(text="S&P 500 Stock Prices"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='rgb(235,235,225)'
    )
    fig = go.Figure(
        data=data,
        layout=layout,
    )

    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=fig,
                )
            ])
        ),
    ])


def draw_sidebar():
    """Setup sidebar dropdowns / info"""
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
            html.A(
                href='https://github.com/morganlbruce/stock-dashboard',
                children=[
                    html.Img(
                        src='assets/github-mark-white.svg',
                        style={'height': '30px', 'align': ''}
                    )
                ]
            ),
        ],
        color='primary',
        dark=True,)
    ]),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    draw_sidebar()
                ], width=3),
                dbc.Col([
                    draw_figure(df)
                ], width=9),
            ], align='center'),
            html.Br(),
        ])
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
