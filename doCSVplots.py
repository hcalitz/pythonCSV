# doCSVplots.py
# JJ Calitz 
# July 2016
# IFS Massey University
# Palmerston North, New Zealand

# NAME
#     doCSVplots.py - plot the contents of a CSV file.
 
# SYNOPSIS
#     python doCSVplots.py [-r startrow stoprow] [-c condition] [-f line [marker]] [-o plotfilename] filename [x y1 [y2 y3 ... yn]]

# EXAMPLE
#     python doCSVplots.py mydata.csv "Date" "Median Value" "1st max value" -r 83 2000 -c "Site Num" == "003" -f x -
#
# DESCRIPTION 
#     Generates customised plots form selected columns, with optional row selection and condition selection
# 
#		-c 
# 			a condition is imposed on any column and has the format:  field operator value
# 			e.g. 
# 				-c "'Site Num' == 003"
# 				-c "Latitude < -29.02"
#
#		-f
#			sets the line format and marker format. Parameters in quotes to prevent command line confusion
#			default line '-', no marker
#			e.g.
#				-f "--" "^"
#				-f "-"
# 			Marker Code 	Marker Displayed
# 				+ 	Plus Sign
# 				. 	Dot
# 				o 	Circle
# 				* 	Star
# 				p 	Pentagon
# 				s 	Square
# 				x 	X Character
# 				D 	Diamond
# 				h 	Hexagon
# 				^ 	Triangle
# 
# 			Linestyle Code 	Line style Displayed
# 				- 	Solid Line
# 				-- 	Dashed Line
# 				: 	Dotted Line
# 				-. 	Dash-Dotted Line
# 				None 	No Connecting Lines#
#
#		-o 
#			Sets output file name, will not show graph
#
#		-r
# 			limit row range between these values. This limitation is set after condition selection is done.
#
# EXAMPLES 
#	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -
#	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -
#	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -
#	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -
#	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -


import pandas as pd
import matplotlib.pyplot as plt
import shlex
import os.path

# For reading from the command line 
import sys

def ParseCommandline (flag, numargs, arglist, headerlist):
    if flag in arglist:
        flagpos = arglist.index(flag)
    else:
        flagpos = -1
    flagList = ['-c','-f','-o','-r']
    # Specify Line and Marker formats
    if flag == "-f":
        linetext = '-'
        marktext = ''
        markers = ['+','.','o','*','p','s','x','D','h','^']
        lines = ['-','--',':','-.','None']        
        # if at end of arglist, and marker not specified
        if len(arglist) > (flagpos+2) and (flagpos > 0):
            if arglist[flagpos+2] in markers:
                marktext = markers[markers.index(arglist[flagpos+2])]    
        if arglist[flagpos+1] in lines:
            linetext = lines[lines.index(arglist[flagpos+1])]
        return linetext, marktext

    # Optional: Read condition function form the command line
    if flag == "-c":
        condition = ''
        itemsTobeAdded = []
        if flagpos > 0:
            # extract the extra columns to be loaded from the header
            cstring = shlex.split(arglist[flagpos+1])
            buildstring = ''
            for k in cstring:
                if k in headerlist:
                    itemsTobeAdded.append(k)
                    buildstring = buildstring + "df['" + k + "']"
                else:
                    buildstring = buildstring + ' ' + k + ' '
            condition = buildstring
        return itemsTobeAdded, condition
	
    # output file name specified
    if flag == "-o":
        if flagpos > 0:
            outfile = arglist[flagpos+1]
        else:
            outfile = ''
        return outfile
    
    # find the filename and the columns to be plotted
    if flag == 'findfile':
        readCols = 0
        selectCols = []
        for count in range(1,len(arglist)):
            if readCols and (arglist[count] not in flagList):
                selectCols.append(arglist[count])
            else:
                readCols = 0
            if os.path.isfile(arglist[count]) and (arglist[count-1] not in flagList ):
                filename = arglist[count]
                readCols = 1
        return filename, selectCols

# find filename
filename,colsToInclude = ParseCommandline("findfile", 2, sys.argv, sys.argv)
dfheader = pd.read_csv(filename, header=0, nrows=1)

# Read case sensitive column headings from commandline, 
# enclose spaces in inverted commas, e.g. "1 st value"
xvar = colsToInclude[0]
plotCols = colsToInclude[1:]

linetext, marktext = ParseCommandline("-f", 2, sys.argv, dfheader.keys())

extraCols, condition = ParseCommandline("-c", 1, sys.argv, dfheader.keys())
colsToInclude = colsToInclude + extraCols

# Now read the data	  
print "Loading only",colsToInclude,"from ",filename,"...."
if 'Date' in xvar or 'date' in xvar:
    df = pd.read_csv(filename, header=0, usecols=colsToInclude, parse_dates=[xvar])
    x= [pd.Timestamp.date(df[xvar][elem]) for elem in range(len(df[xvar]))]
    usedates = 1
else:
    df = pd.read_csv(filename, header=0, usecols=colsToInclude)
    usedates = 0
print len(df[xvar]),"data points loaded"

if condition != '':  
    df = df.loc[eval(condition)]
    print "Apply restrictions:", condition,"(",len(df[xvar]),"data points)"

# Optional: Read the range values from the command line 
if "-r" in sys.argv:
    flagpos = sys.argv.index("-r")
    startrow = int(sys.argv[flagpos+1])
    stoprow = int(sys.argv[flagpos+2])
else:
    startrow = 1
    stoprow = len(df[xvar])

print "Plotting",plotCols, "with", len(df[xvar]),"data points"

#Plot the data 
fig = plt.figure(1)
#ax = fig.add_subplot(111)
ax = fig.add_axes([0.1, 0.12, 0.6, 0.75])

for ydat in plotCols:
    if usedates:
        if marktext=='None':
            ax.plot(x[startrow:stoprow],df[ydat][startrow:stoprow], label=ydat, linestyle=linetext)
        else:
            ax.plot(x[startrow:stoprow],df[ydat][startrow:stoprow], label=ydat,marker=marktext, linestyle=linetext)
        fig.autofmt_xdate()
    else:
        if marktext=='None':
	        ax.plot(df[xvar][startrow:stoprow],df[ydat][startrow:stoprow], label=ydat, linestyle=linetext)
        else:
            ax.plot(df[xvar][startrow:stoprow],df[ydat][startrow:stoprow], label=ydat,marker=marktext, linestyle=linetext)
            	    
handles, labels = ax.get_legend_handles_labels()
ax.set_xlabel(xvar)
lgd = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

outfile = ParseCommandline("-o", 1, sys.argv, dfheader.keys())
if outfile != '':
    print "Graph written to",outfile
    plt.savefig (outfile, bbox_extra_artists=(lgd,), bbox_inches='tight')
else:
    plt.show()
    

