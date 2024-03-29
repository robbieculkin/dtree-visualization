import dash_cytoscape as cyto
import dash_html_components as html

def get_layout():
    cyto.load_extra_layouts()

    return html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            layout={
                'name': 'dagre',
                'nodeDimensionsIncludeLabels': True,
                'animate': True,
            },
            elements=[],
            style={'width': 'auto', 'height': '100vh'},
        ),

        #class and feature names
        html.Div(id='names', style={'display': 'none'}),
        #decision tree
        html.Div(id='tree', style={'display': 'none'}),
        #visible nodes
        html.Div(id='visible', style={'display': 'none'}),
        #collapsed leaves
        html.Div(id='collapsed_leaf', style={'display': 'none'}),
    ])