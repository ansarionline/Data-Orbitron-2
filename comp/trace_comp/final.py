from . import *
from dash import Output, Input, State, html
import dash_bootstrap_components as dbc
from dash import callback_context

def create_all_accordions(app):
    style={
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "8px",
        "backgroundColor": "#f9f9f9",
        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.1)",
        "display": "none",
    }
    return dbc.Container([
        html.Div(
                id="line-accord",
                children=line.make_line(app),
                style=style
            ),
        html.Div(
                id="bar-accord",
                children=bar.make_bar(app),
                style=style
            )
    ])


def show_or_hide(accord_id, app):
    @app.callback(
        Output(accord_id, 'style'),
        [
            Input('trace-table', 'data'),
            Input('btn-trace', 'n_clicks'),
            Input('content-trace', 'style')  # Listen to the visibility of the content-trace panel
        ],
        State(accord_id, 'style'),
    )
    def toggle(data, btn_clicks, content_trace_style, style):
        trace_ = accord_id.split('-')[0]
        
        # Check if the content-trace panel is visible
        if content_trace_style and content_trace_style.get("display") != "block":
            return {"display": "none"}  # Hide the accordion if the panel is not visible

        # Simulate button clicks
        if btn_clicks is None:
            btn_clicks = 0
        btn_clicks += 1
        # Check if data is empty
        if not data or len(data) == 0:
            return {**style, "display": "none"}  # Return a new dictionary with updated display

        # Check if the trace type exists in the data
        has_trace_ = any(row.get('Type', '').lower() == trace_ for row in data)
        if has_trace_:
            return {**style, "display": "block"}  # Return a new dictionary with updated display

        return {**style, "display": "none"}  # Default to hiding if no matching trace is found
        
def register_all(app, fig):
    line.register_line(app, fig)
    bar.register_bar(app, fig)

def register_traces(app, fig):
    show_or_hide('line-accord', app)
    show_or_hide('bar-accord', app)
    register_all(app, fig)