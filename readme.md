# doCSVplots.py
 JJ Calitz <BR>
 July 2016 <BR>
 IFS Massey University <BR>
 Palmerston North, New Zealand

 NAME<BR>
	doCSVplots.py - plot the contents of a CSV file.
 
 SYNOPSIS<BR>
	python doCSVplots.py [-r startrow stoprow] [-c condition] [-f line [marker]] [-o plotfilename] filename [x y1 [y2 y3 ... yn]]

 EXAMPLE<BR>
	python doCSVplots.py mydata.csv "Date" "Median Value" "1st max value" -r 83 2000 -c "Site Num" == "003" -f x -

 DESCRIPTION <BR>
	Generates customised plots form selected columns, with optional row selection and condition selection
 
		-c 
 			a condition is imposed on any column and has the format:  field operator value
 			e.g. 
 				-c "'Site Num' == 003"
 				-c "Latitude < -29.02"

		-f
			sets the line format and marker format. Parameters in quotes to prevent command line confusion
			default line '-', no marker
			e.g.
				-f "--" "^"
				-f "-"
 			Marker Code 	Marker Displayed
 				+ 	Plus Sign
 				. 	Dot
 				o 	Circle
 				* 	Star
 				p 	Pentagon
 				s 	Square
 				x 	X Character
 				D 	Diamond
 				h 	Hexagon
 				^ 	Triangle
 
 			Linestyle Code 	Line style Displayed
 				- 	Solid Line
 				-- 	Dashed Line
 				: 	Dotted Line
 				-. 	Dash-Dotted Line
 				None 	No Connecting Lines#

		-o 
			Sets output file name, will not show graph

		-r
 			limit row range between these values. This limitation is set after condition selection is done.

 EXAMPLES <BR>
	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -<BR>
	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -<BR>
	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -<BR>
	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -<BR>
	python doCSVplots.py mydata.csv "Date" "Median Value" -r 12 22 -c "'Site Num' == 003" -f x -

TIPS<BR>
	When plotting large data sets, use the <BR>
	-f 'None' '.' <BR>
	parameter otherwise the routine will produce an overflow error
	

