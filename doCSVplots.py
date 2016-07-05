# doCSVplots.py
# JJ Calitz 
# July 2016
# Palmerston North, New Zealand

# Use program like this on the command line: 
# python doplots.py filename x y [startrow] [stoprow]

import pandas as pd
import matplotlib.pyplot as plt

# For reading from the command line 
import sys

filename = sys.argv[1]

# Read column headings from commandline
xvar = sys.argv[2]
yvar = sys.argv[3]

if 'Date' in xvar or 'date' in xvar:
    df = pd.read_csv(filename, header=0, usecols=[xvar,yvar], parse_dates=[xvar])
    x= [pd.Timestamp.date(df[xvar][elem]) for elem in range(len(df[xvar]))]
    usedates = 1
else:
    df = pd.read_csv(filename, header=0, usecols=[xvar,yvar])
    usedates = 0

# Optional: Read the range values from the command line 
if len(sys.argv) > 4:
    startrow = int(sys.argv[4])
    stoprow = int(sys.argv[5])
else:
    startrow = 1
    stoprow = len(df[xvar])
if usedates:
    plt.plot(x[startrow:stoprow],df[yvar][startrow:stoprow], label=yvar)
    plt.xticks(rotation=30)
else:
	plt.plot(df[xvar][startrow:stoprow],df[yvar][startrow:stoprow], label=yvar)
plt.show()
