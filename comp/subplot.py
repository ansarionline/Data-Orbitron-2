from dash import Dash, html, dash_table as dt, Output, Input, State, dcc
import dash
import dash_bootstrap_components as dbc
import plotly.subplots as ps
import plotly.graph_objects as go
from itertools import product
import pandas as pd
from io import StringIO
traces = [
    # {'label':'Basic',"value":'bsc',"disabled":True},
    {"label": "Line", "value": "line"},  # Done
    {"label": "Bar", "value": "bar"}, # Done
    # {'label':'Catagorical',"value":'cat',"disabled":True},
    # {"label": "Bar", "value": "bar"}, # Done
    # {"label": "Funnel", "value": "fun"},# Done
    # {'label':'Statistical',"value":'stats',"disabled":True},
    # {"label": "Box", "value": "box"}, # Done
    # {"label": "Histogram", "value": "hst"}, # Done
]

data = []

def add_figure(go, fig, name, type_, rows, cols, x=[1,2], y=[1,2], index=1):
    if isinstance(rows, str):
        rows = eval(rows)
    if isinstance(cols, str):
        cols = eval(cols)
    
    if not isinstance(rows, (list, tuple)):
        rows = [rows]
    if not isinstance(cols, (list, tuple)):
        cols = [cols]
        
    if type_ == 'line':
        trace = go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name=name
        )
    elif type_ == 'bar':
        trace = go.Bar(
            x=x,
            y=y,
            name=name
        )
    elif type_ == 'box':
        trace = go.Box(
            y=y,
            name=name
        )
    elif type_ == 'hst':
        trace = go.Histogram(
            x=x,
            name=name
        )
    elif type_ == 'fun':
        trace = go.Funnel(
            x = x,
            y = y,
            name = name
        )
    else:
        return fig
    fig.add_trace(trace, row=rows[0], col=cols[0])
    return fig
def add_new_row(data, name, type_, row_num, col_num, x, y):
    if not any(row['Row'] == str(row_num) and row['Col'] == str(col_num) for row in data):
        highest_index = max(int(row['Index']) for row in data) if data else 0
        new_index = str(highest_index + 1)
    else:
        new_index = str(max(int(row['Index']) for row in data) if data else 0)
    
    new_row = {
        "Index": new_index,
        "ID": str(name),
        "Type": str(type_),
        "Row": str(row_num),
        "Col": str(col_num),
        "XData": str(x),
        "YData": str(y)
    }
    
    if not any(trace['ID'] == name for trace in data):
        if isinstance(new_row, dict):  # Ensure only dictionaries are added
            data.append(new_row)
    return new_index

def register_subplots(app, fig, go):
    @app.callback(
        [
            Output('figure-preview', 'figure', allow_duplicate=True),
            Output('trace-table', 'data', allow_duplicate=True),
            Output('axes-select', 'options', allow_duplicate=True)
        ],
        [
            Input('add-trace-button', 'n_clicks'),
            Input('trace-table', 'data')
        ],
        [
            State('trace-table', 'data_previous'),
            State('x-col-select', 'value'),
            State('y-col-select', 'value'),
            State('trace-name', 'value'),
            State('trace-type', 'value'),
            State('row-num', 'value'),
            State('col-num', 'value'),
            State('df-df', 'data'),
            State('figure-preview', 'figure'),
            State('row-total', 'value'),
            State('col-total', 'value'),
            State('ver-spac', 'value'),
            State('horizon-spac', 'value')
        ],
        prevent_initial_call=True
    )
    def update_subplots(
        n_clicks, current_data,
        previous_data, x_col, y_col, name, trace_type, row_num, col_num, df_json, fig,
        rows, cols, v_space, h_space
    ):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        rows = rows or 1
        cols = cols or 1
        v_space = v_space or 0.1
        h_space = h_space or 0.1
        current_data = current_data or []
        previous_data = previous_data or []
        fig = go.Figure(fig)

        # Convert df_json to pandas DataFrame
        df = pd.read_json(StringIO(df_json), orient='split') if df_json else pd.DataFrame()
        current_data = [trace for trace in current_data if isinstance(trace, dict)]
        # Create a new subplot figure
        new_fig = ps.make_subplots(
            rows=rows,
            cols=cols,
            vertical_spacing=v_space,
            horizontal_spacing=h_space,
            start_cell='top-left',
            figure=fig
        )

        # Handle deleted traces
        if previous_data:
            previous_ids = {row["ID"] for row in previous_data if isinstance(row, dict)}
            current_ids = {row["ID"] for row in current_data if isinstance(row, dict)}
            deleted_ids = previous_ids - current_ids

            # Remove traces in one-pass filtering
            new_fig.data = [trace for trace in new_fig.data if trace.name not in deleted_ids]

        # Add a new trace if the add button is clicked
        if triggered_id == 'add-trace-button' and n_clicks and row_num and col_num and name and x_col and y_col:
            if row_num > rows or col_num > cols:
                return new_fig, current_data, [{"label": trace["Index"], "value": trace["Index"]} for trace in current_data]

            if any(trace["ID"] == name for trace in current_data if isinstance(trace, dict)):
                return new_fig, current_data, [{"label": trace["Index"], "value": trace["Index"]} for trace in current_data]

            # Retrieve x and y data from the DataFrame
            if x_col not in df.columns or y_col not in df.columns:
                return new_fig, current_data, [{"label": trace["Index"], "value": trace["Index"]} for trace in current_data]

            x_data = df[x_col]
            y_data = df[y_col]

            # Add the new trace
            new_row = add_new_row(current_data, name, trace_type, row_num, col_num, x_col, y_col)
            current_data.append(new_row)

            new_fig = add_figure(go, new_fig, name, trace_type, [row_num], [col_num], x=x_data, y=y_data)

        # Add traces to the figure
        for trace in current_data:
            if not isinstance(trace, dict):
                continue

            trace_x = df[trace["XData"]] if trace["XData"] in df.columns else [1]
            trace_y = df[trace["YData"]] if trace["YData"] in df.columns else [1]

            if not any(existing_trace.name == trace["ID"] for existing_trace in new_fig.data):
                new_fig = add_figure(
                    go, new_fig, trace["ID"], trace["Type"],
                    [int(trace["Row"])], [int(trace["Col"])], x=trace_x, y=trace_y
                )
        current_data = [trace for trace in current_data if isinstance(trace, dict)]
        print("-"*50)
        print("Current Data:", current_data)
        print("Indeces:", [{"label": trace["Index"], "value": trace["Index"]}
            for trace in current_data])
        print("-"*50)
        axes_options = [
            {"label": trace["Index"], "value": trace["Index"]}
            for trace in current_data
        ]
        if previous_data:
            previous_ids = {row["ID"] for row in previous_data if isinstance(row, dict)}
            current_ids = {row["ID"] for row in current_data if isinstance(row, dict)}
            deleted_ids = previous_ids - current_ids

            # Remove traces in one-pass filtering
            new_fig.data = [trace for trace in new_fig.data if trace.name not in deleted_ids]

        return new_fig, current_data, axes_options

    
    
def register_visuals(app):
    pass

main_figure_table = dt.DataTable(
                        id='trace-table',
                        data=data,
                        columns=[
                            {'name': 'Index' ,'id': 'Index'},
                            {'name': 'ID', 'id': 'ID'},
                            {'name': 'Type', 'id': 'Type'},
                            {'name': 'Row', 'id': 'Row'},
                            {'name': 'Col', 'id': 'Col'},
                            {'name': 'X', 'id': 'XData'},
                            {'name': 'Y', 'id': 'YData'}
                        ],
                        editable=False,
                        row_deletable=True,
                                style_table={
                                    'height': '100%',  # Reduced height
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
                    )

def make_splt(current_rows, current_cols):
    return dbc.Container([
        html.Div([
            dbc.InputGroup([
                dbc.InputGroupText(class_name = "inptext", children="Rows"),
                dbc.Input(id='row-total', type='number', min=1, step=1,
                          value=current_rows, placeholder='Rows'),
                dbc.Tooltip("Set the total number of rows for the subplot grid.", target="row-total"),
                dbc.InputGroupText(class_name = "inptext", children="Columns"),
                dbc.Input(id='col-total', type='number', min=1, step=1,
                          value=current_cols, placeholder='Columns'),
                dbc.Tooltip("Set the total number of columns for the subplot grid.", target="col-total"),
            ], className="mb-3"),
            dbc.InputGroup([
                dbc.InputGroupText(class_name = "inptext", children="Spacing ↕"),
                dbc.Input(id='ver-spac', placeholder='Vertical Spacing',
                          min=0.1, max=1, step=0.05, type='number', value=0.1),
                dbc.Tooltip("Set the vertical spacing between subplots.", target="ver-spac"),
                dbc.InputGroupText(class_name = "inptext", children="Spacing ↔"),
                dbc.Input(id='horizon-spac', placeholder='Horizontal Spacing',
                          min=0.1, max=1, step=0.05, type='number', value=0.1),
                dbc.Tooltip("Set the horizontal spacing between subplots.", target="horizon-spac"),
            ], className="mb-3"),
        ], style={"margin-top": '10px', "margin-bottom": '10px'}),
    ], style={
        "border": "1px solid #007bff",
        "border-radius": "8px",
        "padding": "10px",
        "backgroundColor": "#f9f9f9",
        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
        "marginTop": '15px',
        "fontSize": "12px",  # Reduced font size
    })


def make_trc():
    return dbc.Container([
        html.Div(id='Traces', children=[
            dbc.InputGroup([
                dbc.InputGroupText(class_name = "inptext", children="Type"),
                dbc.Select(options=traces, id='trace-type', value='line'),
                dbc.Tooltip("Select the type of trace to add (e.g., Line, Scatter, Bar).", target="trace-type"),
                dbc.InputGroupText(class_name = "inptext", children="Name"),
                dbc.Input(id='trace-name', placeholder='ID', value='1x1'),
                dbc.Tooltip("Enter a unique name for the trace.", target="trace-name"),
            ], className="mb-3"),
            dbc.InputGroup([
                dbc.InputGroupText(class_name = "inptext", children="Row"),
                dbc.Input(id='row-num', placeholder='Row', type='number', min=1, step=1),
                dbc.Tooltip("Specify the row number for the trace.", target="row-num"),
                dbc.InputGroupText(class_name = "inptext", children="Column"),
                dbc.Input(id='col-num', placeholder='Col', type='number', min=1, step=1),
                dbc.Tooltip("Specify the column number for the trace.", target="col-num"),
            ], className="mb-3"),
            dbc.InputGroup([
                dbc.InputGroupText(class_name = "inptext", children="X"),
                dbc.Select(id='x-col-select', placeholder='X data'),
                dbc.Tooltip("Select the column for the X-axis data.", target="x-col-select"),
                dbc.InputGroupText(class_name = "inptext", children="Y"),
                dbc.Select(id='y-col-select', placeholder='Y Data'),
                dbc.Tooltip("Select the column for the Y-axis data.", target="y-col-select"),
            ], className="mb-3"),
            dbc.Button('Add ➕', id='add-trace-button', n_clicks=0, color="primary", className="w-100"),
            dbc.Tooltip("Click to add the trace to the subplot.", target="add-trace-button"),
            html.Div([
                main_figure_table
            ], style={
                "height": "200px",
                "overflowY": "auto",
                "margin": "10px 0",
                "border": "1px solid #ddd",
                "border-radius": "8px",
                "backgroundColor": "#ffffff",
                "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
            })
        ], style={"margin-top": '10px', "margin-bottom": '10px'}),
    ], style={
        "border": "1px solid #007bff",
        "border-radius": "8px",
        "padding": "10px",
        "backgroundColor": "#f9f9f9",
        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
        "marginTop": '15px',
        "fontSize": "12px",  # Reduced font size
    })


def make_subplots_panel(app, fig, data=data):
    grid_ref = getattr(fig, '_grid_ref', None)
    current_rows = len(grid_ref) if grid_ref else 1
    current_cols = len(grid_ref[0]) if grid_ref and grid_ref else 1

    subplots_form = [
        html.Div([
            html.H5("Subplot Configuration", className="text-primary mb-3", style={"fontSize": "14px"}),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText(class_name="inptext", children="Dimensions"),
                    dbc.Input(id='row-total', type='number', min=1, step=1,
                              value=current_rows, placeholder='Rows'),
                    dbc.Tooltip("Set the total number of rows for the subplot grid.", target="row-total"),
                    dbc.Input(id='col-total', type='number', min=1, step=1,
                              value=current_cols, placeholder='Columns'),
                    dbc.Tooltip("Set the total number of columns for the subplot grid.", target="col-total"),
                ], className="mb-2"),
            ]),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText(class_name="inptext", children="Spacings"),
                    dbc.Input(id='ver-spac', placeholder='Vertical Spacing',
                              min=0.1, max=1, step=0.05, type='number', value=0.1),
                    dbc.Tooltip("Set the vertical spacing between subplots.", target="ver-spac"),
                    dbc.Input(id='horizon-spac', placeholder='Horizontal Spacing',
                              min=0.1, max=1, step=0.05, type='number', value=0.1),
                    dbc.Tooltip("Set the horizontal spacing between subplots.", target="horizon-spac"),
                ], className="mb-2"),
            ]),
        ], style={"margin-bottom": "10px"}),

        html.Div([
            html.H5("Trace Configuration", className="text-primary mb-3", style={"fontSize": "14px"}),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText(class_name="inptext", children="Type"),
                    dbc.Select(options=traces, id='trace-type', value='line'),
                    dbc.Tooltip("Select the type of trace to add (e.g., Line, Scatter, Bar).", target="trace-type"),
                    dbc.InputGroupText(class_name="inptext", children="Name"),
                    dbc.Input(id='trace-name', placeholder='ID', value='1x1'),
                    dbc.Tooltip("Enter a unique name for the trace.", target="trace-name"),
                ], className="mb-2"),
            ]),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText(class_name="inptext", children="Pos"),
                    dbc.Input(id='row-num', placeholder='Row', type='number', min=1, step=1),
                    dbc.Tooltip("Specify the row number for the trace.", target="row-num"),
                    dbc.Input(id='col-num', placeholder='Col', type='number', min=1, step=1),
                    dbc.Tooltip("Specify the column number for the trace.", target="col-num"),
                ], className="mb-2"),
            ]),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText(class_name="inptext", children="Data"),
                    dbc.Select(id='x-col-select', placeholder='X data'),
                    dbc.Tooltip("Select the column for the X-axis data.", target="x-col-select"),
                    dbc.Select(id='y-col-select', placeholder='Y Data'),
                    dbc.Tooltip("Select the column for the Y-axis data.", target="y-col-select"),
                ], className="mb-2"),
            ]),
            dbc.Button('Add ➕', id='add-trace-button', n_clicks=0, color="primary", className="w-100 mb-2"),
            dbc.Tooltip("Click to add the trace to the subplot.", target="add-trace-button"),
            html.Div([
                main_figure_table
            ], style={
                "height": "150px",
                "overflowY": "auto",
                "margin": "5px 0",
                "border": "1px solid #ddd",
                "border-radius": "8px",
                "backgroundColor": "#ffffff",
                "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
            })
        ], style={"margin-bottom": "10px"}),
    ]

    register_subplots(app, fig, go)
    register_visuals(app)
    return html.Div(subplots_form, style={
        "padding": "10px",
        "backgroundColor": "#ffffff",
        "border": "1px solid #ddd",
        "border-radius": "8px",
        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
        "maxHeight": "85vh",  # Limit height to prevent overflow
        "overflowY": "auto",  # Add vertical scrolling if content overflows
        "fontSize": "12px",  # Consistent font size
    })
