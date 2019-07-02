import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

TREE_LEAF = -2

def imdb_data():
    imdb = pd.read_csv('data/imdb_labelled.txt', sep='\t')
    imdb.columns = ['text', 'sentiment']

    cv = CountVectorizer()
    X = cv.fit_transform(imdb['text'])
    y = imdb['sentiment']

    feature_names = cv.get_feature_names()

    return X, y, feature_names

def generate_elements(tree, feature_names):
    node_count = tree.tree_.node_count
    children_left = tree.tree_.children_left
    children_right = tree.tree_.children_right
    feature = tree.tree_.feature
    threshold = tree.tree_.threshold

    elements = []
    for node in range(node_count):
        #NODES
        if feature[node] == TREE_LEAF:
            node_type = 'leaf'
            node_label = 'leaf'
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

        #EDGES
        if children_left[node] != -1: #read: if node has a left child
            elements.append(
                {'data':
                    {'source': node,
                    'target': children_left[node],
                    'label': 'No'
                    }
                }
            )
        if children_right[node] != -1: #read: if node has a right child
            elements.append(
                {'data':
                    {'source': node,
                    'target': children_right[node],
                    'label': 'Yes'
                    }
                }
            )

    return elements