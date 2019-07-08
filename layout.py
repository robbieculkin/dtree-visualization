import dash_cytoscape as cyto
import dash_html_components as html

def cyto_layout():
    cyto.load_extra_layouts()

    return html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            layout={
                'name': 'dagre',
                'nodeDimensionsIncludeLabels': True,
            },
            elements=[],
            style={'width': 'auto', 'height': '100vh'},
        ),

        #data source TODO make upload button
        html.Div(id='dummy', style={'display': 'none'}),
        #vectorized data
        html.Div(id='prepped-data', style={'display': 'none'}),
        #class and feature names
        html.Div(id='names', style={'display': 'none'}),
        #decision tree
        html.Div(id='tree', style={'display': 'none'})
    ])