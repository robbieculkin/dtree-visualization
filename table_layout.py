import dash_html_components as html
import dash_table

def get_layout():
    return dash_table.DataTable(
        id='table',
        style_data={'whiteSpace': 'normal'},
        style_table={
            'height': '600px',
            'overflowY': 'scroll',
            'border': 'thin lightgrey solid'
        },
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        page_size=10,
    )