#!/usr/bin/python

# This program is used to chart temperature profiles in real time.
# In addition, it can save such profiles in CSV (comma separated value)
# format and read these profiles back in at a later date.  A standard
# profile can be read in to allow the manual control of a toaster
# oven or hot plate to be used.
#
# The thermocouple input device is from PCSensors.Com called the
# TEMPer1K4.  This has a USB connector on one end and a thermocouple
# on the other and currently costs about US$20 (circa 2012.)  There
# is a button on the thermocouple that causes it to emit a temperature
# reading once a second.  This temperature reading shows up as keyboard
# input, so it is extremely easy to read.

# Other Notes:
#
# Zephertronics sells solder paste and other tools
#
# Amtech NC-559 has an actual temperature profile:
#
# Profile A:
#   20-150 - 120sec
#   150-183 - 90 sec
#   183-220 - 30 sec
#   220-183 - 30 sec
#   183-150 - 30 sec
#
# Profile B:
#   20-150 - 90 sec
#   150-183 - 120 sec
#   183-220 - 30 sec
#   220-183 - 30 sec
#   183-150 - 30 sec

import getpass
from Tkinter import *       
import tkFileDialog
import sys

class Application(Frame):

    def __init__(self, master=None):
	""" This will initialize all the widgets and application
	    data structures. """

	# Get the top level frame initialized and grid enabled:
	Frame.__init__(self, master)
	self.grid(row = 0, column = 0)

	# Create a file [Open] button:
	self.open_button = open_button = \
	  Button(self, text = "Open", command = self.open)
	open_button.grid(row = 0, column = 0)

	# Create a file [Save] button:
	self.save_button = save_button = \
	  Button(self, text = "Save", command = self.save)
	save_button.grid(row = 0, column = 1)

	# Create a [Quit] button:
	self.quit_button = quit_button = \
	  Button(self, text = 'Quit', command = self.quit)
	quit_button.grid(row = 0, column = 2)

	# Initialize some values for the canvas:
	self.x_minimum = x_minimum = 0.0
	self.x_maximum = x_maximum = 400.0
	self.y_minimum = y_minimum = 15.0
	self.y_maximum = y_maximum = 260.0
	self.canvas_width = canvas_width = 800.0
	self.canvas_height = canvas_height = 500.0
	self.x_scale = canvas_width / (x_maximum - x_minimum)
	self.y_scale = canvas_height / (y_maximum - y_minimum)

	# Create the canvas to draw all the data on:
	self.canvas = canvas = Canvas(self,
	  height = canvas_height, width = canvas_width, background = "white")
	canvas.grid(row = 1, column = 0, columnspan = 3)

	# Draw some horizontal lines across the canvas to indicate where
	# various phase are:
	self.horizontal_line(150, "blue", "soak")
	self.horizontal_line(183, "green", "leaded reflow")
	self.horizontal_line(217, "orange", "no lead relflow")
	self.horizontal_line(245, "red", "danger")

	# The data shows up as if it is typed in on the keyboard.
	# The *input_available* method is called whenever the next
	# line of data shows up:
	self.tk.createfilehandler(sys.stdin,
	  tkinter.READABLE, self.input_available)

	# Initilize the remaining data strcutures:
	self.time = 0
	self.temperature = 0
	self.temperatures = []
	self.color_index = 0
	self.colors = ["purple", "magenta", "blue", "orange", "red", "brown",
	  "cyan", "green", "pink", "violet"]

    def color_get(self):
	""" Return the next color from the color sequence. """

	color_index = self.color_index
	colors = self.colors
	color = colors[color_index % len(colors)]
	self.color_index = color_index + 1
	return color

    def horizontal_line(self, y, color, label):
	""" Draw a horizontal line. """

	self.line_draw(0, y, self.x_maximum, y, color)

    def input_available(self, a, b):
	# Read line one character at a time until a new line is reached:

	# The data comes in as ";\t:\t{temp1}\t{temp2}\t1s\n".
	# {temp1} is the thermocouple temperature in centigrade.
	# {temp2} is probably the reference junction temperature, but
	# that could be totally wrong.  {temp1} is the temperature to use.
	# The format of {temp1} is "dd.ff", where "ff" is "00", "25", "50",
	# or "75".  The "1s" stands for 1 second intervals.

	# The usual problem with Unix is that there is system call that
        # reads until a new-line is reached.  So, we read one character
	# at a time until a new line is found:
	line = ""
	while True:
	    c = sys.stdin.read(1)
	    if c == '\n':
		break
	    line += c
	#print "line='{0}'".format(line)

	# Split the data apart using white space as the separator:
	line_arguments = line.split()
	#print "line_arguments=", line_arguments

	# Make sure we do not get an interrupted line:
	if len(line_arguments) > 2:
	    # ";\t":\t"{temp1}\t..." shows up as [";", ":", "{temp1}", ...].
	    # Grab the third value since it has the temperature we want.
	    new_temperature = float(line_arguments[2])
	    #print "temperature = {0}".format(new_temperature)

	    # Remember the temperature in *temperatures*:
	    self.temperatures.append(new_temperature)

	    # Plot from the previous end-point to the current location:
	    temperature = self.temperature
	    time = self.time
	    self.line_draw(time,
	      temperature, time + 1, new_temperature, "black")

	    # Remember where the current end-point is:
	    self.time = time + 1
	    self.temperature = new_temperature

    def line_draw(self, x1, y1, x2, y2, color):
	""" Draw a line segment of a given color. """

	#print "line_draw({0}, {1}, {2}, {3}, {4})". \
	#  format(x1, y1, x2, y2, color)

	# Grab some values from *self*:
	canvas_height = self.canvas_height
	x_minimum = self.x_minimum
	x_scale = self.x_scale
	y_minimum = self.y_minimum
	y_scale = self.y_scale

	# Draw the line segment using pixel coordinates:
	self.canvas.create_line((x1 - x_minimum) * x_scale,
	  canvas_height - (y1 - y_minimum) * y_scale,
	  (x2 - x_minimum) * x_scale,
	  canvas_height - (y2 - y_minimum) * y_scale,
	  fill = color)

    def open(self):
	""" Called when a the [Open] button is called.  Used to read in
	    a profile or a previous data run. """

        # Get a color and initialize (x,y):
	color = self.color_get()
	x = 0.0
	y = 0.0

	# Open the data file and read it in:
	in_stream = tkFileDialog.askopenfile(title = "Profile")
	lines = in_stream.readlines()
	in_stream.close()

	# Plot all the data.  Each line looks like "x, y\n"
	for line in lines:
	    # Split the data out from the line:
	    data = line.split(",")
	    #print "data=", data
	    x_new = float(data[0].strip(" \n"))
	    y_new = float(data[1].strip(" \n"))
	    #print "({0}, {1})".format(x_new, y_new)

	    # Draw the line:
	    self.line_draw(x, y, x_new, y_new, color)

	    # Remember the end-point:
            x = x_new
            y = y_new

    def save(self):
	""" Save the current temperature run as a data file. """

        # Grab the temperatures:
	temperatures = self.temperatures

	# Open an output stream to write the data to:
	out_stream = tkFileDialog.asksaveasfile(title = "Temperature Run")

	# Write out all the data in CSV (comma separated values) format:
	t = 0
	for temperature in self.temperatures:
	    #print "t[{0}]={1}".format(t, temperature)
            out_stream.write("{0}, {1}\n".format(t, temperature))
            t += 1

	# Close it off:
	out_stream.close()
	
	# For get the temperatures prior for the next run.
	del temperatures[:]

# Run the application:
app = Application()                    
app.master.title("Temperature Profile Charter") 
app.mainloop()

