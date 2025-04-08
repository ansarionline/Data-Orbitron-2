from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.io as pio
import json
import tempfile

formats = [
    fmt.upper() for fmt in ['png', 'jpg', 'jpeg', 
                            'webp', 'svg', 'pdf', 
                            'json', 'pydict', 'py', 
                            'html', 'htm']
]

def generate_python_code(figure):
    """
    Generate Python code for a Plotly figure.
    """
    fig_dict = figure  # The figure is already in dictionary format
    python_code = "import plotly.graph_objects as go\n\n"
    python_code += f"fig = go.Figure({json.dumps(fig_dict, indent=4)})\n"
    python_code += "fig.show()\n"
    return python_code
def register_export(app, fig):
    @app.callback(
        Output('download-figure', 'data', allow_duplicate=True),
        Input('export-button', 'n_clicks'),
        State('export-filename', 'value'),
        State('export-format', 'value'),
        State('figure-preview', 'figure'),
        State('export-width', 'value'),
        State('export-height', 'value'),
        State('export-scale', 'value'),
        prevent_initial_call=True
    )
    def export_figure(n_clicks, name, export_format, figure, width, height, scale):
        triggerd_id = ctx.triggered_id
        
        if not figure:
            return dcc.send_string("No figure to export.", filename="error.txt")

        if export_format.upper() not in formats:
            return dcc.send_string(f"Invalid format: {export_format}", filename="error.txt")

        try:
            file_name = f"{name}-data-orbitron-export.{export_format.lower()}"
            if export_format.lower() in ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf']:
                # Use a temporary file to save the image
                with tempfile.NamedTemporaryFile(prefix=name,suffix=f".{export_format.lower()}", 
                    delete=False) as tmp_file:
                    pio.write_image(
                        figure,
                        tmp_file.name,
                        width=width or 720,
                        height=height or 360,
                        scale=scale or 1,
                        engine="kaleido"
                    )
                    return dcc.send_file(tmp_file.name)
            elif export_format.lower() == 'json':
                return dcc.send_string(pio.to_json(figure), filename=file_name)
            elif export_format.lower() == 'pydict':
                return dcc.send_string(json.dumps(figure, indent=4), filename=file_name)
            elif export_format.lower() == 'py':
                python_code = generate_python_code(figure)
                return dcc.send_string(python_code, filename=file_name)
            elif export_format.lower() in ['html', 'htm']:
                return dcc.send_string(
                    pio.to_html(figure,
                                full_html=True,
                                config={'displaylogo': False,
                                        'responsive': True,    
                                        'scrollZoom': True,   
                                        'doubleClick': 'reset',
                                        }),
                    filename=file_name
                )
            else:
                return dcc.send_string(f"Unsupported format: {export_format}", filename="error.txt")
        except Exception as e:
            print("Exception occurred:", str(e))  
            return dcc.send_string(f"Error exporting figure: {str(e)}", filename="error.txt")

def make_export(app, fig):
    exporttt = dbc.Container([
        html.Div([
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Name", class_name="inptext"),
                    dbc.Input(id='export-filename', 
                            placeholder='File Name',
                            value='exported_figure',
                        style={'width': '40%'}),
                    dbc.Select(
                        id='export-format',
                        options=[{'label': fmt, 'value': fmt.lower()} for fmt in formats],
                        placeholder='Select Export Format',
                        style={'width': '20%'},
                        value='png'
                    )
                ])
            ], className="mb-2"),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Width", class_name="inptext"),
                    dbc.Input(id='export-width', type='number', placeholder='Width (px)',
                            min=50, step=1, value=720),
                    dbc.InputGroupText("Height", class_name="inptext"),
                    dbc.Input(id='export-height', type='number', placeholder='Height (px)',
                            min=50, step=1, value=360)
                ])
            ], className="mb-2"),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText("Scale", class_name="inptext"),
                    dbc.Input(id='export-scale', type='number', placeholder='Scale (e.g., 1)',
                            min=0.1, step=0.1, value=1, max = 10)
                ])
            ], className="mb-2"),
            dbc.Button("Export", id='export-button'),
            dcc.Download(id="download-figure")  # Download component
        ], style={"marginBottom": "15px"})
    ], id='export-div', style={
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "8px",
        "backgroundColor": "#f9f9f9",
        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)"
    })
    register_export(app, fig)
    return exporttt