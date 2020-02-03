from collections import OrderedDict
from dash.dependencies import Input, Output
from dash_table.Format import Format, Scheme, Sign, Symbol
from plotly.graph_objs import *
from scipy import stats
from sklearn.model_selection import train_test_split

import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


#--------- Pandas Dataframe
orig = pd.read_csv('data/PUBG_Player_Statistics.csv')

## Create a copy of the dataframe
df = orig.copy()
cols = np.arange(52, 152, 1)

## Drop columns after the 52nd index
df.drop(df.columns[cols], axis = 1, inplace = True)

## Drop player_name and tracker id
df.drop(df.columns[[0, 1]], axis = 1, inplace = True)

## Drop Knockout and Revives
df.drop(df.columns[[49]], axis = 1, inplace = True)
df.drop(columns = ['solo_Revives'], inplace = True)

## Drop the string solo from all strings
df.rename(columns = lambda x: x.lstrip('solo_').rstrip(''), inplace = True)

## Combine a few columns 
df['TotalDistance'] = df['WalkDistance'] + df['RideDistance']
df['AvgTotalDistance'] = df['AvgWalkDistance'] + df['AvgRideDistance']

# Create train and test set using Sci-Kit Learn
train, test = train_test_split(df, test_size=0.1)
dev, test = train_test_split(test, test_size = 0.5)
df = train

#--------- Dashboard
## Importing Logo and encoding it
image_filename = 'images/PUBG_Logo.png' 
encoded_image = base64.b64encode(
    open(image_filename, 'rb').read())


## Importing Plots and encoding it
### Histogram
image_filename = 'images/Histogram_Plots.png' 
encoded_image1 = base64.b64encode(
    open(image_filename, 'rb').read())

### Q-Q Plot
image_filename = 'images/Probability_Plot_1.png' 
encoded_image2 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Probability_Plot_2.png' 
encoded_image3 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Probability_Plot_3.png' 
encoded_image4 = base64.b64encode(
    open(image_filename, 'rb').read())

### Discretized Distributions
image_filename = 'images/Distribution_Kills.png' 
encoded_image5 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Kill-Death-Ratio.png' 
encoded_image6 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Headshots.png' 
encoded_image7 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Headshot-Kill-Ratio.png' 
encoded_image8 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Wins.png' 
encoded_image9 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Win-Ratio.png' 
encoded_image10 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Top10s.png' 
encoded_image11 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Top10-Ratio.png' 
encoded_image12 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Total-Distance.png' 
encoded_image13 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Average-Distance.png' 
encoded_image14 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Time-Survived.png' 
encoded_image15 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Average-Time-Survived.png' 
encoded_image16 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Rounds-Played.png' 
encoded_image17 = base64.b64encode(
    open(image_filename, 'rb').read())

image_filename = 'images/Distribution_Damage-Per-Game.png' 
encoded_image18 = base64.b64encode(
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
                html.Img(src = 'data:image/png;base64,{}'
                         .format(encoded_image.decode())
                        )
            ],
            
            style = 
            {
                'display': 'flex', 'align-items': 'center',
                'justify-content': 'center'
            }
        ),

### Inserting Datatable Header               
        html.Div(
            [
                html.H2("Playerunknown's Battleground Match Statistics")
            ]
        ),
        html.Div(
            [
                dcc.Markdown(
                    ''' 
                    * Dataset distributed through Kaggle on a successfully popular multiplayer video game, Playerunknown's Battlegrounds.
                    * The dataset includes various features on the performance of an individual player collected through their match history.
                    
                    '''
                )
            ]
        ),

### Inserting in Datatable
        dash_table.DataTable( 
            id = 'typing_formatting_1',
            data = df.to_dict('records'),
            columns =
            [
                {
                    'id': 'Kills',
                    'name': 'Kills',
                    'type': 'numeric'
                }, 

                {
                    'id': 'KillDeathRatio',
                    'name': 'Kill-Death Ratio',
                    'type': 'numeric'
                }, 

                {
                    'id': 'HeadshotKills',
                    'name': 'Headshot Kills',
                    'type': 'numeric'
                }, 

                {
                    'id': 'HeadshotKillRatio',
                    'name': 'Headshot-Kill Ratio',
                    'type': 'numeric'
                }, 

                {
                    'id': 'Wins',
                    'name': 'Wins',
                    'type': 'numeric',
                },  

                {
                    'id': 'WinRatio',
                    'name': 'WinRatio (%)',
                    'type': 'numeric'

                },
                {
                    'id': 'Top10s',
                    'name': 'Top 10s',
                    'type': 'numeric'

                },
                {
                    'id': 'Top10Ratio',
                    'name': 'Top 10 Ratio',
                    'type': 'numeric'

                },
                {
                    'id': 'TotalDistance',
                    'name': 'Total Distance',
                    'type': 'numeric'

                },
                {
                    'id': 'AvgTotalDistance',
                    'name': 'Average Total Distance (miles)',
                    'type': 'numeric'

                },
                
                {
                    'id': 'TimeSurvived',
                    'name': 'Survival Time (s)',
                    'type': 'numeric'

                },
                
                {
                    'id': 'AvgSurvivalTime',
                    'name': 'Average Survival Time (s)',
                    'type': 'numeric'

                },
                

                {
                    'id': 'RoundsPlayed',
                    'name': 'Rounds Played',
                    'type': 'numeric'

                },
                                {
                    'id': 'DamagePg',
                    'name': 'Damage Per Game',
                    'type': 'numeric'

                },
                
            ],



### Formatting the data/headers cells
            style_cell = 
            {
                'backgroundColor': 'rgb(255, 245, 205)','height': 'auto',
                'minWidth': '0px', 'maxWidth': '300px',
                'whiteSpace': 'normal'
            },

            style_data = 
            {
                'border': '1px solid blue',
                'font-size': 18 
            },

            style_header = 
            {
                'border': '2px solid gold',
                'font-size': 21
            },
            editable = True,
            filter_action = "native",
            sort_action = "native",
            sort_mode = "multi",
            column_selectable = "single",
            row_selectable = "multi",
            row_deletable = True,
            selected_columns = [],
            selected_rows = [],
            page_action = "native",
            page_current = 0,
            page_size = 20,
        
        ),
        html.Div(id = 'typing_formatting_1-container'),
        
        html.Div(
            [
                html.H2("Continuous Representations")
            ]
        ),
        
# Markdown on Continuous Representations
        html.Div(
            [
                dcc.Markdown(
                    '''
                    * Examine the distribution of each feature if its left-skewed, normal, or right-skewed.
                    
                    '''
                )
            ]
        ),
        
# Insert Header for Histograms
        html.Div(
            [
                html.H3("Feature Distributions")
            ]
        ),
        html.Div(
            [
                dcc.Markdown(
                    ''' 
                    * Most features are right-skewed; only Average Survival Time appears to be normal.
                    
                    ''')
            ]
        ),

# Insert Histogram Plots
        html.Div(
            [
                html.Img(src = 'data:image/png;base64,{}'
                         .format(encoded_image1.decode())
                        )
            ],
            style = 
            {
                'display': 'flex', 'align-items': 'center',
                'justify-content': 'center'
            }
        ),    

# Insert Header for Probability Plots
        html.Div(
            [
                html.H3("Q-Q Plots")
            ]
        ),
        html.Div(
            [
                dcc.Markdown(
                    ''' 
                    * Verify our initial claims from the histograms by examining linear behavior in Q-Q plots.
                    * Average Survival Time exhibits linear behavior and is normal.
                    
                    '''
                )
            ]
        ),

# Insert Q-Q Plots
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                         .format(encoded_image2.decode()), className = "four columns")
                    ],
                ), 
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image3.decode()), className = "four columns")
                    ],
                ), 
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image4.decode()), className = "four columns")
                    ],
                ),
            ], className = 'row'
        ),

# Insert Header for Discrete Representation
        html.Div(
            [ 
                html.H2("Discrete Representations")
            ]
        ), 
        html.Div(
            [
                dcc.Markdown(
                    ''' 
                    * Convert features from numerical into categorical to identify populous intervals.
                    
                    ''')
            ]
        ),

# Insert Header for Kills and Kill-Death Ratio
        html.Div(
            [
                html.H3("Kills and Kill-Death Ratio")
            ], className = 'row'
        ),
        

# Insert Markdown for Kills and Kill-Death Ratio     
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the range of 0 - 9 kills, which is 9.1% of the data.
                            
                            ''', className = "six columns"
                        )
                    ],
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in intervals of 0.60 - 0.79, 0.80 - 0.99, and 1.00 - 1.19 (KDR). 
                            * For reference, a KDR of 1.0 implies that for every death you incur, you accomplish one kill.
                            
                            ''', className = "six columns" 
                        )
                    ],
                ), 
            ], className = 'row'
        ),
        
# Insert Kills and Kill-Death Ratio Distributions
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image5.decode()), className = "six columns")
                    ],
                ), 
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image6.decode()), className = "six columns")
                    ],
                ), 
            ], className = 'row'
        ),

# Insert Header for Headshots and Headshot-Kill Ratio
        html.Div(
            [
                html.H3("Headshots and Headshot-Kill Ratio" )
            ]
        ),
        
# Insert Markdown for Headshots and Headshot-Kill Ratio     
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the range of 0 - 9 headshots, which is 34.6% of the data.
                            
                            ''', className = "six columns"
                        )
                    ],
                ), 
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the intervals of 0.150 - 0.199 and 0.200 - 0.249 (HKR). 
                            * For reference, a HKR of 1.0 implies that for every kill you incur, you accomplish one headshot.

                            ''', className = "six columns" 
                        )
                    ],
                ), 
            ], className = 'row'
        ),

# Insert Headshots and Headshot-Kill Ratio Distributions
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image7.decode()), className = "six columns")
                    ],
                ), 
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image8.decode()), className = "six columns")
                    ],
                ), 
            ], className = 'row'
        ),

# Insert Header for Wins and Win Ratio
        html.Div(
            [
                html.H3("Wins and Win Ratio" )
            ]
        ),

# Insert Markdown for Wins and Win Ratio    
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the range of 0 - 9 wins, which is 25.9% of the data.
                            
                            ''', className = "six columns" )
                    ],
                ), 
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the interval of 1.00  - 1.99 (%).
                            * For reference, a 1.0% win ratio is analogous to every 100 games one win is achieved.
                
                            ''', className = "six columns" 
                        )
                    ],
                ), 
            ], className = 'row'
        ),

# Insert Wins and Win Ratio Distributions
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image9.decode()), className = "six columns")
                    ],
                ), 
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image10.decode()), className = "six columns")
                    ],
                ), 
            ], className = 'row'
        ), 

# Insert Header for Top 10s and Top 10 Ratio
        html.Div(
            [
                html.H3("Top 10s and Top 10 Ratio" )
            ]
        ),
        
# Insert Markdown for Top 10s and Top 10 Ratio    
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players have not achieved a top 10 finish, which is 6.9% of the data.

                            ''', className = "six columns" 
                        )
                    ],
                ), 
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in intervals of 9.00 - 9.99 (%). 
                            * For reference, a 1% top 10 ratio implies that you earn nine top 10 finishes out of 100 rounds played.

                            ''', className = "six columns" 
                        )
                    ],
                ), 
            ], className = 'row'
        ),
# Insert Top 10s and Top 10 Ratio Distributions
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image11.decode()), className = "six columns")
                    ],
                ), 
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image12.decode()), className = "six columns")
                    ],
                ), 
            ], className = 'row'
        ), 

# Insert Header for Total Distance and Average Distance Per Game
        html.Div(
            [
                html.H3("Total Distance and Average Distance per game" )
            ]
        ),
        
# Insert Markdown for Total Distance and Average Distance Per Game      
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the range of 0 - 19999 miles, which is 12.1% of the data.
                            * The average man will travel 110,000 miles in his lifetime, which is 6x the reported amount from the majority of players.
                
                ''', className = "six columns" 
                        )
                    ],
                ), 
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most data is represented in the center  (1800 - 3000 miles).
                            * The average man will travel 1,000 miles (driving) + 3.7 miles (walking). 
                
                ''', className = "six columns" 
                        )
                    ],
                ), 
            ], className = 'row'
        ),
        
# Insert Total Distance and Average Distance Per Game Distributions
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image13.decode()), className = "six columns")
                    ],
                ), 
        html.Div(
            [
                html.Img(src = 'data:image/png;base64,{}'
                         .format(encoded_image14.decode()), className = "six columns")
            ],
        ), 
            ], className = 'row'
        ), 
        
# Insert Header for Time Survived and Average Time Survived per game
html.Div(
    [
        html.H3("Time Survived and Average Time Survived per game" )
    ]
        ),
        

# Insert Markdown for Time Survived and Average Time Survived per game      
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the range of 0 - 9999 seconds, which is 15.7% of the data.
                            * The average man will live 22,075,000 seconds in his lifetime, which is roughly 22,700x the reported amount from the majority of players.        
                            
                            ''', className = "six columns" 
                        )
                    ],
                ), 
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most data is represented in the center (900 - 999 seconds).
                            
                            ''', className = "six columns" )
                    ],
                ), 
            ], className = 'row'
        ),

# Insert Time Survived and Average Time Survived per Game
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image15.decode()), className = "six columns")
                    ],
                ), 
        html.Div(
            [
                html.Img(src = 'data:image/png;base64,{}'
                         .format(encoded_image16.decode()), className = "six columns")
            ],
        ), 
            ], className = 'row'
        ), 

# Insert Header for Rounds Played and Damage per game
        html.Div(
            [
                html.H3("Rounds Played and Damage per game" )
            ]
        ),

        
# Insert Markdown for Rounds Played and Damage per game   
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most players are in the range of 0 - 9 rounds, which is 17.1% of the data.
                            
                            ''', className = "six columns" 
                        )
                    ],
                ), 
                html.Div(
                    [
                        dcc.Markdown(
                            ''' 
                            * Most data is represented in the center (130 - 139 DMG Per Round), which is 6.0%.
                            
                            ''', className = "six columns" 
                        )
                    ],
                ), 
            ], className = 'row'
        ),
# Insert Rounds Played and Damage per game
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image17.decode()), className = "six columns")
                    ],
                ), 
                html.Div(
                    [
                        html.Img(src = 'data:image/png;base64,{}'
                                 .format(encoded_image18.decode()), className = "six columns")
                    ],
                ), 
            ], className = 'row'
        ),          
    ]
)






   
        

    

if __name__ == '__main__':
    app.run_server(debug = True)
