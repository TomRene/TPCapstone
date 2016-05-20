"""
Created on Fri May 13 10:33:02 2016
@author: tompichard
This files does GetShapeSave then TransformSave then AnalyzeSave
V1.0: 
1) Enter stock code, Start Date, End Date. 
2) Process in from Yahoo Finance, re-index and sort.
3) Perform transformations to normalize OHLC based on Adj_CLose and round.
4) Format file dates then save shaped file to Shaped directory.
5) Use shaped file and create new df to contain only columns needed.
6) Add relative lows LLOWs
7) Add L1 and CT1s
8) Added the preliminary projection stats
"""

from yahoo_finance import Share
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as pltf
import datetime

# 1) Enter stock IBMsymbol and timeframe.

t = raw_input('Enter Stock Symbol: ')
y = raw_input('Enter Start Date in YYYY-MM-DD format: ')
z = raw_input('Enter End Date in YYYY-MM-DD format: ')


# 2) Load security history.

security = Share(t)
df = security.get_historical(y, z)
table = pd.DataFrame(df)

# 2.1) Re-index and sort dataframe. 

table[' '] = 0
table[' '] = max(table.index) - range(len(table))
table = table.set_index([' '])
table.sort_index(inplace=True)

print table


# 3) Define and run functions to normalize open, high and lows, and allow
# open high, low and adj_closes to be rounded.

def newlow(x):
    if x['Adj_Close'] != x['Close']:
        return float(x['Low']) / (float(x['Close']) / float(x['Adj_Close']))
    else:
        return float(x['Low'])

def newopen(x):
    if x['Adj_Close'] != x['Close']:
        return float(x['Open']) / (float(x['Close']) / float(x['Adj_Close']))
    else:
        return float(x['Open'])
    
def newhigh(x):
    if x['Adj_Close'] != x['Close']:
        return float(x['High']) / (float(x['Close']) / float(x['Adj_Close']))
    else:
        return float(x['High'])

def convadjclos(x):
    tt = float(x['Adj_Close'])    
    return tt

table['NOpen'] = table.apply(newopen, axis=1)
table['NHigh'] = table.apply(newhigh, axis=1)
table['NLow'] =  table.apply(newlow, axis=1)
table['Adj_Close'] =  table.apply(convadjclos, axis=1)

table['NLow'] = np.round(table.NLow,2)
table['NHigh'] = np.round(table['NHigh'],2)
table['NOpen'] = np.round(table['NOpen'],2)
table['Adj_Close'] = np.round(table['Adj_Close'],2)        


# 4) Establish data formatting for saving to file note(t ref in section 1 above).

y = datetime.datetime.strptime(y, '%Y-%m-%d')
y = y.strftime('%m-%d-%Y')
z = datetime.datetime.strptime(z, '%Y-%m-%d')
z = z.strftime('%m-%d-%Y')
newname = '{0}__{1}__{2}'.format(t,y,z)

# 4.1) Save to Shaped directory.

xx = '/Users/tompichard/documents/personal/newpersonal/gads/1.capstone/phase2/stockdata/shaped/'+newname+'.csv'
xx = table.to_csv(xx)


# 5) Take table df and save as table2 with only columns needed.

table2 = table[['Date', 'Symbol', 'NOpen', 'NHigh', 'NLow', 'Adj_Close']]

# 6) {Creating Lows} 
# create f for convenience in inserting 1 letter in loop below.
f = table2

# 6.1) Identify the lows and store in a separate list.

lows = []
c = 0
while c < (len(table)-2):     
    #print f[c], c
    if f.NLow[c+1] < f.NLow[c] and f.NLow[c+1] < f.NLow[c+2]:
        #lo = np.round(f.NLow[c+1],2)
        lo = float("{0:.2f}".format(f.NLow[c+1]))
        lows.append(['LLOW',lo, c+1, f.Date[c+1]])
    c = c+1

# 6.2) make the above list into a df.
    
lows2 = pd.DataFrame(lows, columns = ['Type', 'NLow', 'OrInd', 'Date'])

# 6.3) set OrInd as index in a new df to enable merging into table2.

lows4concat = lows2.set_index('OrInd')

# 6.4) merge LLOs into table 2.

result = pd.merge(left=f,right=lows4concat, how='left')

# 7) Create the triplets (CT1s).
# Filter only LLOW records (for processing) then make df.

table3 = result[(result['Type']=='LLOW')]
table4 = pd.DataFrame(table3)

# 7.1) Initialize Type2 column.

table4['Type2'] = 'NaN'
    
# 7.2) Identify and record L1s which are lows that have a subsequent higher low.
# These will be used in the next routine.

ctr = 0
while ctr < len(table3)-1:
    L1 = table4.iloc[ctr].NLow
    L2 = table4.iloc[ctr+1].NLow     
    #print L1, L2    
    if L1 < L2:
        table4.iloc[ctr,7] = 'L1' 
        ctr +=1
    else:
        ctr +=1

# 7.3) Seed the next table.

table5 = pd.DataFrame(table4)
table5['Type3'] = 'NaN'

# 7.4) Identify and record CT1s i.e. patterns with 3 consecutive rising lows.
# Note CT1s appear on the first low of that pattern.

ctr2 = 0
while ctr2 < len(table5)-2:
    L1 = table5.iloc[ctr2].Type2
    L2 = table5.iloc[ctr2+1].Type2
    L3 = table5.iloc[ctr2+2].Type2        
    if L1 == L2 == 'L1':
        table5.iloc[ctr2,8] = 'CT1' # assigns Triplet as consecutive triplet1
        ctr2 +=1
    else:
        ctr2 +=1
        
table7 = pd.merge(left=result,right=table5, how='left')

# 7.5) Save to Prepped directory.
'''
yy = '/Users/tompichard/documents/personal/newpersonal/gads/1.capstone/phase2/stockdata/prepped/'+newname+'.csv'
yy = table7.to_csv(yy)
'''
# 8) below

# 8.1) create filtered df on LLOW and seed/calc 2 new attribute columns

stockmeta1 = table7[(table7['Type']=='LLOW')]
stockmeta1['Run1'] = 'NaN'
stockmeta1['Run2'] = 'NaN'

ctr=0
while ctr < len(stockmeta1):   
    if stockmeta1.at[stockmeta1.index[ctr],'Type3'] == 'CT1':    
        # calculate & store Run1
        run1 = stockmeta1.at[stockmeta1.index[ctr],'Run1'] = stockmeta1.index[ctr+1] - stockmeta1.index[ctr]
        # calculate & store Run2
        run2 = stockmeta1.at[stockmeta1.index[ctr],'Run2'] = stockmeta1.index[ctr+2] - stockmeta1.index[ctr+1]        
        # calculate & store Rise1
    ctr = ctr + 1

# 8.2) Merge these results into the mother dataset 'table7'

stockpredict1 = pd.merge(left=table7,right=stockmeta1, how='left')

''' metacode
1) find CT1s
2) peg Open 1 day after CT1s
3) peg (A) the 1 week avg of closes after CT1 + Run1 and Run2
4) peg A + 5 days out 
) Calc the net gain loss in %, and track W L '''

# 8.3 Now create copy df and seed then calculate the trade prediction parameters

stockpredict = stockpredict1

stockpredict['Entry'] = 'NaN'
stockpredict['PLavg1'] = 'NaN'
stockpredict['PLpct1'] = 'NaN'
stockpredict['WL1'] = 'NaN'
stockpredict['PLavg2'] = 'NaN'
stockpredict['PLpct2'] = 'NaN'
stockpredict['WL2'] = 'NaN'

ctr2=0
while ctr2 < len(stockpredict):
    if stockpredict.at[stockpredict.index[ctr2],'Type3'] == 'CT1':    
        # assign the CT1 window
        CT1End = stockpredict.at[stockpredict.index[ctr2],'Run1'] + stockpredict.at[stockpredict.index[ctr2],'Run2']
        # determine entry point
        #print stockpredict.at[stockpredict.index[ctr2,'NOpen']        
        Entry = stockpredict.at[stockpredict.index[ctr2+int(CT1End)+1],'Adj_Close']   #changed to +2 Open on 5/15, then +1 Adj_Close     
        stockpredict.at[stockpredict.index[ctr2], 'Entry'] = Entry
        #print CT1End, Entry        
        # determine average of week following Entry and the second following
        PLav1 = stockpredict.at[stockpredict.index[ctr2],'PLavg1'] = stockpredict['Adj_Close'][ctr2+CT1End+1:ctr2+CT1End+6].mean()
        PLav2 = stockpredict.at[stockpredict.index[ctr2],'PLavg2'] = stockpredict['Adj_Close'][ctr2+CT1End+6:ctr2+CT1End+11].mean()
        # stockmeta1['NLow'][100:200].mean()        
        # Determine the pct winds for avg1 and avg2
        PLpc1 = stockpredict.at[stockpredict.index[ctr2],'PLpct1'] = (PLav1-Entry)/Entry
        PLpc2 = stockpredict.at[stockpredict.index[ctr2],'PLpct2'] = (PLav2-Entry)/Entry
        if PLpc1 > 0:
            stockpredict.at[stockpredict.index[ctr2],'WL1'] = 'W'
        else:
            stockpredict.at[stockpredict.index[ctr2],'WL1'] = 'L' 
        if PLpc2 > 0:
            stockpredict.at[stockpredict.index[ctr2],'WL2'] = 'W'
        else:
            stockpredict.at[stockpredict.index[ctr2],'WL2'] = 'L'    
        #print ctr2, CT1End, Entry, PLav1, PLav2, PLpc1, PLpc2    
    ctr2 = ctr2 + 1
    

# stockpredict.to_csv('/Users/tompichard/Documents/Personal/NEWPERSONAL/GADS/1.CAPSTONE/DevFiles/DATA/' + 'IBMstockpredict1' + '.csv')

# 8.4) Save these results as the larger dataset

yy = '/Users/tompichard/documents/personal/newpersonal/gads/1.capstone/phase2/stockdata/prepped/'+newname+'.csv'
yy = stockpredict.to_csv(yy)

# 8.5) Now create a filtered df on only trades for calculating statistics

stockstat = stockpredict[stockpredict['Type3'] == 'CT1']
print 'Nbr of trades', stockstat['WL1'].count()
print 'Net WL1 return % overall ', stockstat['PLpct1'].mean()
print 'Net WL1 success % overall ', float((stockstat['WL1'][stockstat['WL1']=='W'].count()))/float((stockstat['WL1'].count()))
print 'Net WL2 return % overall ', stockstat['PLpct2'].mean()
print 'Net WL2 success % overall ', float((stockstat['WL2'][stockstat['WL2']=='W'].count()))/float((stockstat['WL2'].count()))

#------------------------------------------------------

# 5/17/16 Add moving average to stockstat df

stockpredict['MovAvg'] = 'NaN'
X = len(stockpredict)
n = 0
while n < X:
    stockpredict['MovAvg'] = stockpredict[['Adj_Close']].rolling(window=200).mean()
    n +=1
    
# 5/17/16 Add printing bars and ma
ax1 = plt.subplot(1,1,1, axisbg='#191919')
#ax1 = plt.axis(0,200,0,200)
pltf.plot_day_summary2_ohlc(ax1, stockpredict.NOpen, stockpredict.NHigh, stockpredict.NLow, stockpredict.Adj_Close, colorup='w', colordown='r')

run = stockpredict.index
rise = stockpredict.MovAvg

plt.plot(run, rise)