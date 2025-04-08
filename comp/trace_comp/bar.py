import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, no_update
from comp.trace_comp.utils import query_trace as qt

def create_tooltip(target, text, placement='top'):
    return dbc.Tooltip(text, target=target, placement=placement)

def make_bar(app):
    return [
        html.H5("Bar Settings", className="text-primary mb-3"),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Trace", class_name="inptext"),
                    dbc.Select(
                        id='select-trace-bar',
                        placeholder='Select Bar ID'
                    ),
                    create_tooltip(
                        'select-trace-bar',
                        'Select the bar trace you want to modify.',
                        placement='top'
                    )
                ])
            ]),
        ], style={"marginBottom": "5px"}),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Basic", class_name="inptext"),
                    dbc.Input(id="bar-width", placeholder="Width", type="number", step=0.1),
                    create_tooltip(
                        'bar-width',
                        'Set the width of the bar.',
                        placement='top'
                    ),
                    dbc.Input(id="bar-color", placeholder="Color", type="color", style={'height': '39px'}),
                    create_tooltip(
                        'bar-color',
                        'Set the color of the bar.',
                        placement='top'
                    ),
                    dbc.Input(id="bar-opacity", placeholder="Opacity", type="number", min=0, max=1, step=0.05),
                    create_tooltip(
                        'bar-opacity',
                        'Set the opacity of the bar (0 to 1).',
                        placement='top'
                    )
                ])
            ]),
        ], style={"marginBottom": "5px"}),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Border", class_name="inptext"),
                    dbc.Input(id="bar-border-width", placeholder="Width", type="number", step=1, min=0),
                    create_tooltip(
                        'bar-border-width',
                        'Set the width of the bar border.',
                        placement='top'
                    ),
                    dbc.Input(id="bar-border-color", placeholder="Color", type="color", style={'height': '39px'}),
                    create_tooltip(
                        'bar-border-color',
                        'Set the color of the bar border.',
                        placement='top'
                    ),
                    dbc.Input(id="bar-border-rad", placeholder="Corner Radius", type="number", min=0, step=1),
                    create_tooltip(
                        'bar-border-rad',
                        'Set the corner radius of the bar.',
                        placement='top'
                    )
                ])
            ]),
        ], style={"marginBottom": "5px"}),

    ]

import json
def set_defaults(app):
    @app.callback(
        [Output('bar-width','value'),
        Output('bar-color', 'value'),
        Output('bar-border-width', 'value'),
        Output('bar-border-color', 'value'),
        Output('bar-border-rad', 'value')],
        Input('select-trace-bar','value'),
        State('figure-preview','figure'),
    )
    def defaultly(name, data):
        data = data.get('data', [])
        if not data:
            return [no_update] * 10
        for n in data:
            if n.get('name') == name:
                b = n.get('marker', {})
                bw = b.get('width', '') 
                bc = b.get('color', '') 
                bd = b.get('line', {})  
                bdw = bd.get('width', '') 
                bdc = bd.get('color', '') 
                bds = bd.get('shape', '')  
                return bw, bc, bdw, bdc, bds
            break
        return [no_update] * 5

def validate(value):
    return value if value is not None and len(str(value))>0 else None

def update_bar(fig, name, **kwargs):
    if not isinstance(fig, go.Figure):
        fig = go.Figure(fig)
    fig.update_traces(**kwargs, selector=dict(name=name))
    return fig

def update_trace(app, fig):
    @app.callback(
        Output('figure-preview', 'figure',allow_duplicate=True),
        [
            Input('bar-width','value'),
            Input('bar-color', 'value'),
            Input('bar-opacity', 'value'),
            Input('bar-border-width', 'value'),
            Input('bar-border-color', 'value'),
            Input('bar-border-rad', 'value')
        ],
        [State('select-trace-bar', 'value'),
        State('figure-preview', 'figure')]
    )
    def update(bw, bc, bo, bdw, bdc, bdr, name, fig):
        fig =  update_bar(
            fig,
            name,
            width=validate(bw),
            marker=dict(
                color = validate(bc),
                opacity = validate(bo),
                line = dict(
                    width = validate(bdw),
                    color = validate(bdc),
                ),
            cornerradius = validate(bdr),
            )
        )
        return fig

def register_bar(app,fig):
    qt(app,'select-trace-bar','bar')
    set_defaults(app)
    update_trace(app,fig)
