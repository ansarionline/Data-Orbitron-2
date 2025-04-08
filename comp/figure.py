import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State, Dash
import plotly.graph_objects as go

# List of available fonts
fonts = [
    "Arial", "Verdana", "Tahoma", "Trebuchet MS", "Georgia", "Times New Roman",
    "Courier New", "Lucida Console", "Impact", "Roboto", "Open Sans", "Lato", "Poppins",
    "Montserrat", "Raleway", "PT Sans", "Droid Sans", "Droid Serif", "Source Sans Pro",
    "Noto Sans", "San Francisco", "Helvetica", "Gill Sans", "Palatino", "Optima",
    "Segoe UI", "Candara", "Constantia", "Consolas", "Franklin Gothic Medium",
    "Ubuntu", "DejaVu Sans", "Liberation Sans", "Nimbus Sans", "Futura", "Baskerville",
    "Century Gothic", "Garamond", "Bookman Old Style", "Lucida Bright"
]

def validate(value):
    return value if value is not None and len(str(value)) > 0 else None

import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

def register_figure(app, fig):
    @app.callback(
        Output('figure-preview', 'figure', allow_duplicate=True),
        [
            Input('fig-title-text', 'value'),
            Input('fig-title-font', 'value'),
            Input('fig-title-size', 'value'),
            Input('fig-title-color', 'value'),
            Input('fig-title-x', 'value'),
            Input('fig-title-y', 'value'),
            Input('fig-paper-bgcolor', 'value'),
            Input('fig-plot-bgcolor', 'value'),
            Input('fig-show-legend', 'value'),
            Input('fig-legend-arrangement', 'value')
        ],
        State('figure-preview', 'figure')  # Keep the figure state as input to update
    )
    def update_figure(title, font, size, color, x, y, 
                    paper_bgcolor, plot_bgcolor, show_legend
                    , legend_arrangement, fig):
        # Validate the figure object
        if not fig or 'data' not in fig or 'layout' not in fig:
            raise ValueError("Invalid figure object passed to the callback.")

        # Create a fresh copy of the figure
        fig = go.Figure(fig)

        # Update the layout
        layout_update = {
            'template': 'plotly_white',
            'title': {
                'text': title if title else fig.layout.title.text,
                'font': {
                    'family': font if font else fig.layout.title.font.family,
                    'size': size if size else fig.layout.title.font.size,
                    'color': color if color else fig.layout.title.font.color
                },
                'x': x if x is not None else fig.layout.title.x,
                'y': y if y is not None else fig.layout.title.y
            },
            'paper_bgcolor': paper_bgcolor or fig.layout.paper_bgcolor,
            'plot_bgcolor': plot_bgcolor or fig.layout.plot_bgcolor,
            'autosize': True,
            'showlegend': show_legend,  # Toggle legend visibility
            'legend': {
                'orientation': legend_arrangement or fig.layout.legend.orientation
            }
        }

        fig.update_layout(layout_update)

        # Return the updated figure
        return fig

def make_fig(app, fig):
    figure_form = dbc.Container([
        # Title Settings
        html.H6("Title", className="text-primary mb-2"),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Text", class_name="inptext"),
                    dbc.Input(id='fig-title-text', placeholder='Figure Title'),
                ])
            ], className="mb-2"),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Font", class_name="inptext"),
                    dbc.Select(id='fig-title-font',
                        options=[{'label': l, 'value': l} for l in fonts]),
                    dbc.Input(id='fig-title-size', placeholder='Size',
                            type='number', min=5, step=1),
                    dbc.Input(id='fig-title-color', type='color', style={'height': '40px'}),
                ])
            ], className="mb-2"),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Posing", class_name="inptext"),
                    dbc.Input(id='fig-title-x', placeholder='X', type='number', 
                            min=0, step=0.05, max=1),
                    dbc.Input(id='fig-title-y', placeholder='Y', type='number', 
                            min=0, step=0.05, max=1),
                ])
            ], className="mb-2"),
        ], style={"marginBottom": "15px"}),

        # Themes
        html.H6("Themes", className="text-primary mb-2"),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Colors", class_name="inptext"),
                    dbc.Input(id='fig-paper-bgcolor', type='color',
                            value='#e4f6fb', style={'height': '40px'}),
                    dbc.Input(id='fig-plot-bgcolor', type='color', 
                            value='#ffffff', style={'height': '40px'}),
                ])
            ])
        ], style={"padding": "10px"}),

        # Legend Controls
        html.H6([
            "Legends",
            dbc.Checkbox(id='fig-show-legend', value=True)
        ],
        className="text-primary mb-2",
        style={"display": "inline-flex", "alignItems": "center", "gap": "2px"}),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Pos", class_name="inptext"),
                    dbc.Select(
                        id='fig-legend-arrangement',
                        options=[
                            {'label': 'Vertical', 'value': 'v'},
                            {'label': 'Horizontal', 'value': 'h'}
                        ],
                        value='v'
                    )
                ])
            ], className="mb-2"),
        ], style={"marginBottom": "15px"}),

    ], id='figure-div', style={
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "8px",
        "backgroundColor": "#f9f9f9",
        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)"
    })

    register_figure(app, fig)
    return figure_form
