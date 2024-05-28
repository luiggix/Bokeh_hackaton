import numpy as np
import pandas as pd 

from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, Button
from bokeh.models.tools import HoverTool
from bokeh.models.annotations import Span

TFR = pd.read_csv('Datos/UNdata_Export_20230621_205538168.zip')
TFR_group = TFR.groupby('Country or Area')

def plot_country(dfg, label, color, lw):
    maxim = 2021
    country = dfg.get_group(label)
    
    cc = country[country['Year(s)']>=maxim-1]
    p.line(y='Value', x='Year(s)', color=color, source = cc, line_width=lw, line_dash="dashed")

    cc = country[country['Year(s)']<maxim]
    p.line(y='Value', x='Year(s)', color=color, source = cc, line_width=lw)


title = 'Evolución del TFR (Total Fertility Rate)'
p = figure(title=title, width=800, height=600)
    
def callback():
    global TFR_gropu
    global TFR
    global p
    
    p.line(y='Value', x='Year(s)', color='silver', source = TFR, line_width=0.75)
        
    plot_country(TFR_group, 'Mexico', 'forestgreen', lw= 2.0)
    plot_country(TFR_group, 'Niger', 'darkred', lw= 2.0)
    plot_country(TFR_group, 'Japan', 'mediumblue', lw= 2.0)
    plot_country(TFR_group, 'World', 'black', lw= 2.0)
    
    upper = Span(location=2.1, dimension='width', 
                 line_color='black', line_width=1.0, line_dash="dashed")
    p.add_layout(upper)
    
    hover = HoverTool()
    hover.tooltips=[
        ('TFR Value', '@Value'),
        ('País', "@{Country or Area}"),
        ('Year', '@{Year(s)}')
    ]
    
    p.add_tools(hover)
    
    p.xaxis.major_label_orientation = 1.5*np.pi/4


# add a button widget and configure with the call back
button = Button(label="Presiona")
button.on_event('button_click', callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))