# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 20:44:37 2022

@author: Matthew

This module is a GUI interface for converting between different dates in the
Eberron universe's different calendar systems. Imports the Calendars.py
module, where the actual date calculations are performed.
"""

from tkinter import * # classic widgets
from tkinter import ttk # themed widgets

import Calendars as cal # Eberron calendar module

debug = True

# supported calendar options
calendars = ('Galifar',
             'Druidic',
             'Dwarven',
             'Talenta',
             'Aereni',
             'Sovereign')

# predefine function callbacks
def calculate(*args):
    try:
        if calvar_in.get() == calvar_out.get(): # no conversion required
            date_out = date_in
            datestr_out.set(date_out.disp())
            if debug: print('no conversion')
        elif calvar_in.get() in ['Galifar','Druidic','Dwarven','Talenta'] and calvar_out.get() in ['Galifar','Druidic','Dwarven','Talenta']:
            # don't need to convert date object, just month
            date_out = date_in
            datestr_out.set(date_out.disp(cal = calvar_out.get()))
            if debug: print('galifar to druidic, dwarven, or talenta')
        elif calvar_in.get()=='Galifar' and calvar_out.get()=='Aereni':
            # convert Galifar to Aereni
            date_out = cal.galifar2aereni(date_in)
            datestr_out.set(date_out.disp())
            if debug: print('galifar to aereni')
        elif calvar_in.get()=='Galifar' and calvar_out.get()=='Sovereign':
            # convert Galifar to Sovereign
            date_out = cal.galifar2sovereign(date_in)
            datestr_out.set(date_out.disp())
            if debug: print('galifar to sovereign')
        elif calvar_in.get()=='Aereni' and calvar_out.get()=='Galifar':
            # convert Aereni to Galifar
            date_out = cal.aereni2galifar(date_in)
            datestr_out.set(date_out.disp())
            if debug: print('aereni to galifar')
        elif calvar_in.get()=='Sovereign' and calvar_out.get()=='Galifar':
            # convert Sovereign to Galifar
            date_out = cal.sovereign2galifar(date_in)
            datestr_out.set(date_out.disp())
            if debug: print('sovereign to galifar')
        elif calvar_in.get()=='Aereni' and calvar_out.get()=='Sovereign':
            # convert Aereni to Galifar, then Galifar to Sovereign
            date_out = cal.galifar2sovereign(cal.aereni2galifar(date_in))
            datestr_out.set(date_out.disp())
            if debug: print('aereni to sovereign')
        elif calvar_in.get()=='Sovereign' and calvar_out.get()=='Aereni':
            # convert Sovereign to Galifar, then Galifar to Aereni
            date_out = cal.galifar2aereni(cal.sovereign2galifar(date_in))
            datestr_out.set(date_out.disp())
            if debug: print('sovereign to aereni')
        if debug:
            print('input: ', datestr_in.get())
            print('cal in: ', calvar_in.get())
            print('cal out: ', calvar_out.get())
            print('output: ', datestr_out.get())
    except ValueError:
        pass

# for debugging
def print_hierarchy(w, depth=0):
    print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth+1)

# set up containers for entire GUI        
root = Tk() # create the base Tk instance
root.title("Shardspace Date Converter") # window title
mainframe = ttk.Frame(root, padding = "12 12 12 12") # 12 pixel padding around edges
mainframe.grid(column=0, row=0, sticky='nsew') # put mainframe in 0,0 cell of root, attached to all four sides
root.columnconfigure(0, weight=1) # let col 0 (mainframe) resize horizontally
root.rowconfigure(0, weight=1) # let row 0 (mainframe) resize vertically
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# set up frame for date converter
dateframe = ttk.Frame(mainframe)
dateframe.grid(column=0, row=0, sticky='nsew')
dateframe.columnconfigure(0, weight=1)
dateframe.rowconfigure(0, weight=1)
dateframe.columnconfigure(1, weight=1)
dateframe.rowconfigure(1, weight=1)
dateframe.columnconfigure(2, weight=1)
#dateframe.rowconfigure(2, weight=1)
dateframe.columnconfigure(3, weight=1)
#dateframe.rowconfigure(3, weight=1)
dateframe.columnconfigure(4, weight=1)
dateframe.rowconfigure(4, weight=1)

# static elements
inlabel = ttk.Label(dateframe, text='Input:')
inlabel.grid(column=1, row=2, padx=5, pady=5, sticky='nsew')
outlabel = ttk.Label(dateframe, text='Output:')
outlabel.grid(column=1, row=3, padx=5, pady=5, sticky='nsew')

# calendar selection comboboxes
calvar_in = StringVar()
calvar_out = StringVar()
cal_in = ttk.Combobox(dateframe, textvariable=calvar_in)
cal_in.grid(column=3, row=2, padx=5, pady=5, sticky='nsew')
cal_out = ttk.Combobox(dateframe, textvariable=calvar_out)
cal_out.grid(column=3, row=3, padx=5, pady=5, sticky='nsew')
def function(entry):
    entry.selection_clear() # clear when value changes
cal_in.bind('<<ComboboxSelected>>', function(cal_in))
cal_in['values'] = calendars
cal_in.state(["readonly"])
cal_out.bind('<<ComboboxSelected>>', function(cal_out))
cal_out['values'] = calendars
cal_out.state(["readonly"])

# input selection frame
select = ttk.Frame(dateframe)
select.grid(column=2, row=1, padx=5, pady=5, sticky='nsew')

# datestring labels
date_in = cal.GalifarDate()
date_out = cal.GalifarDate()
datestr_in = StringVar()
datestr_out = StringVar()
datelbl_in = ttk.Label(dateframe, textvariable=datestr_in)
datelbl_out = ttk.Label(dateframe, textvariable=datestr_out)
datelbl_in.grid(column=2, row=2, padx=5, pady=5, sticky='nsew')
datelbl_out.grid(column=2, row=3, padx=5, pady=5, sticky='nsew')

# create a button to press to perform the calculation
calc = ttk.Button(dateframe, text="Calculate", command=calculate)
calc.grid(column=4, row=3, sticky='nsew')

# misc functions
def reset_to_default():
    date_in = cal.GalifarDate()
    date_out = cal.GalifarDate()
    datestr_in.set(date_in.disp())
    datestr_out.set(date_out.disp())
    calvar_in.set('Galifar')
    calvar_out.set('Galifar')

# debug
if debug: print_hierarchy(root)

# start the GUI
reset_to_default()
root.mainloop()