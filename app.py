import dash
import dash_html_components as html
import cyto_callbacks
import cyto_layout
import data_callbacks
import data_layout
import table_callbacks
import table_layout

DATA_DIV = 'data'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

app.layout = html.Div([
    data_layout.get_layout(DATA_DIV),
    html.Div(
        children=[cyto_layout.get_layout()],
        className='seven columns',
    ),
    html.Div(
        children=[table_layout.get_layout()],
        className='four columns',
    ),
])

data_callbacks.get_callbacks(app, DATA_DIV)
cyto_callbacks.get_callbacks(app, DATA_DIV)
table_callbacks.get_callbacks(app, DATA_DIV)

if __name__ == '__main__':
    app.run_server(debug=True)