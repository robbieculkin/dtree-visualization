import pandas as pd
from dash.dependencies import Input, Output

def get_callbacks(app, data_div):
    @app.callback([Output('table', 'columns'),
                   Output('table', 'data')],
                 [Input(data_div, 'children')])
    def populate_table(data):
        if data is None:
            print('no data')
            return None, None

        df = pd.read_json(data).reset_index()
        columns=[{"name": i, "id": i} for i in df.columns]
        data=df.to_dict('records')
        return columns, data