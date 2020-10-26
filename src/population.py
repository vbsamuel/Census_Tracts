## Importing libaries
import pandas as pd
import numpy as np
import seaborn as sns
import csv
import os

## Loading the input file
## We are opening the top most file from the input folder
path='../input'
file = os.listdir(path)
filename = file[0]
FullPathFileName = os.path.join(path,filename)
df01 = pd.read_csv(FullPathFileName, encoding = "ISO-8859-1", engine='python')
df02=df01.copy()

### Fill-in empty value for CBSA09 with COU10
df02['CBSA09'] = df02.apply(lambda row: row['COU10'] if np.isnan(row['CBSA09']) else row['CBSA09'], axis=1)


## Sum the number of counts for Census Tracts
df02['TRACTS']=df02.groupby('CBSA09')['CBSA09'].transform("count")


## Preparing CBSA_T - forming a state identifier for processing missing value
df03 = df02[['ST10','CBSA_T']]
df04 = df03.drop_duplicates().reset_index(drop=True)
df04['NewCBSA_T'] = df04['CBSA_T'].str[-2:]
df05=df04[['ST10','NewCBSA_T']]
df06=df05.groupby('ST10').last().reset_index()
dict1=dict(df06)


## Preparing CBSA_T - key dictionary for state and corresponding CBSA_T file
new_keys = list(dict1['ST10'])
new_values = list(dict1['NewCBSA_T'])
dict2 = dict(zip(new_keys, new_values))


## Preparing CBSA_T - replace the NaN values in CBSA_T with the curresponding State
def foo(x):
    if str(x[1])=='nan':
        return "NaN, " + dict2[x[0]]
    else:
        return x[1]

## Preparing CBSA_T - Applying Substitute value
df02['CBSA_T'] = pd.DataFrame(df02[['ST10','CBSA_T']].apply(foo, axis=1))

## Wrapping '' around CBSA_T
df02['CBSA_T']= df02['CBSA_T'].apply(lambda x : '"'+x+'"')

## Local Assignment of datatypes for number column
## they can come either in numbers or strings
POP00_dty = df02['POP00'].dtypes
POP10_dty = df02['POP00'].dtypes
PPCHG_dty = df02['PPCHG'].dtypes

## Function to removing "," from object datatype and
## converting them to int & sum the values
def Fo1(ser):
    lst = list(ser)
    lst2 = [int(x.replace(',','')) for x in lst]
    return sum(lst2)


## Adding POP00 and appending to dataframe
if (POP00_dty == "int64") or (POP00_dty == "float64"):
    dict3 = dict(df02.groupby("CBSA09")["POP00"].sum())
    df02["Pop2000"]=df02["CBSA09"].map(dict3)
else:
    dict3 = dict(df02.groupby("CBSA09")["POP00"].apply(Fo1))
    df02["Pop2000"]=df02["CBSA09"].map(dict3)

    
## Adding POP10 and appending to dataframe
if (POP10_dty == "int64") or (POP10_dty == "float64"):
    dict4 = dict(df02.groupby("CBSA09")["POP10"].sum())
    df02["Pop2010"]=df02["CBSA09"].map(dict4)

else:
    dict4 = dict(df02.groupby("CBSA09")["POP10"].apply(Fo1))
    df02["Pop2010"]=df02["CBSA09"].map(dict4)

## Average of the PPCHG Value and rounded to two decimal places
if (PPCHG_dty == "int64") or (PPCHG_dty == "float64"):
    df03 = round(df02.groupby('CBSA09')['PPCHG'].mean(),2)
    dict5 = dict(df03)
    df02["NewAvePPCHG"]=df02["CBSA09"].map(dict5)
else:
    ## Removing "," and "(X)" from PPCHG
    ## Converting PPCHG Object datatype to Float
    df02["NewPPCHG"]=df02["PPCHG"].replace(["(X)"], 0)
    df02["NewPPCHG"]=df02["NewPPCHG"].str.replace(",","").astype(float)

    ## Average of the NewPPCHG Value and rounded to two decimal places
    df03 = round(df02.groupby('CBSA09')['NewPPCHG'].mean(),2)
    dict5 = dict(df03)
    df02["NewAvePPCHG"]=df02["CBSA09"].map(dict5)


## dropping all non required columns
df05 = df02[["CBSA09","CBSA_T","TRACTS","Pop2000","Pop2010","NewAvePPCHG"]]
output_df = pd.DataFrame(df05)


## Preparing final output csv file
## keep first duplicate row
FinalResult_df1 = output_df.drop_duplicates().reset_index(drop=True)
FinalResult_df1.sort_values(["CBSA09"], axis=0,ascending=True, inplace=True)
FinalResult_df1.to_csv('../output/report.csv',index=False)

## end of program ##
