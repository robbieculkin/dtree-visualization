import dash
import dash_html_components as html
import cyto_callbacks
import cyto_layout
import data_callbacks
import data_layout

DATA_DIV = 'data'
app = dash.Dash(__name__)

app.layout = html.Div([
    data_layout.get_layout(DATA_DIV),
    cyto_layout.get_layout(),
])

data_callbacks.get_callbacks(app, DATA_DIV)
cyto_callbacks.get_callbacks(app, DATA_DIV)

if __name__ == '__main__':
    app.run_server(debug=True)