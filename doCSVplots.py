# doCSVplots.py
# JJ Calitz 
# July 2016
# IFS Massey University
# Palmerston North, New Zealand

# Use program like this on the command line: 
#     python doplots.py filename x y [startrow] [stoprow]
# e.g.
#     python doplots.py mydata.csv "Date" "Median Value" [startrow] [stoprow]
# or if only certain lines are from eg 83 to 2000 are viewed
#     python doplots.py mydata.csv "Date" "Median Value" 83 2000

import pandas as pd
import matplotlib.pyplot as plt

# For reading from the command line 
import sys

filename = sys.argv[1]

# Read case sensitive column headings from commandline, 
# enclose spaces in inverted commas, e.g. "1 st value" 
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
