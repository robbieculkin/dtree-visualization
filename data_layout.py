import dash_html_components as html

def get_layout(DATA_DIV):
    return html.Div([
        #dummy for input
        html.Div(id='dummy', style={'display': 'none'}),
        #fetched data
        html.Div(id=DATA_DIV, style={'display': 'none'}),
    ])