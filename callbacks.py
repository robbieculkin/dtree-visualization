import json
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from dash.dependencies import Input, Output, State

TREE_LEAF = -2
shades = ['#F17F71', '#FBF4CB', '#75B78C', '#8F5866']


def get_callbacks(app):
    @app.callback(Output('prepped-data', 'children'),
                  [Input('dummy', 'children')])
    def load_data(dummy):
        data = pd.read_csv('data/imdb_labelled.txt', sep='\t')
        data.columns = ['X', 'y']

        return data.to_json()

    @app.callback([Output('tree', 'children'),
                   Output('names', 'children')],
                  [Input('prepped-data', 'children')])
    def fit_tree(data):
        data = pd.read_json(data)

        cv = CountVectorizer()
        X = cv.fit_transform(data['X'])
        y = data['y']

        feature_names = cv.get_feature_names()
        class_names = y.unique().tolist()
        names = {
            'feature': feature_names,
            'class': class_names
        }

        tree = DecisionTreeClassifier(max_leaf_nodes=10, random_state=0)
        tree.fit(X, y)

        tree_info = {
            'node_count': tree.tree_.node_count,
            'children_left': tree.tree_.children_left.tolist(),
            'children_right': tree.tree_.children_right.tolist(),
            'value': tree.tree_.value.tolist(),
            'feature': tree.tree_.feature.tolist(),
            'threshold': tree.tree_.threshold.tolist()
        }

        return json.dumps(tree_info), json.dumps(names)

    @app.callback(Output('cytoscape', 'elements'),
                  [Input('tree', 'children'),
                   Input('names', 'children')],
                  [State('cytoscape', 'elements'),])
    def generate_elements(tree_json, names_json, elements):
        if tree_json is None or names_json is None:
            return []

        tree = json.loads(tree_json)
        node_count = tree['node_count']
        children_left = tree['children_left']
        children_right = tree['children_right']
        feature = tree['feature']
        value = tree['value']
        threshold = tree['threshold']

        names = json.loads(names_json)
        feature_names = names['feature']
        class_names = names['class']

        elements = []
        for node in range(node_count):
            # NODES
            node_class = np.argmax(value[node])
            if feature[node] == TREE_LEAF:
                node_type = f'leaf-{node_class}'
                node_label = class_names[node_class]
            else:
                node_type = 'nonleaf'
                node_label = str(feature_names[feature[node]])

            elements.append(
                {'data':
                    {'id': str(node),
                     'label': node_label,
                     'type': node_type
                     },
                 'classes': 'center-center'
                 }
            )

            # EDGES
            if children_left[node] != -1:  # read: if node has a left child
                elements.append(
                    {'data':
                        {'source': node,
                         'target': children_left[node],
                         'label': 'No'
                         }
                     }
                )
            if children_right[node] != -1:  # read: if node has a right child
                elements.append(
                    {'data':
                        {'source': node,
                         'target': children_right[node],
                         'label': 'Yes'
                         }
                     }
                )

        return elements

    @app.callback(Output('cytoscape', 'stylesheet'),
                 [Input('names', 'children')])
    def stylesheet(names_json):
        if names_json is None:
            return []

        names = json.loads(names_json)
        n_classes = len(names['class'])

        sheet = [
            {
                "selector": "node",
                "style": {
                    "content": "",
                    "width": 25,
                    "height": 25,
                    "background-color": "#84b1fa",
                    "background-blacken": 0,
                    "background-opacity": 1,
                    "shape": "circle",
                    "border-width": 1,
                    "border-style": "double",
                    "border-color": "#999999",
                    "border-opacity": 1,
                    "padding": "0px",
                    "padding-relative-to": "height",
                    "compound-sizing-wrt-labels": "include",
                    "min-width": 0,
                    "min-width-bias-left": 0,
                    "min-width-bias-right": 0,
                    "min-height": 0,
                    "min-height-bias-top": 0,
                    "min-height-bias-bottom": 0,
                    "background-width": "auto",
                    "background-height": "auto",
                    "label": "data(label)",
                    "color": "black",
                    "text-opacity": 1,
                    "font-family": "helvetica",
                    "font-size": 10,
                    "font-style": "normal",
                    "font-weight": "normal",
                    "text-transform": "none",
                    "text-wrap": "none",
                    "text-halign": "center",
                    "text-valign": "center",
                    "text-margin-x": 0,
                    "text-margin-y": 0
                }
            },
            {
                "selector": "edge",
                "style": {
                    "curve-style": "haystack",
                    "line-color": "#999999",
                    "line-style": "solid",
                    "loop-direction": "-45deg",
                    "loop-sweep": "-90deg",
                    "source-arrow-color": "#999999",
                    "mid-source-arrow-color": "#999999",
                    "target-arrow-color": "#999999",
                    "mid-target-arrow-color": "#999999",
                    "source-arrow-shape": "none",
                    "mid-source-arrow-shape": "none",
                    "target-arrow-shape": "triangle",
                    "mid-target-arrow-shape": "none",
                    "source-arrow-fill": "filled",
                    "mid-source-arrow-fill": "filled",
                    "target-arrow-fill": "filled",
                    "mid-target-arrow-fill": "filled",
                    "label": "data(label)",
                    "source-label": "",
                    "target-label": "",
                    "color": "black",
                    "text-opacity": 1,
                    "font-family": "helvetica",
                    "font-size": 8,
                    "font-style": "italic",
                    "font-weight": "lighter",
                    "text-transform": "none",
                    "text-wrap": "none",
                    "text-max-width": 100,
                }
            }
        ]

        for class_id in range(n_classes):
            class_id = class_id % len(shades)
            sheet.append(
                {
                    "selector": f'node[type="leaf-{class_id}"]',
                    "style": {
                        "background-color": shades[class_id]
                    }
                }
            )

        return sheet

