from dash import dcc, html, Input, Output, State, dash_table, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import plotly.graph_objects as go

def register_data(app, fig=None):
    @app.callback(
        Output('df-table', 'data', allow_duplicate=True),
        Output('df-table', 'columns', allow_duplicate=True),
        Output('x-col-select', 'options', allow_duplicate=True),
        Output('y-col-select', 'options', allow_duplicate=True),
        Output('figure-preview', 'figure', allow_duplicate=True),
        Output('df-df', 'data', allow_duplicate=True),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('figure-preview', 'figure'),
    )
    def update_data(contents, filename, figure):
        data, columns, col_options, fig = [], [], [], figure or {"data": []}
        df_json = None

        if contents is not None:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)

            try:
                if 'csv' in filename:
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                elif 'xls' in filename:
                    df = pd.read_excel(io.BytesIO(decoded))
                else:
                    raise ValueError("Unsupported file type")
                data = df.to_dict('records')
                columns = [{"name": col, "id": col} for col in df.columns]
                col_options = [{"label": col, "value": col} for col in df.columns]
                df_json = df.to_json(orient='split')
            except Exception as e:
                print(f"Error processing uploaded file: {e}")

        return data, columns, col_options, col_options, fig, df_json
    
    

def make_data(app, fig):
    ddd = dbc.Container(
        id='data-div',
        children=[
            # Row for file upload
            dbc.Row(
                [
                    dcc.Store('df-df', data=[]),
                    dbc.Col(
                        [
                            dcc.Upload(
                                id='upload-data',
                                children=dbc.Button(
                                    "Upload File",
                                    style={"width": "100%"}  # Full width button
                                ),
                                style={
                                    "width": "100%",  # Full width container
                                    "marginBottom": "5px",  # Reduced margin
                                    "textAlign": "center",
                                    "padding": "5px",  # Reduced padding
                                    "border": "1px dashed #007bff",  # Thinner border
                                    "borderRadius": "5px",
                                    "backgroundColor": "#f8f9fa",
                                },
                                multiple=False
                            )
                        ],
                        width=12
                    ),
                ],
                style={"marginBottom": "10px"},  # Reduced row margin
                id='dt-r'
            ),
            # Row for data table
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dash_table.DataTable(
                                id='df-table',
                                style_table={
                                    'height': '300px',  # Reduced height
                                    'width': '100%',  # Full width
                                    'overflowY': 'auto',  # Scrollable vertically
                                    'overflowX': 'auto',  # Scrollable horizontally
                                },
                                style_cell={
                                    "textAlign": "center",
                                    "padding": "3px",  # Reduced padding
                                    "fontFamily": "Arial, sans-serif",
                                    "fontSize": "11px",  # Smaller font size
                                    "fontWeight": "normal",
                                    "whiteSpace": "normal",  # Wrap text for responsiveness
                                },
                                style_header={
                                    "fontWeight": "bold",
                                    "textAlign": "center",
                                    "fontSize": "12px",  # Smaller font size
                                    "backgroundColor": "#007bff",
                                    "color": "white",
                                },
                                columns=[
                                    {"id": "Index", "name": "Index"},
                                    {"id": "Col1", "name": "Col1"}
                                ],
                                editable=False,
                                row_deletable=False
                            )
                        ],
                        width=12
                    )
                ],
                style={"marginBottom": "10px"}  # Reduced row margin
            ),
        ],
        style={
            'width': '100%',  # Full width container
            'padding': '5px',  # Reduced padding
            'backgroundColor': '#f8f9fa',
            'border': '1px solid #ddd',
            'borderRadius': '8px',  # Slightly smaller border radius
        }
    )
    register_data(app, fig)
    return ddd