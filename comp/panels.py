import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from comp import axis, figure, subplot, data, export
from comp.trace_comp import final
import dash

def span(icon, text):
    return html.Span(
                    [
                        html.Span([icon, html.Span(text)], className="title-button")
                    ]
                )

def register_all_panels(app):
    @app.callback(
        [
            Output("content-data", "style"),
            Output("content-subplots", "style"),
            Output("content-axis", "style"),
            Output("content-figure", "style"),
            Output("content-trace", "style"),
            Output("content-export", "style"),
            Output("left-offcanvas", "title"),
        ],
        [
            Input("btn-data", "n_clicks"),
            Input("btn-subplots", "n_clicks"),
            Input("btn-axis", "n_clicks"),
            Input("btn-figure", "n_clicks"),
            Input("btn-trace", "n_clicks"),
            Input("btn-export", "n_clicks"),
        ],
    )
    def toggle_panels(a,aa,aaa,e,tr,f):
        # Determine which button was clicked
        ctx = dash.callback_context

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Initialize styles and panel title
        content_styles = [{"display": "none"}] * 6
        panel_title = span("📊", "Data")  # Default title

        # Update styles and title based on the clicked button
        if button_id == "btn-data":
            content_styles[0] = {"display": "block"}
            panel_title = span("📊", "Data")
            
        elif button_id == "btn-subplots":
            content_styles[1] = {"display": "block"}
            panel_title = span("📐", "Subplots")
        
        elif button_id == "btn-axis":
            content_styles[2] = {"display": "block"}
            panel_title = span("📏", "Axis")
            
        elif button_id == "btn-figure":
            content_styles[3] = {"display": "block"}
            panel_title = span("📈", "Figure")
            
        elif button_id == "btn-trace":
            content_styles[4] = {"display": "block"}
            panel_title = span("📌", "Trace")
            
        elif button_id == "btn-export":
            content_styles[5] = {"display": "block"}
            panel_title = span("📤", "Export")
            
        return content_styles + [panel_title]

def make_panel(app, fig):
    panels = dbc.Row(
        [
            # Left-side buttons (acting as tabs)
            dbc.Col(
                html.Div(
                    [
                        dbc.Button("📊", id="btn-data", color="primary", className="mb-2", style={"width": "100%"}),
                        dbc.Tooltip("View and manage data.", target="btn-data", placement="top"),
                        
                        dbc.Button("📐", id="btn-subplots", color="primary", className="mb-2", style={"width": "100%"}),
                        dbc.Tooltip("Configure subplots.", target="btn-subplots", placement="top"),
                        
                        dbc.Button("📏", id="btn-axis", color="primary", className="mb-2", style={"width": "100%"}),
                        dbc.Tooltip("Adjust axis settings.", target="btn-axis", placement="top"),
                        
                        dbc.Button("📈", id="btn-figure", color="primary", className="mb-2", style={"width": "100%"}),
                        dbc.Tooltip("Customize the figure.", target="btn-figure", placement="top"),
                        
                        dbc.Button("📌", id="btn-trace", color="primary", className="mb-2", style={"width": "100%"}),
                        dbc.Tooltip("Manage traces.", target="btn-trace", placement="top"),
                        
                        dbc.Button("📤", id="btn-export", color="primary", className="mb-2", style={"width": "100%"}),
                        dbc.Tooltip("Export your work.", target="btn-export", placement="top"),
                    ],
                    style={
                        "height": "100vh",
                        "overflowY": "auto",
                        "backgroundColor": "skyblue",
                        "borderRight": "1px solid #ddd",
                        "border-radius": "8px",
                        "padding": "2px",
                        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
                    },
                ),
                width=2,
                style={"padding": "0", "margin": "0"}  # Remove padding and margin
            ),
            # Right-side content area
            dbc.Col(
                html.Div(
                    [
                        html.Div(data.make_data(app, fig), id="content-data", style={"display": "block"}),
                        html.Div(subplot.make_subplots_panel(app, fig), id="content-subplots", style={"display": "none"}),
                        html.Div(axis.make_axis(app, fig), id="content-axis", style={"display": "none"}),
                        html.Div(figure.make_fig(app, fig), id="content-figure", style={"display": "none"}),
                        html.Div(final.create_all_accordions(app), id="content-trace", style={"display": "none"}),  # Generate accordions here
                        html.Div(export.make_export(app, fig), id="content-export", style={"display": "none"}),
                    ],
                    style={
                        "padding": "2px",
                        "backgroundColor": "#ffffff",
                        "borderRadius": "8px",
                        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.1)",
                        "height": "85vh",  # Adjust height to fit the layout
                        "overflowY": "auto",
                    },
                ),
                width=10,  # Adjust width to fit the layout
                style={"padding": "0", "margin": "0"}  # Remove padding and margin
            ),
        ],
        style={"height": "90vh", "margin": "0", "padding": "0"},  # Remove row spacing
    )
    register_all_panels(app)  # Register the callback for toggling panels
    return panels
