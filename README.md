# temprof

A python/tkinter program to plot toaster oven reflow solder profiles
using a USB thermocouple.

## Introduction

I do reflow soldering using an inexpensive toaster over than I
purchased from the local drug store on sale for $20.  I use the
toaster oven without modification.

I purchased a USB thermocouple from
[PCSensor.Com](http://PCSensor.Com/) called the Temper1K4.
for about $20 (US) circa 2012.  There is a button on the
thermocouple that causes it to emit a temperature read once
a second as if the data were typed in on the keyboard.  The
thermocouple is really easy to use.

## Usage

* Start temperf.py by typing "python temperf.py"

* Click on the [Open] button and select a profile.  There are two
  supplied profiles "leaded_profile.csv" and "no_lead.csv".  If you
  need to create your own profile for your particular brand of solder
  paste, copy one of the supplied profiles and edit it using your
  favorite text editor.

* Insert the thermocouple into the toaster oven along with the
  PCB to be reflow soldered.

* Turn on the toaster oven.

* Wait 10 seconds and depress the on button on the thermocouple.

* Using your hand crack the toaster oven door open and closed to
  closely approximate the temperature profile.

* When peak temperature is reached, turn off the toaster oven.
  and keep cracking the oven door open/closed to bring the
  temperature down along the profile.

* When done, click on the [Save] button to save the oven run
  in a file.  For example "YYYY-MM-DD-HH-MM.csv".

## Data Formats

The data format is .csv (i.e. comma separated values).  The first
value is a time in seconds, and the second number is the temperature
in Centigrade.

