import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import matplotlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict
from dash.dependencies import Input, Output
from dash_table.Format import Format, Scheme, Sign, Symbol


#--------- Pandas Dataframe
## Pandas dataframe manipulation
df = pd.read_csv('Capcom_Cup_2018_SQL')
df.drop(columns = ['id'], inplace = True)
df.columns=['Player', 'Character', 'Region', 'Tour Points', 'Tour Earnings', 'Placement']
df


#--------- Sorting the dataframe by various features to plot the sorted axes
# Sort alphabetically the region and character features
sorted_alphabetical_region = df.sort_values(by = ['Region'])
sorted_alphabetical_chars = df.sort_values(by = ['Character'])

# Sort by frequency of the region feature
sorted_freq_region = df.assign(freq = df.groupby('Region')['Region'].transform('count'))\
  .sort_values(by = ['freq','Region'],ascending=[False,True]).loc[:,['Region']]

# Sort by frequency of the character feature
sorted_freq_character = df.assign(freq = df.groupby('Character')['Character'].transform('count'))\
  .sort_values(by = ['freq','Character'],ascending = [False,True]).loc[:,['Character']]

# Sort by the number of tour points
df['TP_sum'] = df.groupby('Region')['Tour Points'].transform('sum')
sorted_TP = df.sort_values(by = ['TP_sum'], ascending = False)

# Sort by the number of tour earnings
df['TE_sum'] = df.groupby('Region')['Tour Earnings'].transform('sum')
sorted_TE = df.sort_values(by = ['TE_sum'], ascending = False)


#--------- Use the selected sorted dataframes for plots: Distribution of Region, Character and a heatmap of the Regional Character & Placements
## Regional Distribution Plot
### Plotly express histogram - setting parameters
histogram_region = px.histogram(sorted_freq_region, x = "Region",
                                color = 'Region', height = 500)
## Updating the axes/layout of the figure
histogram_region.update_xaxes(automargin = True)
histogram_region.update_yaxes(title = 'Number of Participants', 
                              automargin = True)
histogram_region.update_layout(margin = {"t": 10, "l": 20, "r": 10})


## Character Distribution Plot
### Plotly express histogram - setting parameters
histogram_character = px.histogram(sorted_freq_character, x = "Character",
                                   color = 'Character', height = 500)
### Updating the axes/layout of the figure
histogram_character.update_xaxes(automargin = True)
histogram_character.update_yaxes(title='Number of Participants',
                                 automargin = True)
histogram_character.update_layout(margin =  {"t": 10, "l": 20, "r": 10})

## Regional Placements & Character Plot
### Category order of the axes
order = ['China', 'Dominican Republic', 'France', 'Japan', 'Norway', 'Peru', 'Singapore', 'South Korea', 
         'Taiwan', 'United Arab Emirates', 'United Kingdom', 'United States of America']

### Plotly graphing object to create Heatmap using the Region, Placement, and Characters of the participants
heatmap = go.Figure(
    {
        'data': [go.Heatmap(
            z=sorted_alphabetical_chars['Placement'],
            x=sorted_alphabetical_chars['Region'],
            y=sorted_alphabetical_chars['Character']
        )
                ],
        'layout' : go.Layout(
            xaxis = {'title':'Region', 'categoryarray': order, "automargin": True },
            yaxis = {'title':'Character', "automargin": True},
            height = 500,
            margin =  {"t": 10, "l": 20, "r": 10}
        )
    }
)


#--------- Dashboard
## Importing Logo and encoding it
image_filename = 'Capcom_Cup_2018.png' # replace with your own image
encoded_image = base64.b64encode(
    open(image_filename, 'rb').read())

## CSS stylesheet for formatting
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## Instantiating the dashboard application
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True

## Setting up the dashboard layout
app.layout = html.Div(
    [

### Inserting Logo into Heading and centering it
        html.Div(
            [
                html.Img(src='data:image/png;base64,{}'
                         .format(encoded_image.decode())
                        )
            ],
            style = 
            {
                'display': 'flex', 'align-items': 'center',
                'justify-content': 'center', 'backgroundColor': '#008EFF'
            }
        ),

### Inserting Datatable Header               
        html.Div(
            [
                html.H2("Capcom Cup 2018 Roster")
            ]
        ),
    
### Inserting in Datatable
        dash_table.DataTable( 
            id = 'typing_formatting_1',
            data = df.to_dict('records'),
            columns =
            [
                {
                    'id': 'Player',
                    'name': 'Player',
                    'type': 'text'
                }, 

                {
                    'id': 'Region',
                    'name': 'Region',
                    'type': 'text'
                }, 

                {
                    'id': 'Character',
                    'name': 'Character',
                    'type': 'text'
                }, 

                {
                    'id': 'Tour Points',
                    'name': 'Tour Points',
                    'type': 'numeric'
                }, 

                {
                    'id': 'Tour Earnings',
                    'name': 'Tour Earnings ($)',
                    'type': 'numeric',
                    'format': FormatTemplate.money(0)
                },  

                {
                    'id': 'Placement',
                    'name': 'Placement',
                    'type': 'numeric'

                }
            ],

### Highlight Cells based on conditions - first, second, and third row
            style_data_conditional =
            [
                {
                    "if": {"row_index": 0},
                    "backgroundColor": "#FFD700",
                    'color': 'black'

            },

                {
                    "if": {"row_index": 1},
                    "backgroundColor": "#C0C0C0",
                    'color': 'black'

                },

                {
                    "if": {"row_index": 2},
                    "backgroundColor": "#CD7F32",
                    'color': 'black'

                }
            ],

### Formatting the data/headers cells
            style_cell = {'backgroundColor': 'rgb(255, 245, 205)'},

            style_data = {'border': '1px solid blue',
                          'font-size': 18 
                         },

            style_header = { 'border': '2px solid gold',
                           'font-size': 21
                           },
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 35,
        ),
        html.Div(id='typing_formatting_1-container')
    ]
)




### Datatable callback for interactivity

@app.callback(
    Output('typing_formatting_1-container',
           'style_data_conditional'),
    [Input('typing_formatting_1-container',
           'selected_columns')
    ]
) 

def update_styles(selected_columns):
    """Updates the colors of datatable if selected by user"""
    return [
        {
            'if': { 'column_id': i },
            'background_color': '#D2F3FF'
        } for i in selected_columns
		]


### Datatable callback for the update_graphs function
@app.callback(
    Output('typing_formatting_1-container',
           "children"),
    [Input('typing_formatting_1',
           "derived_virtual_data"),
     Input('typing_formatting_1',
           "derived_virtual_selected_rows")
    ]
)


### Function to update two graphs : Regional Tour Points & Earnings
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = sorted_TP if rows is None else pd.DataFrame(rows)
    
    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
### Headers for plots
        html.Div(
            [
                html.H2("Regional Tour Points & Earnings")
            ]
        ),
# Tour Points Plot
        dcc.Graph(
            id="Tour Points",
            figure = {
                "data": [
                    {
                        "x": sorted_TP["Region"],
                        "y": sorted_TP["Tour Points"],
                        "type": "bar",
                        'mode' : 'markers',
                        'name': 'index',
                        "marker": {"color": colors}
                    }
                ],
                "layout": {
                    
                    "xaxis": {"automargin": True,
                              'title': 'Region'},
                    "yaxis": {"automargin": True,
                              "title": {"text": 'Tour Points'}
                             },
                    "height": 500,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        ),


# Tour Earnings Plot        
        dcc.Graph(
            id="Tour Earnings",
            figure={
                "data": [
                    {
                        "x": sorted_TE["Region"],
                        "y": sorted_TE["Tour Earnings"],
                        "type": "bar",
                        'mode' : 'markers',
                        'name': 'index',
                        "marker": {"color": colors}
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True,
                              'title': 'Region'},
                    "yaxis": {"automargin": True,
                        "title": {"text": 'Tour Earnings'}
                    },
                    "height": 500,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        ),

# Insert the number of players in each country plot with header
        html.Div(
            [
                html.H2("Regional & Character Distributions")
            ]
        ),
        dcc.Graph( figure = histogram_region),

# Insert the character Distribution plot
        dcc.Graph(figure = histogram_character),


# Insert the characters from each region and placement plot with header
        html.Div(
            [
                html.H2("Regional Placements with Character Selection")
            ]
        ),
        dcc.Graph( figure = heatmap),     
    ]

    

if __name__ == '__main__':
    app.run_server(debug=True)