# Census Population - Data Engineering Work

## Table of Contents
1. [Overview](README.md#Overview)
1. [Input Dataset](README.md#input-dataset)
1. [Data Engineering](README.md#Data-Engineering)
1. [Expected output](README.md#expected-output)



## Overview
  
The federal Census produces a plethora of datasets on a variety of topics tabulated in a number of different ways. In particular, the Census is known for population counts, including down to census tracts, or relatively small areas that average 4,000 inhabitants. Data at that detailed level is useful, but sometimes it's also helpful to roll up some of the information.

**For this challenge, we want you to take the [2000 to 2010 Census Tract Population Change](https://www.census.gov/data/tables/time-series/dec/metro-micro/tract-change-00-10.html) dataset, perform a few calculations and then write out a new file with the summarized data.


## Input dataset
We will use an input file, `censustract-00-10.csv`, Below is a sample `censustract-00-10.csv` file: 
```
GEOID,ST10,COU10,TRACT10,AREAL10,AREAW10,CSA09,CBSA09,CBSA_T,MDIV09,CSI,COFLG,POP00,HU00,POP10,HU10,NPCHG,PPCHG,NHCHG,PHCHG
02130000100,02,130,000100,4835.518216,1793.906364,,28540,"Ketchikan, AK",,2,C,3801,1736,3484,1694,-317,-8.34,-42,-2.42
02130000200,02,130,000200,5.204047664,0.4525275793,,28540,"Ketchikan, AK",,2,C,4909,2156,4884,2179,-25,-0.51,23,1.07
02130000300,02,130,000300,2.771683112,0.4653222332,,28540,"Ketchikan, AK",,2,C,3054,1493,2841,1394,-213,-6.97,-99,-6.63
02130000400,02,130,000400,14.91968071,0.3246679135,,28540,"Ketchikan, AK",,2,C,2310,891,2268,899,-42,-1.82,8,0.90
48487950300,48,487,950300,933.9565129,6.998080686,,46900,"Vernon, TX",,2,C,2304,916,1849,892,-455,-19.75,-24,-2.62
48487950500,48,487,950500,13.21399173,0.01418539391,,46900,"Vernon, TX",,2,C,3172,1338,2955,1388,-217,-6.84,50,3.74
48487950600,48,487,950600,10.65575478,0,,46900,"Vernon, TX",,2,C,6022,2715,5994,2781,-28,-0.46,66,2.43
48487950700,48,487,950700,13.01780124,0.0371546123,,46900,"Vernon, TX",,2,C,3181,1409,2737,1257,-444,-13.96,-152,-10.79
```

Each line of the input file, except for the first-line header, represents population data for a census tract. Consult this [file layout document produced by the Census](https://www2.census.gov/programs-surveys/metro-micro/technical-documentation/file-layout/tract-change-00-10/censustract-00-10-layout.doc) for a description of each field.

The sample input file is taken from the data file at [2000 to 2010 Census Tract Population Change](https://www.census.gov/data/tables/time-series/dec/metro-micro/tract-change-00-10.html), which contains population counts for census tracts and how much they've changed over the decade. While census tracts are fairly small geographical areas inhabited by 1,200 to 8,000 people, they also can be grouped into larger Metropolitan and Micropolitan Statistical Areas called Core Based Statistical Areas. These core areas comprise a set of communities, often with a population center and shared economic and social ties. 

Metropolitan and Micropolitan statistical areas can span one or more counties and states. For instance, "New York-Northern New Jersey-Long Island, NY-NJ-PA" is a Metropolitan Statistical Area and Core Based Statistical Area that is centered around New York City, extends east through Long Island and west through northern New Jersey and parts of Pennsylvania.

We will get an output file that provides information about each of the Core Based Statistical Area:
* total number of census tracts, 
* total population in 2000, 
* total population in 2010 and 
* average population percent change for census tracts in this Core Based Statistical Area

Note that census tracts within a Core Based Statstical Area are not necessarily grouped together in the input file, and that there will be a small minority of census tracts that fall outside of any Core Based Statistical Area.

## Data Engineering

The program handles following scenarios of the input file:
- Making the input file reading easier for frequent use. The program will automatically read the input file from the top most position in the file directory. This mechanism becomes useful for frequent updates such as nightly, monthly, quarterly, etc.
- Inconsistant data types for the columns: we have noticed that sometimes the elements are integers and sometimes they are strings. We handle both scenarios. 
- Missing data: We have found a lot of missing elements in the file. For the required 6 data elements, we implemented an appropriate strategy by either a substitued value or a derived value in-place of the null or empty cell. This is done to provide a holistic picture of the result.
- Odd elements in numbers columns: Since we don't control how the original file is created and published, we notice that it is possible for numbers columns to have "(X)" to identify a non-determinant number value such as a percentage gain for rows that didn't have a start value. We removed the "(X)" and substituted with null value.
- Making data readable: In the areas where possible, we made the data easier to understand as supposed to random numbers. Ex. CBSA_T has a blank data element and we would produce the output file with "NaN, State Intital". This would mean that the original data was missing or empty and we had identified which state this data belongs to and put in an state identifier for making it easier for trouble shooting. We also make the final data sorted by ascending order (this also helps for easier look-ups)!.


## Expected output

After reading and processing the input file, the code will create an output file, `report.csv`, with as many lines as unique Core Based Statistical Areas found in the input file. 

Following 6 data elements will be written to the output file in the below order:

(1) CBSA09 : Core Based Statstical Area Code (i.e., CBSA09). Any value from 1 to 720 corresponds to COU10 column in the input file. This is because the original CBSA09 column had NULL data. Values from 10020 and upwards (all 5-digit numbers) corresponds to the original CSBA09 value.

(2) CBSA_T : Core Based Statistical Area Code Title (i.e. CBSA_T). For the CBSA_T missing values we have substituted with "NaN, STATE INITIAL". The "STATE INITIAL" value is two digit alphabet to identify which state it belongs. The State Initiates are derived from ST10 and available CBSA_T data from the data set. Instead of using plain "ST10" we used the state prefix such as CA, TX, WY etc. to make it easy for the reader to identify which state the row belongs to. This helps in reducing time for cross-reference and excel look-ups.
  
(3) TRACTS : Total number of census tracts for the Core Based Statistical Area Title. This is calculated by total count of unique tracts in the Core Based Statistical Area Title.

(4) Pop2000	: Total population in the CBSA in 2000. This is calculated from individual population count for each of the tracts in the Core Based Statistical Area Title for the year 2000.

(5) Pop2010	:Total population in the CBSA in 2010. This is calculated from individual population count for each of the tracts in the Core Based Statistical Area Title for the year 2010.

(6) NewAvePPCHG : Average population percent change for census tracts in the Core Based Statistical Area Title. The unit is in %-percentage. We have rounded the value to two decimal places using standard rounding conventions. (Please note that the any percentage between 0.005% and 0.010%, inclusive has been rounded to 0.01% and anything less than 0.005% has been round to 0.00%)


The lines in the output file will be sorted by Core Based Statstical Area Code (ascending)

Given the above `censustract-00-10.csv` input file, we'd expect an output file, `report.csv` to be stored in the 'output' file directory. Below is an example of report.csv file format
```
28540,"Ketchikan, AK",4,14074,13477,-4.41
46900,"Vernon, TX",4,14679,13535,-10.25
```




