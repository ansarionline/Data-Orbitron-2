import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, no_update, dcc
from comp.trace_comp.utils import query_trace as qt
import json

def create_tooltip(target_id, description, placement="right"):
    return dbc.Tooltip(description, target=target_id, placement=placement)

def make_line(app):
    line_form = [
        html.H5("Line Settings", className="text-primary mb-3"),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Trace", class_name="inptext"),
                    dbc.Select(
                        id='select-trace-line',
                        placeholder='Select Line ID'
                    ),
                    create_tooltip(
                        'select-trace-line',
                        'Select the line ID for line settings.',
                    )
                ])
            ]),
        ], style={"marginBottom": "5px"}),
        html.H6("Line", className="text-primary mb-3"),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Basic", class_name="inptext"),
                    dbc.Input(id='line-basic-width', type='number', 
                            placeholder='Width', min=0),
                    create_tooltip(
                        'line-basic-width',
                        'Set the width of line.',
                    ),
                    dbc.Input(id='line-basic-opacity', type='number', 
                            min=0, max=1, step=0.1, placeholder='Opacity'),
                    create_tooltip(
                        'line-basic-opacity',
                        'Set the opacity of line.',
                    ),
                    dbc.Input(id='line-basic-color', type='color', 
                            value='#636efa', style={'height': '40px'}),
                    create_tooltip(
                        'line-basic-color',
                        'Set the color of line.',
                    ),
                ])
            ]),
        ], style={"marginBottom": "5px"}),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Dash", class_name="inptext"),
                    dbc.Select(
                        id='line-shap-dash',
                        options=[
                            {'label': 'Solid━━', 'value': 'solid'},
                            {'label': 'Dash--', 'value': 'dash'},
                            {'label': 'Dot⋯', 'value': 'dot'},
                            {'label': 'Dash+Dot-·-', 'value': 'dashdot'},
                        ],
                        placeholder='Dash Shape'
                    ),
                    create_tooltip(
                        'line-shap-dash',
                        'Set the shape of dash of line.',
                    ),
                    dbc.Select(
                        id='line-shap-shape',
                        options=[
                            {'label': 'Straight', 'value': 'linear'},
                            {'label': 'Curve', 'value': 'spline'},
                            {'label': 'VHV', 'value': 'vhv'},
                            {'label': 'HVH', 'value': 'hvh'},
                        ],
                        placeholder='Line Shape'
                    ),
                    create_tooltip(
                        'line-shap-shape',
                        'Set the sequence of dash of line.',
                    ),
                    dbc.Input(id='line-shap-smth', type='number',
                    min=0, max=1, step=0.005, placeholder='Smoothing'),
                    create_tooltip(
                        'line-shap-smth',
                        'Set the smoothness of line.',
                    ),
                ])
            ]),
        ], style={"marginBottom": "5px"}),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Fill Type", class_name="inptext"),
                    dbc.Select(
                        id='line-fill-type',
                        options=[
                            {'label': 'None', 'value': 'none'},
                            {'label': 'Zero X', 'value': 'tozerox'},
                            {'label': 'Zero Y', 'value': 'tozeroy'},
                            {'label': 'Next', 'value': 'tonext'},
                            {'label': 'Next X', 'value': 'tonextx'},
                            {'label': 'Next Y', 'value': 'tonexty'},
                            {'label': 'Lead Self', 'value': 'toself'},
                        ],
                        placeholder='Fill Style',
                        value='none'
                    ),
                    create_tooltip(
                        'line-fill-type',
                        'Fill the area under line. This creates the area plot.',
                    ),
                    dbc.Input(id='line-fill-clr', type='color', 
                    value='#ADD8E6', style={'height': '39px'}),
                    create_tooltip(
                        'line-fill-clr',
                        'Set the color of fill area.',
                    ),
                ])
            ]),
        ], style={"marginBottom": "10px"}),
        html.H6("Marker", className="text-primary mb-3"),
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Basic", class_name="inptext"),
                    dbc.Input(id='marker-size', type='number', placeholder='Size',
                            min = 0),
                    create_tooltip(
                        'marker-size',
                        'Set the size of the marker.',
                    ),
                    dbc.Input(id='marker-color', type='color', value='#636efa', style={'height': '40px'}),
                    create_tooltip(
                        'marker-color',
                        'Set the color of the marker.',
                    ),
                    dbc.Input(id='marker-opacity', type='number',
                            min=0, max=1, step=0.1, placeholder='Opacity'),
                    create_tooltip(
                        'marker-opacity',
                        'Set the opacity of the marker (0 to 1).',
                    )
                ])
            ], style={"marginBottom": "5px"}),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Border", class_name="inptext"),
                    dbc.Select(
                        id='marker-symbol',
                        options=[
                            {'label': 'Circle', 'value': 'circle'},
                            {'label': 'Square', 'value': 'square'},
                            {'label': 'Diamond', 'value': 'diamond'},
                            {'label': 'Cross', 'value': 'cross'},
                            {'label': 'X', 'value': 'x'},
                        ],
                        placeholder='Symbol'
                    ),
                    create_tooltip(
                        'marker-symbol',
                        'Set the symbol of the marker.',
                    ),
                    dbc.Input(id='marker-line-width', type='number', 
                            placeholder='Line Width', min=0),
                    create_tooltip(
                        'marker-line-width',
                        'Set the width of the marker border.',
                    ),
                    dbc.Input(id='marker-line-color', type='color', value='#000000', style={'height': '40px'}),
                    create_tooltip(
                        'marker-line-color',
                        'Set the color of the marker border.',
                    )
                ])
            ]),
        ], style={"marginBottom": "5px"})
    ]
    return line_form

def defaultly(name, data):
    data = data.get('data', [])
    if not data:
        return [no_update] * 10

    for n in data:
        if n['name'] == name:
            l = n.get('line', {})
            lw = l.get('width', '')
            lo = l.get('opacity', '')
            lc = l.get('color', '')
            ld = l.get('dash', '')
            ls = l.get('shape', '')
            lt = l.get('smoothing', '')
            ft = n.get('fill', '')
            fc = n.get('fillcolor', '')
            m = n.get('marker', {})
            ms = m.get('size', '')
            mc = m.get('color', '')
            mo = m.get('opacity', '')
            msym = m.get('symbol', '')
            mlw = m.get('line', {}).get('width', '')
            mlc = m.get('line', {}).get('color', '')
            return lw, lo, lc, ld, ls, lt, ft, fc, ms, mc, mo, msym, mlw, mlc        
    return [no_update] * 14

def set_defaults(app):
    @app.callback(
        [
            Output('line-basic-width', 'value'),
            Output('line-basic-opacity', 'value'),
            Output('line-basic-color', 'value'),
            Output('line-shap-dash', 'value'),
            Output('line-shap-shape', 'value'),
            Output('line-shap-smth', 'value'),
            Output('line-fill-type', 'value'),
            Output('line-fill-clr', 'value'),
            Output('marker-size', 'value'),
            Output('marker-color', 'value'),
            Output('marker-opacity', 'value'),
            Output('marker-symbol', 'value'),
            Output('marker-line-width', 'value'),
            Output('marker-line-color', 'value'),

        ],
        Input('select-trace-line', 'value'),
        State('figure-preview', 'figure'),
    )
    def defaultly_callback(name, data):
        return defaultly(name, data)

def validate(value):
    return value if value is not None and len(str(value)) > 0 else None

def update_line(fig, name, **kwargs):
    if not isinstance(fig, go.Figure):
        fig = go.Figure(fig)
    fig.update_traces(**kwargs, selector=dict(name=name))
    return fig

def update_trace(app, fig):
    @app.callback(
        Output('figure-preview', 'figure'),
        [
            Input('line-basic-width', 'value'),
            Input('line-basic-opacity', 'value'),
            Input('line-basic-color', 'value'),
            Input('line-shap-dash', 'value'),
            Input('line-shap-shape', 'value'),
            Input('line-shap-smth', 'value'),
            Input('line-fill-type', 'value'),
            Input('line-fill-clr', 'value'),
            Input('marker-size', 'value'),
            Input('marker-color', 'value'),
            Input('marker-opacity', 'value'),
            Input('marker-symbol', 'value'),
            Input('marker-line-width', 'value'),
            Input('marker-line-color', 'value'),
        ],
        [State('select-trace-line', 'value'), State('figure-preview', 'figure')],
        prevent_initial_call=True
    )
    def update(lw, lo, lc, ld, ls, lt, ft, fc, ms, mc, mo, msym, mlw, mlc, name, fig):
        if not isinstance(fig, go.Figure):
            try:
                fig = go.Figure(fig)
            except Exception as e:
                print(f"Error converting figure: {e}")
                return no_update

        # Guard for line width
        try:
            lw = float(lw) if lw is not None else None
        except ValueError:
            lw = None  # If conversion fails, set to None

        line_width = validate(lw) if lw is not None and lw > -1 else None

        # Guard for marker size
        try:
            ms = float(ms) if ms is not None else None
        except ValueError:
            ms = None  # If conversion fails, set to None

        marker_size = ms if ms is not None and ms >= 0 else 0

        # Guard for marker opacity
        try:
            mo = float(mo) if mo is not None else None
        except ValueError:
            mo = None  # If conversion fails, set to None

        marker_opacity = mo if mo is not None and 0 <= mo <= 1 else None

        updated_fig = update_line(
            fig,
            name,
            line=dict(
                width=line_width,  # Only update if the guard passes
                color=validate(lc),
                dash=validate(ld),
                shape=validate(ls),
                smoothing=validate(lt) if validate(ls) == 'spline' else None,
            ),
            opacity=validate(lo),
            fill=validate(ft),
            fillcolor=validate(fc),
            marker=dict(
                size=marker_size,
                color=validate(mc),
                opacity=marker_opacity,
                symbol=validate(msym),
                line=dict(
                    width=validate(mlw),
                    color=validate(mlc)
                )
            )
        )
        return updated_fig

def register_line(app, fig):
    qt(app, 'select-trace-line', 'sca')
    set_defaults(app)
    update_trace(app, fig)
# negative sizing