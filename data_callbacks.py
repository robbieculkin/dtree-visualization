from dash.dependencies import Input, Output
import pandas as pd

def get_callbacks(app, data_div):
    @app.callback(Output(data_div, 'children'),
                  [Input('dummy', 'children')])
    def load_data(dummy):
        data = pd.read_csv('data/imdb_labelled.txt', sep='\t')
        data.columns = ['X', 'y']

        return data.to_json()