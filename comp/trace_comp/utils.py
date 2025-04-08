import dash_bootstrap_components as dbc
from dash import Output, Input, State

def query_trace(app, output, type_):
    @app.callback(
        Output(output, "options"),
        [Input('figure-preview', "figure"),
         Input('btn-trace', "n_clicks")]
    )
    def toggle_panel(figure, btn_trace):
        # Simulate button click and figure data
        if btn_trace is None:
            btn_trace = 0
        btn_trace += 1  # Simulate button click increment

        if not figure or 'data' not in figure:
            return []

        trace = []
        for t in figure['data']:
            if type_ == 'scatter' or type_ == 'bubbles' or type_ == 'sca':
                if t.get('type', '') == 'scatter':
                    trace.append({
                        "label": t.get('name', ''),
                        "value": t.get('name', '')
                    })
            elif type_ == 'bar':
                if t.get('type', '') == 'bar':
                    trace.append({
                        "label": t.get('name', ''),
                        "value": t.get('name', '')
                    })
            else:
                if t.get('type', '') == type_:
                    trace.append({
                        "label": t.get('name', ''),
                        "value": t.get('name', '')
                    })
        return trace
