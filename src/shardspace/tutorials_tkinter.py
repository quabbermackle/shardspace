# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 21:14:43 2022

@author: Matthew
"""

from tkinter import * # classic widgets
from tkinter import ttk # themed widgets

#tutorial 4
def print_hierarchy(w, depth=0):
    print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth+1)

'''
root = Tk()
root.title("Feet to Meters")
mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

print_hierarchy(root)
'''

# tutorial 0
#root = Tk()
#ttk.Button(root, text="Hello World").grid()
#print_hierarchy(root)
#root.mainloop()

# tutorial 1
'''
# define called functions first
def calculate(*args):
    try:
        value = float(feet.get()) # get the value of the global variable
        # multiply and divide by 10000 to avoid floating point rounding errors
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0) # set the global variable's value
    except ValueError:
        pass
    
# set up the main application window
root = Tk() # everything else will be a child of this object
root.title("Feet to Meters") # title is displayed in top windows menu bar

# create a frame widget to hold the contents of the user interface
mainframe = ttk.Frame(root, padding = "3 3 12 12") # themed widget, child of root
# grid places widget inside main application window
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# tell frame to expand to fill extra space if window is resized
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# create entry to input number of feet to convert
feet = StringVar() # global variable, must be an instance of the StringVar class
# need to specify the parent when creating a widget (first parameter)
# further entries are "configuration options"
# width=7 specifies that the widget is 7 characters wide
# binding the global "feet" variable as the textvariable means that Tk will
#   automatically update the global variable when the feet_entry object changes
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet) # child of content frame
# grid places the widget into the content frame
# the sticky option tells which sides of the cell to anchor content to
feet_entry.grid(column=2, row=1, sticky=(W, E))

# label to display resulting number of meters that is calculated
# each widget is created as the appropriate object type with the mainframe as
#   the parent, then placed in the content frame with grid, specifying the location
meters = StringVar() # global variable, must be an instance of the StringVar class
# setting the textvariable to the global variable "meters" means the calculate
#   function only has to change the global variable's value, and Tk will
#   automaticaly update the widget displayed in the GUI
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

# create a button to press to perform the calculation
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# static text labels to make it clear how to use the application
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# add a little bit of padding around each widget to keep them from being scrunched
# could have added these as options to each call of grid(), but this is more concise
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
    
feet_entry.focus() # put focus on the entry box so the cursor starts in that field
root.bind("<Return>", calculate) # call the calculate routine when user presses Enter

print_hierarchy(root)

# enter the main Tk event loop
# necessary for everything to be displayed onscreen and for user interaction
root.mainloop()
'''

# tutorial 2 (same as 1 but in a class wrapper)
'''
class FeetToMeters:
    
    def __init__(self, root):
        
        root.title("Feet to Meters")
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        self.feet = StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        
        self.meters = StringVar()
        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)
        
        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
        
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)
        
    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass
        
root = Tk()
FeetToMeters(root)
print_hierarchy(root)
root.mainloop()
'''

#tutorial 3
'''
root = Tk()
button = ttk.Button(root, text="Hello", command="buttonpressed")
button.grid()
button['text'] # returns current value of text option
button['text'] = 'goodbye' # change the value of the text option
button.configure(text='goodbye') # another way to change the value
button.configure('text') # get all info about text option
# normally returns list of 5, ie ('text', 'text', 'Text', '', 'goodbye')
# first item is the option's name
# second is the option's name in the database
# third is the option's class
# fourth is the option's default value
# fifth is the option's current value
button.configure() # get information on all options for this widget
print_hierarchy(root)
'''

#tutorial 5
'''
root = Tk()
l = ttk.Label(root, text="Starting...")
l.grid()
# for simplicity, these are anonymous functions that take as an argument
#   an "event object" that captures lots of info about an event. Additional
#   details (like the location of the mouse) can be extracted from the event
#   object with percent substitutions
l.bind('<Enter>', lambda e: l.configure(text='Moved mouse inside'))
l.bind('<Leave>', lambda e: l.configure(text='Moved mouse outside'))
l.bind('<ButtonPress-1>', lambda e: l.configure(text='Clicked left mouse button'))
l.bind('<3>', lambda e: l.configure(text='Clicked right mouse button')) # shorthand for <ButtonPress-3>
l.bind('<Double-1>', lambda e: l.configure(text='Double clicked')) # shorthand for <Double-ButtonPress-1>
l.bind('<B3-Motion>', lambda e: l.configure(text='right button drag to %d,%d' % (e.x, e.y)))
print_hierarchy(root)
root.mainloop()
'''

# tutorial 6 - widget roundup
'''
root = Tk()

# use ttk.Frame objects as containers
frame = ttk.Frame(root, width=350, height=350) # displays as a simple rectangle
# 350 = pixels
# 350c = centimeters
# 350m = millimeters
# 350i = inches
# 350p = printer's points (1/72 inch)
frame['padding'] = 5 # 5 pixels on all sides
frame['padding'] = (5, 10) # 5 on left/right, 10 on top/bottom
frame['padding'] = (5,7,10,12) # left: 5, top: 7, right: 10, bottom: 12
frame['borderwidth'] = 2 # defaults to 0 (no border)
frame['relief'] = 'sunken' # default is "flat"

# use ttk.Style objects to define custom styles and apply to widgets
s = ttk.Style()
s.configure('Danger.TFrame', background='red', borderwidth=5, relief='raised')
ttk.Frame(root, width=200, height=200, style='Danger.TFrame').grid()

# use ttk.Label objects to identify controls and provide info to the user
label = ttk.Label(root, text='Full name:')
# an object attached to a widget must be a subclass of type Variable(), of
#   which there are StringVar(), IntVar(), DoubleVar(), and BooleanVar() predefined
# use the get() and set() methods of a Variable() object to read or write the
#   current value of the object
resultsContents = StringVar()
label['textvariable'] = resultsContents
resultsContents.set('New value to display')

# labels can also display images instead of text. Two-step process:
#   - create an image "object"
#   - tell the label to use that object via its "image" config option
#image = PhotoImage(file='myimage.gif')
#label['image'] = image
# labels can display both an image and text at the same time
# to do so, use the 'compound' config option (default is 'none')
#label['compound'] = 'top' # image above text, can also be 'left', 'bottom', or 'right'

# to change fonts & colors, it is recommended to create a custom style object
label['font'] = "TkDefaultFont"
label['foreground'] = 'blue' # text color
label['background'] = '#ff340a' # background color
label['relief'] = 'sunken'
label['anchor'] = 'center' # n, ne, e, se, s, sw, w, nw, or center
resultsContents.set('New value to \ndisplay')
# use the 'wraplength' option to wrap text to a max line length (pixels etc)
label['justify'] = 'right' # left, center, or right

# create ttk.Button() objects for users to interact with by clicking
# buttons take a callback function, 'command', which must be predefined
def myaction():
    pass

button = ttk.Button(root, text='Okay', command=myaction)
# buttons also have options text, textvariable, image, and compound
# buttons have a 'default' config option:
#   if 'default' = 'active', button is invoked when Return/Enter is pressed
#   otherwise, 'default' = 'normal'
# note that you still need to create an event binding to make Return/Enter activate the button
root.bind('<Return>', lambda e: button.invoke()) # call the button's command with the invoke() method
close = ttk.Button(root, text='Close', command=myaction)
root.bind('<Key-Escape>', lambda e: close.invoke())
button.state(['disabled'])          # set the disabled flag
button.state(['!disabled'])         # clear the disabled flag
button.instate(['disabled'])        # true if disabled, else false
button.instate(['!disabled'])       # true if not disabled, else false
button.instate(['!disabled'], myaction)  # execute 'cmd' if not disabled
# full list of state flags in themed widgets:
#    active, disabled, focus, pressed, selected, background, readonly, alternate, and invalid

# use checkbuttons, ttk.Checkbutton() for a button with a binary value
# when clicked, the toggle is flipped and the callback invoked
# good for turning options on or off
checklabel = ttk.Label(root, text='Units')
activeSystem = StringVar()
checklabel['textvariable'] = activeSystem
def metricChanged():
    activeSystem.set(measureSystem.get())
measureSystem = StringVar()
check = ttk.Checkbutton(root, text='Use Metric',
                        command=metricChanged, variable=measureSystem,
                        onvalue='metric', offvalue='imperial')
# by default, onvalue=1 and offvalue=0, unless overridden like above
check.instate(['alternate']) # set to indeterminate tristate value

# various subclasses of Varable():
s = StringVar(value="abc")   # default value is ''
b = BooleanVar(value=True)   # default is False
i = IntVar(value=10)         # default is 0
d = DoubleVar(value=10.5)    # default is 0.0

# radiobutton widgets let you choose between mutually exclusive choices
# similar to checkbutton but with more than two options
# always used as a set, with multiple radiobutton widgets tied to one choice
# create an instance of the ttk.Radiobutton() class, typically several at once
phone = StringVar()
home = ttk.Radiobutton(root, text='Home', variable=phone, value='home')
office = ttk.Radiobutton(root, text='Office', variable=phone, value='office')
cell = ttk.Radiobutton(root, text='Mobile', variable=phone, value='cell')

# entry widgets present a single-line text field that takes a string value
# create an instance of the ttk.Entry() class with a StringVar textvariable
username = StringVar()
name = ttk.Entry(root, textvariable=username)
name['width'] = 20 # number of characters wide
print('current value is %s' % name.get())
name.delete(0,'end') # delete between two indices, 0-based
name.insert(0, 'your name') # insert new text at a given index
# entry widgets don't have a callback
# to watch for changes, watch for changes in the linked variable
def it_has_been_written(*args):
    ...
username.trace_add("write", it_has_been_written)
# entries for passwords can display the contents as a bullet or other symbol
# set the 'show' config option to the desired display character
password = StringVar()
passwd = ttk.Entry(root, textvariable=password, show="*")
# entries can also be disabled via the 'state' configs
# they can also use the 'state' flag 'readonly':
#   if set, users cannot change the entry, but can select the text and copy it to the clipboard
# there is also an 'invalid' state, set if the entry widget fails validation

# Validation
# specify what makes an entry valid or invalid with the validatecommand option
# supply a callback that returns T/F whether entry is valid
import re # import regular expressions
def check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <=5 # if False, value will not be changed
check_num_wrapper = (root.register(check_num), '%P') # use percent substitution to pass the entry value to the callback

num = StringVar()
e = ttk.Entry(root, textvariable=num, validate='key', validatecommand=check_num_wrapper) # validation checked on keystrokes
e.grid(column=0, row=0, sticky='we')

# the above is prevalidation - checking changes on each keystroke
# can also revalidate - only check changes when entry loses focus
# add a message to explain format to call on error
# can key a "process" button to be disabled unless revalidation passes
errmsg = StringVar()
formatmsg = "Zip should be ##### or #####-####"

def check_zip(newval, op):
    errmsg.set('')
    valid = re.match('^[0-9]{5}(\-[0-9]{4})?$', newval) is not None
    btn.state(['!disabled'] if valid else ['disabled'])
    if op=='key': # if triggered by keystroke
        ok_so_far = re.match('^[0-9\-]*$', newval) is not None and len(newval) <= 10
        if not ok_so_far:
            errmsg.set(formatmsg)
        return ok_so_far
    elif op=='focusout': # if triggered by leaving focus (there is also 'focusin' for entering focus)
        if not valid:
            errmsg.set(formatmsg)
    return valid
check_zip_wrapper = (root.register(check_zip), '%P', '%V') # trigger is passed to callback with the %V substitution

zip = StringVar()
f = ttk.Frame(root)
f.grid(column=0, row=0)
ttk.Label(f, text='Name:').grid(column=0, row=0, padx=5, pady=5)
ttk.Entry(f).grid(column=1, row=0, padx=5, pady=5)
ttk.Label(f, text='Zip:').grid(column=0, row=1, padx=5, pady=5)
e = ttk.Entry(f, textvariable=zip, validate='all', validatecommand=check_zip_wrapper) # validation on all triggers, not just keystrokes
e.grid(column=1, row=1, padx=5, pady=5)
btn = ttk.Button(f, text='Process')
btn.grid(column=2, row=1, padx=5, pady=5)
btn.state(['disabled'])
msg = ttk.Label(f, font='TkSmallCaptionFont', foreground='red', textvariable=errmsg)
msg.grid(column=1, row=2, padx=5, pady=5, sticky='w')
# if validatecommand callback causes an error, validation is disabled for that widget
# can force widget to validate by calling its .validate method
# there is also an 'invalidcommand' option to specify a callback for when validation fails
# can also check an entry's 'invalid' state flag to check validation status
# other precent substitutions:
#   %s - get entry's contents prior to editing
#   %d - differentiate between insert and delete
#   %i - where an insert or delete occurs
#   %s - what is being inserted or deleted
#   %v - current setting of the 'validate' option
#   %w - name of the widget

# Combobox widget combines entry with a list of choices
# can choose from set of values or put in custom value
countryvar = StringVar()
country = ttk.Combobox(root, textvariable=countryvar)
# combobox generates <<ComboboxSelected>> virtual event for when its value changes
# can also check changes on textvariable, but the event is more straightforward
def function(entry):
    entry.selection_clear() # clear when value changes if in readonly mode
country.bind('<<ComboboxSelected>>', function(country))
country['values'] = ('USA', 'Canada', 'Australia') # list of values
country.state(["readonly"]) # restricts users to predefined values
print(country.get())
country.set('USA')
print(country.get())
print(country.current()) # returns 0-based index with no arguments. returns specific value if given index

for child in root.winfo_children(): 
            child.grid() # draw all children

print_hierarchy(root)
root.mainloop()
'''

# tutorial 7 - grid geometry manager
# grid is the best choice for general use - columns & rows
# pack is also powerful but harder to use
# place gives complete control of positioning each element

root = Tk()
# in grid, widgets are assigned a 'column' number and a 'row' number
# positive integers, don't have to start at 0 and can leave gaps to add more later
# width & height vary depending on dimensions of widgets
# widgets can take up multiple cells with 'columnspan' and 'rowspan'
# LAYOUT
#   by default, a widget is centered horizontally and vertically in a cell
#   the empty space around a widget displays the color of the widget's parent
#   the 'sticky' option sticks the widget, including its background, to the edge
#       specify with a string 'nsew' or a list (N, S, E W)
#       most widgets, like label, have an 'anchor' option for where the text is attached (also 'nsew')
#   if having difficulty with a widget's size, change its background color to see more easily
# RESIZING
#   widget's don't resize unless you tell them to
#   each col and row has a 'weight' option, default = 0 (don't expand to fill extra space)
#   specify a positive weight for at least one column and one row
#   use the 'columnconfigure' and 'rowconfigure' methods of grid
#   weight is relative - two columns with same weight expand at same rate
#   both colconfigure and rowconfigure take a 'minsize' option, widget won't shrink smaller
# PADDING
#   by default, each col & row are directly adjacent, so widgets are right next to each other
#   adding space in between widgets is called padding, which can be done several ways
#   a widget's own options can add extra space, such as the frame widget
#       this is a good reason to make a frame the parent of all other widgets
#       frame's 'padding' option specifies extra space inside frame
#       can be same or different for each of the four sides
#   can also use 'padx' and 'pady' grid options when adding the widget
#       padx is top & bottom, pady is left & right
#       a single value puts the same on both, a two-value list lets you put different amounts on each
#   can also add padding around entire row or column
#       use the 'pad' option with columnconfigure and rowconfigure methods
#   less used is "internal padding" via grid options 'ipadx' and 'ipady'
#       ex: 20x20 frame, (external) padding 5:
#               requests 20x20 rectangle from grid
#               granted 20x20 rectangle surrounded by 5-pixel border
#           20x20 frame, (internal) padding 5:
#               widget effectively requests 30x30 rectangle
#               if frame centered or attached to a single side or corner:
#                   20x20 frame with extra space around it
#               if frame set to stretch (sticky we, ns, or nsew):
#                   fills extra space, results in 30x30 with no border
# QUERYING AND CHANGING
#   using the .grid_slaves() method on a widget object returns all the widgets gridded inside it
#       can also specify a row or column
#       ie widget.grid_slaves(row=3)
#   using the .grid_info() method on a widget object returns a list of all grid options & their values
#   use the .grid_configure() method to change a grid option on a widget
#       ie widget.grid_configure(sticky=(E,W))
# FORGET AND REMOVE
#   calling the .forget() method of grid removes children from grid
#       input list of one or more children, takes them off the screen
#       can grid them again later, but any grid options must be set again
#   the .remove() method of grid is the same but REMEMBERS grid options
# NESTED LAYOUTS
#   nice to keep independent areas of interface contained in separate frames
#   easy to place these frames in a mainframe, rearrange, and reuse
#   can import a frame from one module into another and simply add to mainframe
content = ttk.Frame(root, padding=(3,3,12,12))
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=200)
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

onevar = BooleanVar(value=True)
twovar = BooleanVar(value=False)
threevar = BooleanVar(value=True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky='nsew')
namelbl.grid(column=3, row=0, columnspan=2, sticky='nw', padx=5)
name.grid(column=3, row=1, columnspan=2, sticky='nwe', pady=5, padx=5)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

print_hierarchy(root)
root.mainloop()