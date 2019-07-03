shades = ['#F17F71', '#FBF4CB', '#75B78C', '#8F5866']


def stylesheet(n_classes):
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
