"""File to run dashboard server"""

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv(r'data/all_stocks_5yr.csv')
df['smoothed_open'] = df.groupby('Name')['open']\
                        .transform(
                            lambda x: x.rolling(5, 1).mean()
                        )

df['smoothed_open_diff'] = df.groupby('Name')['smoothed_open']\
                             .diff()\
                             .fillna(0)

df['positive_smoothed_open_diff'] = df['smoothed_open_diff'] >= 0

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def draw_figure(plot_df):
    """Plot graph"""
    ticker_name = plot_df['Name'].unique()[0]
    fig = go.Figure()
    # for asdf, sub_df in plot_df.groupby('positive_smoothed_open_diff'):
        # fig.add_trace(
            # go.Scatter(
                # x=sub_df['date'],
                # y=sub_df['open'],
                # name=asdf,
            # )
        # )
    fig.add_trace(
        go.Scatter(
            x=plot_df['date'],
            y=plot_df['open'],
        )
    )
    fig.update_layout(
        title=go.layout.Title(text=f"S&P 500 Stock Prices - {ticker_name}"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='rgb(215,215,215)'
    )

    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=fig,
                )],
                style={
                }
            ),
            style={
                'border-color': '#181818',
                'box-shadow': '1px 1px 1px 1px rgba(0,0,0,0.2)',
                'background-color': '#373747'
            }
        ),
    ])


def draw_sidebar():
    """Setup sidebar dropdowns / info"""
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ],
                style={
                    'textAlign': 'center'
                })
            ])
        ),
    ])


def create_dropdown(name, options, default=None):
    """Create dropdown dcc component"""
    component_id = f'{name}-select'
    dropdown = dcc.Dropdown(
        options=options,
        value=default,
        id=component_id,
        style={
            'background-color': '#181818',
            'color': '#000000',
            'box-shadow': '0px 4px 8px 4px rgba(0,0,0,0.2)'
        },
    )
    return dropdown


app.layout = html.Div([
    dbc.Row([
        dbc.Navbar(children=[
            html.H4(
                children='S&P 500 Dashboard',
                style={
                    'flex': 'auto',
                    'margin-left': '20px'
                }
            ),
            html.A(
                href='https://github.com/morganlbruce/stock-dashboard',
                children=[
                    html.Img(
                        src='assets/github-mark-white.svg',
                        style={
                            'height': '30px',
                            'margin-right': '20px',
                            'align': 'right'
                        }
                    )
                ]
            ),
        ],
        color='primary',
        dark=True,
        style={
            'color': '#bda5bd',
            'padding': '2px'
        },)
    ]),
    dbc.Row([
        dbc.Card(
            children=dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div(
                            children=[
                            html.H4(
                                children="Select stock",
                                style={
                                    'color': '#cfcfcf'
                                }
                            ),
                            create_dropdown(
                                'stock',
                                df['Name'].unique(),
                                df['Name'].values[0]
                            )],
                            style={
                                'align': 'top',
                                'flex': 'auto',
                            }
                        )
                    ], width=3),
                    dbc.Col([
                        html.Div(id='stock-graph'),
                    ], width=9),
                ], align='center'),
            ]),
            style={
                'height': '93vh',
            }
        )],
    )
])


@callback(
    Output('stock-graph', 'children'),
    Input('stock-select', 'value')
)
def update_graph(value):
    """Callback to plot selected stock value"""
    if value is None:
        return None
    sub_df = df[df['Name'] == value]
    figure = draw_figure(sub_df)
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
