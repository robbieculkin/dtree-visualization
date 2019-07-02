import dash_cytoscape as cyto
import dash_html_components as html
from stylesheet import stylesheet

def cyto_layout(elements):
    cyto.load_extra_layouts()

    return html.Div([
        cyto.Cytoscape(
            id='cytoscape-two-nodes',
            layout={
                'name': 'dagre',
                'nodeDimensionsIncludeLabels': True,
            },
            style={'width': 'auto', 'height': '100vh'},
            elements=elements,
            stylesheet=stylesheet,
        )
    ])