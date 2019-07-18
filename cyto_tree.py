import dash
from callbacks import get_callbacks
from layout import cyto_layout

app = dash.Dash(__name__)

app.layout = cyto_layout()
get_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)