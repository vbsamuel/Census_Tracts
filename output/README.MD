This is the directory where the program would write out output files.

The report.csv, with as many lines as unique Core Based Statistical Areas found in the input file.

Following 6 data elements can be found in the report.csv file in the below order:

(1) CBSA09 : Core Based Statstical Area Code (i.e., CBSA09). Any value from 1 to 720 corresponds to COU10 column in the input file. This is because the original CBSA09 column had NULL data. Values from 10020 and upwards (all 5-digit numbers) corresponds to the original CSBA09 value.

(2) CBSA_T : Core Based Statistical Area Code Title (i.e., CBSA_T). For the CBSA_T missing we have substituted with "NaN, STATE INITIAL". The "STATE INITIAL" value is two digit alphabet corresponding to the state value from ST10. Instead of using plain "ST10" we used the state prefix such as CA, TX, etc to make it easy for reading.

(3) TRACTS : total number of census tracts for the Core Based Statistical Area Title

(4) Pop2000 : total population in the CBSA in 2000

(5) Pop2010 :total population in the CBSA in 2010

(6) NewAvePPCHG : average population percent change for census tracts in this CBSA. Round to two decimal places using standard rounding conventions. (Please note that the Any percentage between 0.005% and 0.010%, inclusive, should round to 0.01% and anything less than 0.005% should round to 0.00%)

The lines in the report.csv file will be sorted by Core Based Statstical Area Code (ascending)
