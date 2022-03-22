"""
© University of Southampton, IT Innovation Centre, 2021

Copyright in this software belongs to University of Southampton
University Road, Southampton, SO17 1BJ, UK.

This software may not be used, sold, licensed, transferred, copied
or reproduced in whole or in part in any manner or form or in or
on any media by any person other than in accordance with the terms
of the Licence Agreement supplied with the software, or otherwise
without the prior written consent of the copyright owners.

This software is distributed WITHOUT ANY WARRANTY, without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE, except where stated in the Licence Agreement supplied with
the software.

Created Date :          09-11-2021

Created for Project :   COTADS

Author: Chris Duckworth 

Email: C.J.Duckworth@soton.ac.uk

----------------------------------------------------------------------
"""

# standard libs
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pickle

# under-the-hood bokeh
from bokeh.palettes import Blues, Pastel1, Reds
from bokeh.transform import cumsum
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import show, figure, output_notebook, output_file, save
from bokeh.models import (CustomJS, Slider, Column, Row, Dropdown, 
                          Select, Range1d, ColumnDataSource, LabelSet, RadioButtonGroup, Div)
from bokeh.layouts import column, row

# interactive in notebooks
from bokeh.resources import INLINE
import bokeh.io
bokeh.io.output_notebook(INLINE)



def hello():
    '''
    Basic function to demonstrate 
    running code with output
    '''
    print('**************************************')
    print('*                                    *')
    print('* Hello and welcome to the notebook! *')
    print('*                                    *')
    print('**************************************')


def risk_score(weights = [1, 1, 1]):
    '''
    Creates and displays interactive widget 
    characterising how HbA1c, CGM usage and 
    number of finger pricks tests per day
    change risk.
    
    Parameters
    ----------
    
    weights : list len(3)
        Optional parameter which scales importance of:
        [CGM usage, BG finger prick tests, HbA1c] in 
        that order.
    
    Returns
    -------
    
    Displayed bokeh widget.
    
    '''
    
    # initial data to update
    data = ColumnDataSource({'x':[0.45, 0.45], 'y':[-0.7, 0.7]})
    p = figure(plot_height = 225, plot_width = 500,  title = "Risk score", x_range = (0, 1.0))
    
    # background risk scale
    colors = Reds[5]
    p.rect(x=[0.165], y=[0], width = 0.335, height = 1.3, angle = 0, fill_color=colors[-1], line_color=colors[-1])
    p.rect(x=[0.5], y=[0], width = 0.335, height = 1.3, angle = 0, fill_color=colors[-2], line_color=colors[-2])
    p.rect(x=[0.835], y=[0], width = 0.335, height = 1.3, angle = 0, fill_color=colors[-4], line_color=colors[-4])
    
    # plotting line over top of background
    line = p.line(x='x', y='y', source=data, line_width=10, color='black', alpha = 0.8)
    
    # risk scale formatting
    p.yaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_label_text_font_size = '0pt'  
    p.ygrid.grid_line_color = None
    p.title.text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = '16pt'
    p.xaxis.ticker = [0, 0.5, 1]
    p.xaxis.major_label_overrides = dict(zip([0, 0.5, 1], ['Lower risk', 'Medium risk', 'Higher risk']))
    p.min_border_left = 50
    p.min_border_right = 50
    p.min_border_top = 70
    p.min_border_bottom = 85
    p.toolbar.logo = None
    p.toolbar_location = None
    
    # interactive elements of plot
    control_slider = Slider(width = 250, height = 50, start = 5, end = 15, value = 5, step = 0.01, title="HbA1c")
    bg_slider = Slider(width = 250, height = 50, start = 0, end = 10, value = 5, step = 1, title="Number of Blood Glucose Tests per day")
    select = Select(width = 100, height = 75, title="Do you use CGM?", value="No", options=["No", "Sometimes", "Yes"])
    
    # Custom JS to define update.
    update = CustomJS(args=dict(line = line, control_slider = control_slider, bg_slider = bg_slider, sel = select, 
                                control_weight = weights[2], bg_weight = weights[1], cgm_weight = weights[0]), code="""

        // Grabbing current value of slider
        var f = (control_slider.value - 5) / 10;

        // Grabbing current value of BG slider
        var g = (bg_slider.value) * 0.03;

        // Grabbing value of dropdown menu
        var device = sel.value; 
        var device_coef = 0.2;

        if (device === "Sometimes") {
            device_coef = 0.1
            
        } else if (device === "Yes") {
            device_coef = 0

        } else {
            device_coef = 0.2
        }
        
        var output_risk = 0.2 + (f * 0.6 * control_weight) + device_coef * cgm_weight - g * bg_weight
        
        if (output_risk > 1) {
            output_risk = 1
        }
        if (output_risk < 0) {
            output_risk = 0
        }
        
        line.data_source.data['x'][0] = output_risk
        line.data_source.data['x'][1] = output_risk
        line.data_source.change.emit()
    """)
    
    # propagating to elements
    control_slider.js_on_change('value', update)
    bg_slider.js_on_change('value', update) 
    select.js_on_change('value', update)

    # returning plot
    text = Div(text="""<h1>Features</h1> """,
width=350, height=50)
    show(Row(Column(text, control_slider, bg_slider, select), p))
    return



def diabetes_data():
    '''
    Creates and displays formatted example 
    tabledata for type-1 diabetes.    
    
    '''
    # creating dictionary to feed to df
    people = {'Patient ID':
                  ['1', '2', '3', '4', '5'], 
          'Blood Glucose Control (HbA1c)':
                  [5, 13, 12, 7, 9],
          'Do you use CGM?'  :
                  ['Yes', 'No', 'Yes', 'Yes', 'No'],
          'Other Health Conditions':
                  [True, False, True, True, False],
          'Body Mass Index':
                  [18, 20, 28, 17, 25],
          'Finger prick tests per day':
                  [2, 9, 3, 7, 5]}
    
    # setting formatting.
    cm = sns.light_palette("salmon", as_cmap=True)
    df = pd.DataFrame(people)
    df = df.style.set_properties(**{'font-size': '12pt',}).set_table_styles([{'selector': 'th', 'props': [('font-size', '12pt')]}])
    return df.background_gradient(cmap=cm)



def request_input(text):
    '''
    Required function for querying input 
    (used in importance_input()). Ensures
    any entry is numeric and in-range.

    ----------
    Parameters
    
    text : float (ideally)
        User input of entering value 1-10
    
    -------
    Returns
    
    rate : float
        Once input has passed checks returns 
        float 1-10
    '''
    while True:
        rate = input(text)
        try:
            rate = float(rate)
        except ValueError:
            print("Please enter a number!")
        else:
            if 1 <= rate <= 10:
                break
            else:
                print("Please enter a number 1-10!")
    return rate



def importance_input():
    '''
    Function which queries user about their 
    percieved importance of CGM usage, 
    blood glucose finger prick tests, 
    HbA1c level. These new weights can then be used 
    as input to the risk_score widget.

    ----------
    Parameters
    
    -------
    Returns
    
    weights : np.array(3,) 
        Array of normalised weights for percieved
        feature importance: [CGM use, BG tests, HbA1c].
        
    '''
    
    print('How important would you rate the following for managing diabetes?')
    CGMuse = request_input("\nUsage of CGM devices (1-10) :")
    BGtests = request_input("\nNumber of finger prick tests a day (1-10) :")
    HbA1c = request_input("\nHbA1c test result (1-10) :")
    
    return np.array([CGMuse, BGtests, HbA1c]) / (CGMuse + BGtests + HbA1c)


def update_feature_plot():
    '''
    Function which queries weights 
    and then creates new version of 
    the feature importance graph. Also 
    returns weights to pass to risk widget.
    
    ----------
    Parameters
    
    -------
    Returns
    
    weights : list(3,)
        scaled weights to pass to 
        risk_score widget
    '''
    # querying weights with input. 
    weights = importance_input()
    
    # Loading in original model importances.
    importances = np.load('./data/feature_importances.npy')
    labels = np.load('./data/feature_labels.npy')
    
    # normalising weights to sum in original.
    normed_weights = weights * (importances[-1] + importances[-3] + importances[-4])
    
    # Updating cgmuse, bg tests and hba1c.
    # this should be tidied up.
    importances[-1] = normed_weights[0]
    importances[-3] = normed_weights[1]
    importances[-4] = normed_weights[2]
            
    # initialising plot
    plt.xkcd()
    fig, ax = plt.subplots(figsize = (8, 7))
    barlist = ax.barh(labels, 
                        100 * importances,
                        color = 'grey')
    #ax.set_title('What things put you more at risk?', fontsize = 20, pad = 10)

    barlist[-1].set_color('salmon')
    barlist[-3].set_color('salmon')
    barlist[-4].set_color('salmon')

    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
    ax.set_xlim([0, 30])
    plt.show()
    
    # multiplying by 3 to pass to slider 
    return 3 * weights 



def choice_cgm_days():
    '''
    Creates and displays interactive widget 
    characterising blood glucose control 
    over 3 separate days.
    
    Parameters
    ----------
    
    Returns
    -------
    
    Displayed bokeh widget.
    
    '''
    #### TO DO : need to save x_dt seperately or transform df.x to x_dt datetime.datetime format
    
    # loading in example cgm data.
    df = pd.read_csv('./data/summary_cgm_days_mmol.csv')
    
    # had to pickle time-formating due to 
    # conversion and incompatibility issues between 
    # bokeh datetime and pd.datetime
    with open("./data/time_series", "rb") as fp:   # Unpickling
        x_dt = pickle.load(fp)  
    df['x'] = x_dt
    
    # defining figure with range.
    p = figure(x_range = Range1d(x_dt[0], x_dt[-1]),
               y_range = Range1d(0, 410 / 18),
               x_axis_type='datetime',
               title = 'Blood Glucose through the day',
               x_axis_label = 'Time of day',
               y_axis_label = 'Blood Glucose Level (mmol/L)',
               plot_width = 500, plot_height = 300)

    source = ColumnDataSource(df)
    
    p.varea(x = [x_dt[0], x_dt[-1]],
            y1 = [70 / 18, 70/ 18],
            y2 = [270/ 18, 270/ 18], 
            color = "grey", 
            alpha = 0.2)

    p.line(x = [x_dt[0], x_dt[-1]],
           y = [70 / 18, 70 / 18],
           color = "grey",
           line_width = 5,
           line_dash = 'dashed',
           alpha = 1)

    p.line(x = [x_dt[0], x_dt[-1]],
           y = [270 / 18, 270 / 18],
           color = "grey",
           line_width = 5,
           line_dash = 'dashed',
           alpha = 1)

    # defining 3 individual lines to turn off/on
    plot_1 = p.line(x = "x", y = "y1", color = "darkseagreen", source = source, line_width = 5)
    plot_2 = p.line(x = "x", y = "y2", color = "firebrick", source = source, line_width = 5)
    plot_3 = p.line(x = "x", y = "y3", color = "dodgerblue", source = source, line_width = 5)

    # initialise the plot with only y1 visible - to match the dropdown default
    plot_2.visible = False
    plot_3.visible = False
    
    # select interaction
#     select = Select(title="Select day", 
#                     value = "Day 1", 
#                     options = ["Day 1", "Day 2", "Day 3"], 
#                     width = 120)
    
    radio_button_group = RadioButtonGroup(labels=["Day 1", "Day 2", "Day 3"], active=0)
    radio_button_group.js_on_click(CustomJS(args=dict(line_1 = plot_1, line_2 = plot_2, line_3 = plot_3), 
                                          code="""
                                                line_1.visible = true
                                                line_2.visible = true
                                                line_3.visible = true

                                                if (this.active == 0) {
                                                    line_2.visible = false 
                                                    line_3.visible = false
                                                } else if (this.active == 1) {
                                                    line_1.visible = false
                                                    line_3.visible = false
                                                } else {
                                                    line_1.visible = false
                                                    line_2.visible = false
                                                }
                                                    """))
    
    # customjs interaction
#     select.js_on_change("value", CustomJS(args=dict(line_1 = plot_1, line_2 = plot_2, line_3 = plot_3), 
#                                           code="""
#                                                 line_1.visible = true
#                                                 line_2.visible = true
#                                                 line_3.visible = true

#                                                 if (this.value === "Day 1") {
#                                                     line_2.visible = false 
#                                                     line_3.visible = false
#                                                 } else if (this.value === "Day 2") {
#                                                     line_1.visible = false
#                                                     line_3.visible = false
#                                                 } else {
#                                                     line_1.visible = false
#                                                     line_2.visible = false
#                                                 }
#                                                     """))

    p.xaxis[0].ticker.desired_num_ticks = 12
    p.xaxis.formatter = DatetimeTickFormatter(days = ['%H:%M'], 
                                              hours = ['%H:%M'])
    p.toolbar.logo = None
    p.toolbar_location = None
    
    #layout = row(select, p)
    layout = column(radio_button_group, p)
    return show(layout)



def make_own_plot(labels, how_important, color = 'darkseagreen'):
    '''
    Small function to enable users to 
    build their own barchart, specifically 
    define their own features and importances.
    
    ----------
    Parameters
    
    labels : list(str)
        contains barchart column labels
        
    how_important : list(float)
        contains size of bars. must match
        labels size.
        
    color : str
        Can define color of bars if needed.
        
    -------
    Returns
    
    matplotlib.pyplot figure
    
    '''
    plt.xkcd()
    fig, ax = plt.subplots(figsize = (8, 7))
    ax.barh(labels[::-1], 
            how_important[::-1],
            color = color)
    plt.show()
    return