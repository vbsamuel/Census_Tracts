## Importing libraries
import pandas as pd
import numpy as np
import seaborn as sns
import csv

## Loading the input file
df1 = pd.read_csv('../input/censustract-00-10.csv', encoding = "ISO-8859-1", engine='python')
df2=df1.copy()


### Fill-in empty value for CBSA09 with COU10
df2['CBSA09'] = df2.apply(lambda row: row['COU10'] if np.isnan(row['CBSA09']) else row['CBSA09'], axis=1)


## Sum the number of counts for Census Tracts
df2["TRACTS"]=df2.groupby("CBSA09")["CBSA09"].transform("count")


## Function to removing "," from object datatype and
## converting them to int & sum the values
def Fo1(ser):
    lst = list(ser)
    lst2 = [int(x.replace(',','')) for x in lst]
    return sum(lst2)


## Adding POP00 and appending to dataframe
dict1 = dict(df2.groupby("CBSA09")["POP00"].apply(Fo1))
df2["Pop2000"]=df2["CBSA09"].map(dict1)


## Adding POP10 and appending to dataframe
dict2 = dict(df2.groupby("CBSA09")["POP10"].apply(Fo1))
df2["Pop2010"]=df2["CBSA09"].map(dict2)


## Removing "," and "(X)" from PPCHG
## Converting PPCHG Object datatype to Float
df2["NewPPCHG"]=df2["PPCHG"].replace(["(X)"], 0)
df2["NewPPCHG"]=df2["NewPPCHG"].str.replace(",","").astype(float)


## Average of the NewPPCHG Value and rounded to two decimal places
df3 = round(df2.groupby('CBSA09')['NewPPCHG'].mean(),2)
dict3 = dict(df3)
df2["NewAvePPCHG"]=df2["CBSA09"].map(dict3)


## forming a state identifier for processing missing values in CBSA_T
## we will use ST10 as baseline to identify the state and extract the state initials that are already correspond to the available state descriptions in CBSA_T
## the state identifier will make it easier for the a human to understand which state these missing values belong to.

df7 = df2[["ST10","CBSA_T"]]
df8 = df7.drop_duplicates().reset_index(drop=True)
df8["NewCBSA_T"] = df8["CBSA_T"].str[-2:]
df9=df8[["ST10","NewCBSA_T"]]
df10=df9.groupby("ST10").last().reset_index()
dict5=dict(df10)


## key dictionary for state and corresponding CBSA_T file
new_keys = list(dict5['ST10'])
new_values = list(dict5['NewCBSA_T'])
dict7 = dict(zip(new_keys, new_values))


## replace the NaN values in CBSA_T with the curresponding State
def foo(x):
    if str(x[1])=='nan':
        return "NaN, " + dict7[x[0]]
    else:
        return x[1]

## Applying Substitute value
df2["CBSA_T"] = pd.DataFrame(df2[['ST10','CBSA_T']].apply(foo, axis=1))

## Wrapping '' around CBSA_T
df2["CBSA_T"]= df2["CBSA_T"].apply(lambda x : '"'+x+'"')


## dropping all non required columns
df5 = df2[["CBSA09","CBSA_T","TRACTS","Pop2000","Pop2010","NewAvePPCHG"]]
output_df = pd.DataFrame(df5)


## Preparing final output csv file
## keep first duplicate row
FinalResult_df1 = output_df.drop_duplicates().reset_index(drop=True)
FinalResult_df1.sort_values(["CBSA09"], axis=0,ascending=True, inplace=True)
FinalResult_df1.to_csv('../output/report.csv',index=False)

## end of program

