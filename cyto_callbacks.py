import json
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from dash.dependencies import Input, Output, State

ROOT_NODE = 0
TREE_LEAF = -2
DEFAULT_MAX_DEPTH = 10
DEPTH_ON_CLICK = 3
SHADES = ['#F17F71', '#FBF4CB', '#75B78C', '#8F5866']

#TODO known bug: collapsed nodes sometimes require 2 clicks to display childrens

def generate_node_element(node_id, tree, names, collapsed_leaf=False):
    node_class = np.argmax(tree['value'][node_id])
    if tree['feature'][node_id] == TREE_LEAF:
        node_type = f'leaf-{node_class}'
        node_label = names['class'][node_class]
    elif collapsed_leaf:
       node_type = 'collapsed_leaf'
       node_label = '...'
    else:
        node_type = 'nonleaf'
        node_label = str(names['feature'][tree['feature'][node_id]])

    return {
        'data':
        {
            'id': str(node_id),
            'label':str(node_label),
            'type': node_type
        },
        'classes': 'center-center'
    }

def generate_edge_elements(node_id, tree):
    edge_elements = []
    left_child = tree['children_left'][node_id]
    right_child = tree['children_right'][node_id]
    if left_child != -1:  # read: if node has a left child
        edge_elements.append(
            {'data':
                {
                    'source': node_id,
                    'target': left_child,
                    'label': 'No',
                    'type' : 'edge'
                }
            })
    if right_child != -1:  # read: if node has a right child
        edge_elements.append(
            {'data':
                {
                    'source': node_id,
                    'target': right_child,
                    'label': 'Yes',
                    'type' : 'edge'
                    }
                })
    return edge_elements

def child_nodes(root_id, tree, max_depth=-1):
    if max_depth == 0 or root_id == -1:
        return []

    visible_nodes = [root_id]

    left_child = tree['children_left'][root_id]
    right_child = tree['children_right'][root_id]

    visible_nodes += child_nodes(left_child, tree, max_depth-1)
    visible_nodes += child_nodes(right_child, tree, max_depth-1)

    return visible_nodes

def collapsed_leaves(tree, visible):
    collapsed_leaf = []
    for node_id in range(tree['node_count']):
        if node_id in visible:
            children = set(child_nodes(node_id, tree, -1)) - set([node_id])
            if children.isdisjoint(set(visible)):
                collapsed_leaf.append(node_id)
    return collapsed_leaf

def get_callbacks(app, data_div):

    @app.callback([Output('tree', 'children'),
                   Output('names', 'children')],
                  [Input(data_div, 'children')])
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

        tree = DecisionTreeClassifier(max_leaf_nodes=None, random_state=0)
        tree.fit(X, y)

        tree_info = {
            'node_count': tree.tree_.node_count,
            'children_left': tree.tree_.children_left.tolist(),
            'children_right': tree.tree_.children_right.tolist(),
            'value': tree.tree_.value.tolist(),
            'feature': tree.tree_.feature.tolist(),
            'threshold': tree.tree_.threshold.tolist(),
            'max_depth': tree.tree_.max_depth
        }

        return json.dumps(tree_info), json.dumps(names)

    @app.callback(Output('cytoscape', 'elements'),
                  [Input('tree', 'children'),
                   Input('names', 'children'),
                   Input('visible', 'children')],
                  [State('cytoscape', 'elements'), ])
    def generate_elements(tree_json, names_json, visible, elements):
        if tree_json is None or names_json is None:
            return []

        tree = json.loads(tree_json)
        names = json.loads(names_json)

        elements = []
        default_depth = min(tree['max_depth'], DEFAULT_MAX_DEPTH) +1
        if visible is None:
            visible = child_nodes(0, tree, default_depth)

        for node_id in range(tree['node_count']):
            if visible is None or node_id in visible:
                children = set(child_nodes(node_id, tree, -1)) - set([node_id])
                collapsed_leaf = children.isdisjoint(set(visible))

                elements.append(generate_node_element(node_id, tree, names, collapsed_leaf))
                elements += generate_edge_elements(node_id, tree)

        return elements

    @app.callback((Output('visible', 'children'),
                   Output('collapsed_leaf', 'children')),
                 [Input('cytoscape', 'tapNodeData'),
                  Input('tree', 'children')],
                 [State('visible', 'children'),
                  State('collapsed_leaf', 'children')])
    def on_click(clicked_node_data, tree_json, visible, collapsed_leaf):
        #need a tree to do anything
        if tree_json is None:
            return visible, collapsed_leaf

        tree = json.loads(tree_json)
        #on first load
        if visible is None and collapsed_leaf is None:
            #default nodes
            visible = child_nodes(0, tree, DEFAULT_MAX_DEPTH)
            collapsed_leaf = collapsed_leaves(tree, visible)
            return visible, collapsed_leaf

        clicked_node_id = int(clicked_node_data['id'])
        clicked_node_children = set(child_nodes(clicked_node_id, tree)) - set([clicked_node_id])
        shallow_children = set(child_nodes(clicked_node_id, tree, max_depth=DEPTH_ON_CLICK)) - set([clicked_node_id])


        if clicked_node_id in visible and clicked_node_id not in collapsed_leaf: #TODO
            #remove all children of a node that has been
            visible = list(set(visible) - clicked_node_children)
            collapsed_leaf.append(clicked_node_id)
        else:
            visible = list(set(visible).union(shallow_children))
            collapsed_leaf = list(set(collapsed_leaf) - set([clicked_node_id]))
        return visible, collapsed_leaf

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
            },
            {
                "selector": f'node[type="collapsed_leaf"]',
                "style": {
                    "content": "",
                    "width": 25,
                    "height": 25,
                    "background-color": "#818182",
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
        ]

        for class_id in range(n_classes):
            class_id = class_id % len(SHADES)
            sheet.append(
                {
                    "selector": f'node[type="leaf-{class_id}"]',
                    "style": {
                        "background-color": SHADES[class_id]
                    }
                }
            )

        return sheet
