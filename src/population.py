##!/usr/bin/env python3

import csv
import os



##creating list of list of row values in the original list
with open('./input/censustract-00-10.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

##creating list of list of column values 
columns = [list(x) for x in zip(*data)]

##Position of the required column values in the original list
def findItem(theList, item):
    return [(ind) for ind in range(len(theList)) if item in theList[ind]]

ST10=findItem(columns, 'ST10')
COU10=findItem(columns, 'COU10')
CBSA09=findItem(columns, 'CBSA09') 
CBSA_T=findItem(columns, 'CBSA_T')
POP00=findItem(columns, 'POP00') 
POP10=findItem(columns, 'POP10')
PPCHG=findItem(columns, 'PPCHG') 

ps_ST10=ST10[0]
ps_COU10=COU10[0]
ps_CBSA09=CBSA09[0]
ps_CBSA_T=CBSA_T[0]
ps_POP00=POP00[0]
ps_POP10=POP10[0]
ps_PPCHG=PPCHG[0]

##creating a temp list of required column values
ST10_Values=columns[ps_ST10]
COU10_Values=columns[ps_COU10]
CBSA09_Values=columns[ps_CBSA09]
CBSA_T_Values=columns[ps_CBSA_T]
POP00_Values=columns[ps_POP00]
POP10_Values=columns[ps_POP10]
PPCHG_Values=columns[ps_PPCHG]


######### Substituted the value of missing CBSA09 with COU10 and CBSA_T with ST10
limit1 = len(CBSA09_Values)
for i in range(1,limit1):
    if (CBSA09_Values[i]=="") or (CBSA09_Values[i]==" ")or (CBSA09_Values[i]=="NaN") or (CBSA09_Values[i] == "X"):
        CBSA09_Values[i]=COU10_Values[i]
    if(CBSA_T_Values[i]=="") or (CBSA_T_Values[i]==" "):
        CBSA_T_Values[i]='"NaN, ' +ST10_Values[i]+ '"'
    else:
        CBSA_T_Values[i]='"'+CBSA_T_Values[i]+'"'
    i=i+1



#######Counting Tracts by unique CSBA09 elements
lst0 = CBSA09_Values[1:]
frequency = {}
TRACTS={}
for item in lst0:
    if (item in frequency):
        frequency[item] += 1
    else:
        frequency[item] = 1
for key, value in frequency.items():
    TRACTS.update({key: value})

NEWTRACTS_Dict1=TRACTS



########Counting POP00
process_CBSA09_Values=CBSA09_Values[1:]
process_POP00_Values=POP00_Values[1:]

##removing commas from POP00
lst=process_POP00_Values
lst2 = [int(x.replace(',','')) for x in lst]

##creating a mesh of keys with empty values list 
ID2 = {key: [] for key in process_CBSA09_Values} 
  
## loop to iterate through keys and values 
for key, val in zip(process_CBSA09_Values, lst2): 
    ID2[key].append(int(val))

## Summation of the population
NEWPOP00_Dict2 = {k:sum(v) for k,v in ID2.items()}



#########Counting POP10
process_POP10_Values=POP10_Values[1:]

##removing commas from POP10
lst3=process_POP10_Values
lst4 = [int(x.replace(',','')) for x in lst3]

##creating a mesh of keys with empty values list 
ID3 = {key: [] for key in process_CBSA09_Values} 
  
## loop to iterate through keys and values 
for key, val in zip(process_CBSA09_Values, lst4): 
    ID3[key].append(int(val))

## Summation of the population
NEWPOP10_Dict3 = {k:sum(v) for k,v in ID3.items()}


########Counting Average PPCHG
process_PPCHG_Values=PPCHG_Values[1:]

##removing commas from PPCHG
lst5=process_PPCHG_Values
lst6 = [(x.replace(',','')) for x in lst5]

##removing (x) from PPCHG
for i in range(0, len(lst6)):
    if lst6[i]=="(x)" or lst6[i]=="(X)":
        lst6[i]="0"

##creating a mesh of keys with empty values list 
ID4 = {key: [] for key in process_CBSA09_Values} 
  
## loop to iterate through keys and values 
for key, val in zip(process_CBSA09_Values, lst6): 
    ID4[key].append(val)


### Converting PPCHG values to float
values=0
for k,v in ID4.items():
    d_list = v
    values = [float(item) for item in d_list]
    ID4[k]  =  values


## computing average population change and round it to 2 decimal place
NEWPPCHG_Dict4 = {k:round(sum(v)/len(v),2) for k,v in ID4.items()}


########Counting POP00
process_CBSA_T_Values=CBSA_T_Values[1:]
lst7=process_CBSA_T_Values

##creating a mesh of keys with empty values list 
ID5 = {key: [] for key in process_CBSA09_Values} 
  
## loop to iterate through keys and values 
for key, val in zip(process_CBSA09_Values, lst7): 
    ID5[key].append(val)

## Mapping to CBSA09
NEWCBSA_T_Dict5 = {k:v for k,v in ID5.items()}

##### Preparing Lists to form CSV for final output.

CBSAT_list=list(NEWCBSA_T_Dict5.values())
TRACTS_list=list(NEWTRACTS_Dict1.values())
POP00_list=list(NEWPOP00_Dict2.values())
POP10_list=list(NEWPOP10_Dict3.values())
PPCHG_list=list(NEWPPCHG_Dict4.values())


### Gathering all the values to form List format
def getList(dict): 
    return dict.keys() 

# Driver program - check TRACTS
dict =  NEWCBSA_T_Dict5
NEWCBSA_T_Key_List= list(getList(dict))

# Driver program - check TRACTS
dict =  NEWTRACTS_Dict1
NEWTRACTS_Key_List= list(getList(dict))
    
# Driver program - check POP00
dict =  NEWPOP00_Dict2
NEWPOP00_Key_List= list(getList(dict))

# Driver program - check POP10
dict =  NEWPOP10_Dict3
NEWPOP10_Key_List= list(getList(dict))

# Driver program - check Ave PPCHG
dict =  NEWPPCHG_Dict4
NEWPPCHG_Key_List= list(getList(dict))

### extracting unique CBSA_T values that correspond to CBSA09 
CBSAT_Update_List = []
def Extract(lst100): 
    return [item[0:1] for item in lst100] 

CBSAT_Update_List = Extract(CBSAT_list)

## flattening the list for CBSA_T
CBSAT_flatten_list2 ={}
CBSAT_flatten_list2 = [item for subl in CBSAT_Update_List for item in subl]

#### Preparing the final list of rows for the output file
NewRows=[]
z=len(TRACTS_list)
for b in range(0,z):
    NewRows.insert(b,[NEWCBSA_T_Key_List[b], CBSAT_flatten_list2[b],TRACTS_list[b],POP00_list[b],POP10_list[b],PPCHG_list[b]])
    
##Removing this to conform to testing parameters... can include if the user needs header info
##NewRows.insert(0, ["CBSA09","CBSA_T","Total Tracts", "Total Pop 2000", "Total Pop 2010", "Average %Pop Change"])

#### Writing to the final output csv file
Final_Output = NewRows

# opening the csv file in 'w+' mode 
file = open('output/report.csv', 'w+', newline ='') 
  
# writing the data into the file 
with file:     
    write = csv.writer(file) 
    write.writerows(Final_Output) 

### end of program ###

