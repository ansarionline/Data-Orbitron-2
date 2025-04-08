import dash, json
import dash_bootstrap_components as dbc
from dash import ctx, dcc, html
from dash import Input, Output, State, no_update
import plotly.graph_objects as go
fonts = [
    "Arial",
    "Balto",
    "Courier New",
    "Droid Sans",
    "Droid Serif",
    "Droid Sans Mono",
    "Gravitas One",
    "Old Standard TT",
    "Open Sans",
    "Overpass",
    "PT Sans Narrow",
    "Raleway",
    "Roboto",
    "Times New Roman",
    "Verdana"
]
def make_xaxis():
    return dbc.Form([
        html.H6('X Title', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Text"),
                dbc.Input(id='x-title-text', value='X Axis', placeholder='X Title'),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Font"),
                dbc.Select(id='x-title-font', placeholder='Font', value='Arial',
                        options=[{'label': l, 'value': l} for l in fonts]),
                dbc.Input(id='x-title-size', type='number', min=5, step=1, value=12,
                        placeholder='Font Size'),
                dbc.Input(id='x-title-color', type='color', value='#000000',
                        style={'height': '40px'}),
            ], className="mb-2"),
        ]),
        html.H6('X Tick', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Font"),
                dbc.Select(id='x-tick-font', placeholder='Font',
                        options=[{'label': l, 'value': l} for l in fonts]),
                dbc.Input(id='x-tick-size', type='number', min=5, step=1, value=12,
                        placeholder='Size'),
                dbc.Input(id='x-tick-color', type='color', value='#000000',
                        style={'height': '40px'}),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Angle"),
                dbc.Input(id='x-tick-angle', type='number', min=0, max=180, step=1, value=0,
                        placeholder='Angle'),
            ], className="mb-2"),
        ]),
        html.H6('X Grid', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([                
                dbc.InputGroupText(class_name="inptext", children="Width"),
                dbc.Input(id='x-grid-width', type='number', min=0, step=1, value=1,
                          placeholder='Grid Width'),
                dbc.InputGroupText(class_name="inptext", children="Color"),
                dbc.Input(id='x-grid-color', type='color', value='#000000',
                          style={'height': '40px'}),
            ], className="mb-2"),
        ]),
        html.H6('X Line', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Width"),
                dbc.Input(id='x-line-width', type='number', min=1, step=1, value=1,
                          placeholder='Width'),
                dbc.InputGroupText(class_name="inptext", children="Color"),
                dbc.Input(id='x-line-color', type='color', value='#000000',
                          style={'height': '40px'}),
            ], className="mb-2"),
        ]),
    ], style={"padding": "10px", "border": "1px solid #ddd", "border-radius": "8px", "backgroundColor": "#f9f9f9"})
def make_yaxis():
    return dbc.Form([
        html.H6('Y Title', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="text"),
                dbc.Input(id='y-title-text', value='y Axis', placeholder='y Title'),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Font"),
                dbc.Select(id='y-title-font', placeholder='Font', value='Arial',
                        options=[{'label': l, 'value': l} for l in fonts]),
                dbc.Input(id='y-title-size', type='number', min=5, step=1, value=12,
                        placeholder='Font Size'),
                dbc.Input(id='y-title-color', type='color', value='#000000',
                        style={'height': '40px'}),
            ], className="mb-2"),
        ]),
        html.H6('Y Tick', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Font"),
                dbc.Select(id='y-tick-font', placeholder='Font',
                        options=[{'label': l, 'value': l} for l in fonts]),
                dbc.Input(id='y-tick-size', type='number', min=5, step=1, value=12,
                        placeholder='Size'),
                dbc.Input(id='y-tick-color', type='color', value='#000000',
                        style={'height': '40px'}),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Angle"),
                dbc.Input(id='y-tick-angle', type='number', min=0, max=180, step=1, value=0,
                        placeholder='Angle'),
            ], className="mb-2"),
        ]),
        html.H6('y Grid', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([                
                dbc.InputGroupText(class_name="inptext", children="Width"),
                dbc.Input(id='y-grid-width', type='number', min=0, step=1, value=1,
                          placeholder='Grid Width'),
                dbc.InputGroupText(class_name="inptext", children="Color"),
                dbc.Input(id='y-grid-color', type='color', value='#000000',
                          style={'height': '40px'}),
            ], className="mb-2"),
        ]),
        html.H6('y Line', className="text-primary mb-2", style={"fontSize": "12px"}),
        dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText(class_name="inptext", children="Width"),
                dbc.Input(id='y-line-width', type='number', min=1, step=1, value=1,
                          placeholder='Width'),
                dbc.InputGroupText(class_name="inptext", children="Color"),
                dbc.Input(id='y-line-color', type='color', value='#000000',
                          style={'height': '40px'}),
            ], className="mb-2"),
        ]),
        dbc.Checkbox(id='y-grid-show', value=True, style={"display":"none"}),
        dbc.Checkbox(id='x-grid-show', value=True, style={"display":"none"}),
    ], style={"padding": "10px", "border": "1px solid #ddd", "border-radius": "8px", "backgroundColor": "#f9f9f9"})

def register_xaxis(app, fig):
    @app.callback(
        [Output('x-title-text', 'value'),
        Output('x-title-font', 'value'),
        Output('x-title-size', 'value'),
        Output('x-title-color', 'value'),
        Output('x-tick-font', 'value'),
        Output('x-tick-size', 'value'),
        Output('x-tick-color', 'value'),
        Output('x-tick-angle', 'value'),
        Output('x-grid-show', 'value'),
        Output('x-grid-color', 'value'),
        Output('x-grid-width', 'value'),
        Output('x-line-color', 'value'),
        Output('x-line-width', 'value')],
        Input('axes-select', 'value'),
        State('figure-preview', 'figure')
    )
    def default_xaxis_title(axes, fig):
        index = axes if axes is not None and int(axes) > 1 else ''
        layout = fig['layout']
        axis = layout.get(f'xaxis{index}', {})
        title = axis.get('title', {})
        t_text = title.get('text','')
        tfnt = title.get('font',{})
        t_font = tfnt.get('family','')
        t_size = tfnt.get('size','')
        t_color = tfnt.get('color','')
        lfnt = axis.get('tickfont',{})
        l_font = lfnt.get('family','')
        l_size = lfnt.get('size','')
        l_color = lfnt.get('color','')
        l_angle = axis.get('tickangle','')
        g_show = axis.get('showgrid',False)
        g_color = axis.get('gridcolor','')
        g_width = axis.get('gridwidth','')
        z_color = axis.get('linecolor','')
        z_width = axis.get('linewidth','')
        return  (t_text,t_font,t_size,t_color,
                l_font,l_size,l_color,l_angle,
                g_show,g_color,g_width,
                z_color,z_width)

    @app.callback(
        Output('figure-preview', 'figure', allow_duplicate=True),
        [Input('x-title-text', 'value'),
        Input('x-title-font', 'value'),
        Input('x-title-size', 'value'),
        Input('x-title-color', 'value'),
        Input('x-tick-font', 'value'),
        Input('x-tick-size', 'value'),
        Input('x-tick-color', 'value'),
        Input('x-tick-angle', 'value'),
        Input('x-grid-show', 'value'),
        Input('x-grid-color', 'value'),
        Input('x-grid-width', 'value'),
        Input('x-line-color', 'value'),
        Input('x-line-width', 'value')],
        [State('figure-preview', 'figure'),
        State('axes-select', 'value')]
    )
    def update_xaxis_settings(
        t_text, t_font, t_size, t_color,
        l_font, l_size, l_color, l_angle, 
        g_show, g_color, g_width,
        z_color,z_width,
        figure, selected_index):
        def validate_input(value):
            return value is not None and len(str(value)) > 0
        def return_input(value):
            return value if validate_input(value) else None
        fig = go.Figure(figure)
        layout_update = {}
        if selected_index:
            selected_index = str(selected_index) if int(selected_index) > 1 else ''
            xaxis_key = f'xaxis{selected_index}'
            layout_update[xaxis_key] = {
                'title': {
                    'font': {
                        'family': return_input(t_font),
                        'size': return_input(t_size),
                        'color': return_input(t_color)
                    },
                    'text': return_input(t_text)
                },
                'tickfont': {
                    'family':return_input(l_font),
                    'size': return_input(l_size),
                    'color': return_input(l_color)
                },
                'tickangle': return_input(l_angle),
                'showgrid':True if return_input(g_width) and return_input(g_width) > 0 else False,
                'gridcolor': return_input(g_color),
                'gridwidth': return_input(g_width),
                'linewidth': return_input(z_width),
                'linecolor': return_input(z_color)
            }
            layout_update[xaxis_key] = {
                key: value for key, value in layout_update[xaxis_key].items() if value is not None
            }
            fig.update_layout(layout_update)
        return fig
    
def register_yaxis(app, fig):
    @app.callback(
        [Output('y-title-text', 'value'),
        Output('y-title-font', 'value'),
        Output('y-title-size', 'value'),
        Output('y-title-color', 'value'),
        Output('y-tick-font', 'value'),
        Output('y-tick-size', 'value'),
        Output('y-tick-color', 'value'),
        Output('y-tick-angle', 'value'),
        Output('y-grid-show', 'value'),
        Output('y-grid-color', 'value'),
        Output('y-grid-width', 'value'),
        Output('y-line-color', 'value'),
        Output('y-line-width', 'value')],
        Input('axes-select', 'value'),
        State('figure-preview', 'figure')
    )
    def default_yaxis_title(axes, fig):
        index = axes if axes is not None and int(axes) > 1 else ''
        layout = fig['layout']
        axis = layout.get(f'yaxis{index}', {})
        title = axis.get('title', {})
        t_text = title.get('text', '')
        tfnt = title.get('font', {})
        t_font = tfnt.get('family', '')
        t_size = tfnt.get('size', '')
        t_color = tfnt.get('color', '')
        lfnt = axis.get('tickfont', {})
        l_font = lfnt.get('family', '')
        l_size = lfnt.get('size', '')
        l_color = lfnt.get('color', '')
        l_angle = axis.get('tickangle', '')
        g_show = axis.get('showgrid', True)
        g_color = axis.get('gridcolor', '')
        g_width = axis.get('gridwidth', '')
        z_color = axis.get('linecolor', '')
        z_width = axis.get('linewidth', '')
        return (t_text, t_font, t_size, t_color,
                l_font, l_size, l_color, l_angle,
                g_show, g_color, g_width,
                z_color, z_width)

    @app.callback(
        Output('figure-preview', 'figure', allow_duplicate=True),
        [Input('y-title-text', 'value'),
        Input('y-title-font', 'value'),
        Input('y-title-size', 'value'),
        Input('y-title-color', 'value'),
        Input('y-tick-font', 'value'),
        Input('y-tick-size', 'value'),
        Input('y-tick-color', 'value'),
        Input('y-tick-angle', 'value'),
        Input('y-grid-show', 'value'),
        Input('y-grid-color', 'value'),
        Input('y-grid-width', 'value'),
        Input('y-line-color', 'value'),
        Input('y-line-width', 'value')],
        [State('figure-preview', 'figure'),
        State('axes-select', 'value')]
    )
    def update_yaxis_settings(
        t_text, t_font, t_size, t_color,
        l_font, l_size, l_color, l_angle, 
        g_show, g_color, g_width,
        z_color, z_width,
        figure, selected_index):
        def validate_input(value):
            return value is not None and len(str(value)) > 0
        def return_input(value):
            return value if validate_input(value) else None
        fig = go.Figure(figure)
        layout_update = {}
        if selected_index:
            selected_index = str(selected_index) if int(selected_index) > 1 else ''
            yaxis_key = f'yaxis{selected_index}'
            layout_update[yaxis_key] = {
                'title': {
                    'font': {
                        'family': return_input(t_font),
                        'size': return_input(t_size),
                        'color': return_input(t_color)
                    },
                    'text': return_input(t_text)
                },
                'tickfont': {
                    'family': return_input(l_font),
                    'size': return_input(l_size),
                    'color': return_input(l_color)
                },
                'tickangle': return_input(l_angle),
                'showgrid':True if return_input(g_width) and return_input(g_width) > 0 else False,
                'gridcolor': return_input(g_color),
                'gridwidth': return_input(g_width),
                'linewidth': return_input(z_width),
                'linecolor': return_input(z_color)
            }
            layout_update[yaxis_key] = {
                key: value for key, value in layout_update[yaxis_key].items() if value is not None
            }
            fig.update_layout(layout_update)
        return fig
    
def register_axis(app,fig):
    register_xaxis(app,fig)
    register_yaxis(app,fig)

def make_select():
    return dbc.InputGroup([
            dbc.Label('Axis Index',style={'margin':'5px'}),
            dbc.Select(id='axes-select')],
            style={'margin':'5px','backgroundColor':'#1111ff','color':'white',
                                        'corner-radius':'8px'})

def make_axis(app, fig):
    axissss = [
        make_select(),
        dbc.Container(
            children=[
                dbc.Row(dbc.Col(make_xaxis()), className="mb-3")
            ],
            id='x-axis-accord'
        ),
        dbc.Container(
            children=[
                dbc.Row(dbc.Col(make_yaxis()))
            ],
            id='y-axis-accord'
        ),
    ]
    register_axis(app, fig)
    return html.Div(dbc.Accordion(axissss))