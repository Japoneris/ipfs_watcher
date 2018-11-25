from bokeh.plotting import figure, ColumnDataSource, curdoc

import subprocess
import time
# I know, it is not the best way for import
from my_utils import get_ipfs_stats_bw

VERBOSE = False
MEMORY_LENGTH = 3600 # Number of seconds you want to display
IN_color  = "mediumblue"
OUT_color = "brown"

PLOT_HEIGHT = 600
PLOT_WIDTH  = 1200


source = ColumnDataSource({'time': [], 'down': [], 'up': []})

def update(verbose=VERBOSE, max_memory=MEMORY_LENGTH):
    """
    
    :param verbose: print or not the values that you get
    :param max_memory: number of point in the plot to keep
    """
    
    dic_vals = {"RateIn": 0, "RateOut": 0}
   
    try:
        # Warning, you will not know why it failed, but you will have plot updated with zero values
        dic_vals = get_ipfs_stats_bw()
    except:
        pass
    
    if verbose:
        print(dic_vals)

    new = {'time':    [int(time.time())*1000], # For seconds
           'down': [dic_vals["RateIn"]/1000],  # For kB
           'up':   [dic_vals["RateOut"]/1000]}

    source.stream(new, max_memory)
    return 

    
doc = curdoc()
doc.add_periodic_callback(update, 1000)

# Define your figure and its attribute
fig = figure(title='Streaming IPFS Traffic', 
             height=PLOT_HEIGHT, width=PLOT_WIDTH,
             #sizing_mode='scale_height', 
             x_axis_type='datetime',
            tools="box_select,box_zoom,lasso_select,reset,hover,save")

fig.line(source=source, x='time', y='down', color=OUT_color, legend="RateIn")
fig.line(source=source, x='time', y='up', color=IN_color, legend="RateOut")

fig.legend.location = "top_left"
fig.legend.click_policy = "hide"

fig.yaxis.axis_label = "kB/sec"

doc.title = "IPFS Stats"
doc.add_root(fig)
