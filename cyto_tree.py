import dash
from sklearn.tree import DecisionTreeClassifier
from callbacks import generate_elements, imdb_data
from layout import cyto_layout

app = dash.Dash(__name__)

X, y, feature_names = imdb_data()
class_names = ['negative', 'positive']
n_classes = 2
tree = DecisionTreeClassifier(max_leaf_nodes=10, random_state=0)
tree.fit(X, y)

elements = generate_elements(tree, feature_names, class_names)
app.layout = cyto_layout(elements, n_classes)


if __name__ == '__main__':
    app.run_server(debug=True)