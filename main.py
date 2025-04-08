import dash
from dash import Output, Input, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.subplots as ps
import os
from comp import panels
from comp.trace_comp import final

width = '25vw'
span = panels.span

# Create initial figure
fig = ps.make_subplots(rows=1, cols=1, start_cell='top-left')
fig = fig.update_layout(template='plotly_white', autosize=True,
                        xaxis=dict(showgrid=True, zeroline=True,
                                linewidth=2, linecolor='lightblue'),
                        yaxis=dict(showgrid=True, zeroline=True,
                                linewidth=2, linecolor='lightblue'),
                        paper_bgcolor='#e4f6fb',
                    )
app = dash.Dash('Data Orbitron',
                title='Data Orbitron',
                external_stylesheets=[dbc.themes.BOOTSTRAP, 
                                    dbc.icons.BOOTSTRAP, 
                                    dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True,
                prevent_initial_callbacks=True)

app.server.secret_key = os.urandom(24)
server = app.server

app.layout = html.Div([
    dcc.Store(id='tab-session', data={'counter': 0}, storage_type='session'),
    
    # Row for the Open Panels button
    dbc.Row(
        dbc.Col(
            dbc.Button(
                "☰ Open Panels", 
                id="open-offcanvas", 
                n_clicks=0, 
                color="primary", 
                className="responsive-button"  # Add a class for custom styling
            ),
            width={"size": "auto"},  # Automatically adjust the column size
            style={'margin': '10px'}  # Add some margin around the button
        ),
        style={'margin-bottom': '10px'}  # Add spacing below the button row
    ),
    
    # Offcanvas for the left panel
    dbc.Offcanvas(
        id="left-offcanvas",
        title=span("📊", "Data"),
        is_open=False,
        children=[
            html.Div(
                panels.make_panel(app, fig),
                style={
                    "width": "100%",
                    "padding": "0px",
                    "boxSizing": "border-box",
                    "height": "100%",  # Ensure it takes full height
                    "overflow": "hidden"  # Prevent scrolling for the entire container
                }
            )
        ],
        placement="start",  # Default placement is "start" (left)
        scrollable=True,
        backdrop=False,  # Remove backdrop for live preview
        style={
            "height": "100vh",
            "overflow": "hidden",  # Prevent scrolling for the Offcanvas
            "transition": "width 0.3s ease-in-out"  # Smooth resizing transition
        }
    ),
    
    # Main Figure Preview
    dbc.Row(
        [
            # Offcanvas column (hidden on mobile)
            dbc.Col(
                dcc.Graph(
                    id='figure-preview',
                    figure=fig,
                    config={'displaylogo': False, 'editable': True},
                    style={'padding': '10px', 'height': '80vh', 'width': '100%'}  # Default full width
                ),
                id='graph-container',
                xs=12, sm=12, md=9, lg=10, xl=10,  # Responsive breakpoints
                style={'padding': '10px', 'width': '100%'}
            )
        ]
    )
], style={'height': '100vh', 'overflow': 'hidden'})
# Callback to toggle the Offcanvas
@app.callback(
    Output("left-offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    State("left-offcanvas", "is_open"),
    prevent_initial_call=True
)
def toggle_offcanvas(n, is_open):
    return not is_open

# Callback to adjust graph width and position dynamically when the Offcanvas is toggled
@app.callback(
    Output("graph-container", "style"),
    Input("left-offcanvas", "is_open")
)
def adjust_graph_position(is_open):
    if is_open:
        return {
            'padding': '10px',
            'width': 'calc(100% - 25vw)',  # Adjust width when Offcanvas is open
            'margin-left': '25vw',  # Shift graph to the right
            'transition': 'all 0.3s ease-in-out'  # Smooth transition for width and margin
        }
    else:
        # Full width when the Offcanvas is closed
        return {
            'padding': '10px',
            'width': '100%',
            'margin-left': '0',
            'transition': 'all 0.3s ease-in-out'  # Smooth transition for width and margin
        }
final.register_traces(app, fig)

if __name__ == '__main__':
    app.run(debug=False)