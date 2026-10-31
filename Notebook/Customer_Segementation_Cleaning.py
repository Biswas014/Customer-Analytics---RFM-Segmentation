# Importing Libraries
import pandas as pd
import numpy as np

# Importing the raw file
df1 = pd.read_csv(r"E:\Projects\Portfolio_Projects\Python&BI\Online Retails 2\archive\online_retail_II.csv")

''' used a raw string since python can't work with backslashes,
r tells Python to treat backslashes as literal characters rather than escape sequences.'''

# Data Exploration

# print(df1.info())  # (1067371,8)

## duplicates checking


# print(df1.duplicated().sum()) 
#    #34335 number of complete duplicate rows without their first occurrences

# ## to see which rows are repeated with their duplicates
duplicates = df1[df1.duplicated(keep=False)]
# print(duplicates.sort_values('Description').head(15))

df1.drop_duplicates(inplace= True)
# print(df1.duplicated().sum())   #0


# ## creating 2 udfs for checking missing and nulls records dynamically
def missing_value_report(df,col):
    empty_str = (df[col] == '').sum()
    whitespace_only = (df[col].str.strip() == '').sum() - empty_str
    has_leading_trailing = df[col].notnull() & (df[col] != df[col].str.strip())

    print(f"empty_string : {empty_str}")
    print(f"whitespace_only : {whitespace_only}")
    print(f"leading/trailing : {has_leading_trailing.sum()}")

# ## retrieve nan/ unrecognized nulls(python) values in a clmn
def nan_or_unrecognized_missing(df, col, possible_junk_tokens=None):
    if possible_junk_tokens is None:
        possible_junk_tokens = ['N/A', 'n/a', 'NA', 'missing', 'Missing', '?', '-', 
                              'NULL', 'null', 'None']
    
    is_nan = df[col].isnull()
    is_known_junk = df[col].isin(possible_junk_tokens)
    
#     # Combine: anything flagged as junk , but NOT true NaN
    non_recognized_mask = (is_known_junk ) & ~is_nan  #both condition need to be true
    
    print(f"Column: {col}")
    print(f"  True NaN/None:                {is_nan.sum()}")
    print(f"  Non-recognized junk values:   {non_recognized_mask.sum()}")
    print()
    print("Breakdown of non-recognized values found:")
    print(df.loc[non_recognized_mask, col].value_counts())

# ## invoice

# print(df1[['Invoice']].head(15))

# # find string records in invoice
# cancelled_order = df1[df1['Invoice'].str.startswith('C')]
# print(cancelled_order.head(15))

# print(df1['Invoice'].str.startswith('C').sum()) #19104 Cancelled orders

# print(df1['Invoice'].str.contains(r'[a-zA-Z]',na= False).sum())  # 19110 (consist a letter)

# print(df1[(~df1['Invoice'].str.match(r'^[a-zA-Z]')) & (df1['Invoice'].str.contains(r'[a-zA-Z]'))])
   #0 means - no id contains letters in a different position except in prefix


## check in what type of records invoice id are not start with c but a letter

# diff = df1[~df1['Invoice'].astype('string').str.match(r'^[0-9cC]')]
# print(diff) # 6 

# # missing_value_report(df= df1, col='Invoice')
# # nan_or_unrecognized_missing(df= df1, col= 'Invoice')

# cancelled_bad_debt_invoice_pos_quan = df1[(df1['Invoice'].astype('string').str.match(r'^[a-zA-Z]'))
#                                 & (df1['Quantity']>0)]
# # print(cancelled_bad_debt_invoice_pos_quan)  
#  ## quantity was negative only for orders being cancelled

# ## dropping cancelled & different prefix invoice
df1 = df1[~df1['Invoice'].astype('string').str.match(r'^[a-zA-Z]')]
# # print(df1.shape)   # (1013926, 8)



# ## stock code

# print(df1['StockCode'].head(15))

# print(df1['StockCode'].astype('string').str.contains(r'[a-zA-Z]',na= False).sum())  
  # 127705 records have atleast one letter in them

# print(df1['StockCode'].astype('string').str.fullmatch(r'[0-9]+',na=False).sum()) 
#  # 886221 no of records have all characters in digits

# print(df1[df1['StockCode'].astype('string').str.fullmatch(r'[a-zA-Z]')])

# # rows whose stock code contains no digits at all
letters_only = df1[~df1['StockCode'].astype(str).str.contains(r'\d')]
# letters_only = df1[df1['StockCode'].astype('string').str.fullmatch(r'[a-zA-Z]+')]  
      # both are same

# summary = (
#     letters_only
#     .groupby(['StockCode', 'Description'], dropna=False)
#     .agg(rows=('Invoice', 'size'),
#          min_qty=('Quantity', 'min'),
#          max_qty=('Quantity', 'max'),
#          min_price=('Price', 'min'),
#          max_price=('Price', 'max'))
#     .reset_index()
#     .sort_values('rows', ascending=False)
# )  
# print(summary)

# unique_letter_codes = letters_only['StockCode'].unique()
# print(unique_letter_codes)

exclude_stock_code = ['POST','DOT','M','D','BANK CHARGES','AMAZONFEE',
           'ADJUST','S']

# df1 = df1[~df1['StockCode'].astype(str).str.upper().isin(exclude_stock_code)]
# print(len(df1))


# # missing_value_report(df= df1, col='StockCode')    #one l&d
# # nan_or_unrecognized_missing(df= df1, col= 'StockCode')

# df1['StockCode'] = df1['StockCode'].str.strip()


# # description

# # print(df1['Description'].dtype)

# missing_value_report(df=df1,col='Description')     # 203063 cells contain l&d
# nan_or_unrecognized_missing(df=df1,col='Description') #both exist


df1['Description'] = df1['Description'].str.split().str.join(' ')

junk_descriptions = ['?','missing','Missing']
df1['Description'] = df1['Description'].replace(junk_descriptions,np.nan)

# # missing_value_report(df=df1,col='Description')     # 0 l&d
# # nan_or_unrecognized_missing(df=df1,col='Description')   # 4384 nan

# print(df1[(df1['Description'].isna()) & (df1['Price'] != 0) & (df1['Quantity'] >0)])
#    #zero result means nan description only occurs on rows having negative quantity or zero price



# ## Quantity

# # print(df1['Quantity'].dtype)

# # nan_or_unrecognized_missing(df=df1,col='Quantity')
# # print(df1['Quantity'].head(15))

# # print(df1[df1['Quantity'] <0]) 

# # print(df1[(df1['Quantity'] <0) & (~df1[df1['Invoice'].str.contains('C')])].sum())
# # there 3393 rows out of 21336 records where quantity negative but the order didn't get cancelled

# print(df1[(df1['Quantity']<0)&(df1['Price'] !=0)]) #3393 rows have negative quantity with zero price


## invoice date
# # print(df1['InvoiceDate'].dtype) #str

# # print(df1[['InvoiceDate']].head(30))

# # missing_value_report(df=df1,col='InvoiceDate')
# # nan_or_unrecognized_missing(df=df1,col='InvoiceDate')

# invalid_date = df1[~df1['InvoiceDate'].str.fullmatch(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')]
# print(invalid_date)

df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'])

# # print(df1['InvoiceDate'])
# # print(df1['InvoiceDate'].dt.year.unique())   # 2009, 10,11

# invalid_month = df1[df1['InvoiceDate'].dt.month> 12]
# print(invalid_month)

# invalid_day = df1[df1['InvoiceDate'].dt.day> 31]
# print(invalid_day)

# ## excluding the time part from invoice date and adding that into a new date column
df1['OrderDate'] = pd.to_datetime(df1['InvoiceDate']).dt.normalize()

# # print(df1[['OrderDate','InvoiceDate']])
# # print(df1['OrderDate'].dtype) # datetime64 (only showing date)

# # df1['date'] = df1['InvoiceDate'].dt.date
# # print(df1['date']) # data type - object (only showing date)

# oldest and latest dates of the transaction

# print(df1[['OrderDate']].sort_values(ascending=False,by='OrderDate'))


# ## price

# # print(df1['Price'].dtypes)  #float
# # print(df1['Price'].head(15))

# # unreal_price = df1[df1['Price'] == 0]
# # print(unreal_price) #5993 rows

df1 = df1.drop(df1[df1['Price'] == 0].index)

# # nan_or_unrecognized_missing(df=df1,col='Price')
# print((df1['Price'] ==0).sum())



# ## customer id

# # print(df1['Customer ID'].dtype)  #float
# # print(df1['Customer ID'].head(15))

# print((df1['Customer ID'] <=0).sum())

# nan_or_unrecognized_missing(df=df1,col='Customer ID')   
#    #226857

df1['Customer ID'] = df1['Customer ID'].astype('Int64')
# # print(df1['Customer ID'].head(15))
# # print(df1['Customer ID'].dtype)  #int64

# # print(df1[df1['Customer ID'].isna()].tail(15))


# ## dropping missing customer id's for preventing any wrong calculation for rfm
df1 = df1.dropna(subset= ['Customer ID'])

# # print((df1['Customer ID'].isna()).sum())
# ## OR
# # nan_or_unrecognized_missing(df= df1,col='Customer ID')



# ## country

# # print(df1['Country'].dtype)
# # print(df1['Country'].unique())

# # nan_or_unrecognized_missing(df=df1,col='Country')
# # missing_value_report(df=df1,col='Country')

# exporting clean data into an new dataframe

# ## Work on customer segmentaion

snapshot_date = pd.to_datetime('2011-12-10')

rfm = df1.groupby('Customer ID').agg(
    recency = ('OrderDate',lambda x: (snapshot_date - x.max()).days),
    frequency = ('Invoice','nunique'),
    monetary = ('Quantity',lambda x: (x * df1.loc[x.index,'Price']).sum())
).reset_index()

# print(rfm)

# print(rfm['recency'].mean())  # 201.9
# print(rfm['recency'].median())  #96
# print(rfm['recency'].quantile([0.5,0.75,0.9]))
  # 96, 380, 535.3
  
# # score customers and assign business segments

rfm['R_Score'] = pd.qcut(rfm['recency'],5,labels= [5,4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['frequency'].rank(method= 'first'),5,labels= [1,2,3,4,5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['monetary'],5,labels= [1,2,3,4,5]).astype(int)

# print(rfm)

def segment_customer(row):
    if row['R_Score'] >=4 and row['F_Score'] >=4 and row['M_Score'] >=4:
        return 'Champions'
    elif row['R_Score'] >=3 and row['F_Score'] >=3:
        return 'Loyal'
    elif row['R_Score'] <=2 and row['F_Score'] >=3:
        return 'At Risk'
    elif row['R_Score'] >=4 and row['F_Score'] <=2:
            return 'New'
    elif row['R_Score'] ==3 and row['F_Score'] <=2:
            return 'Need Attention'
    else:
         return 'Lost'

rfm['Segment'] = rfm.apply(segment_customer,axis=1)
rfm['Is_churned'] = rfm['recency'] > 90

# print(rfm)

# print(df2[['Customer ID']].nunique())     #5853

# ## create two csv files usings rfm and df1 dataframes 

df1['Revenue'] = df1['Quantity'] * df1['Price']


country_lookup = df1[['Customer ID','Country']].drop_duplicates(subset='Customer ID')
rfm = rfm.merge(country_lookup,on= 'Customer ID',how='left')


# print(len(rfm))   #5853
# print(rfm['Customer ID'].nunique()) #5853

col_order = ['Invoice','StockCode','Description','OrderDate','Customer ID','Quantity',
             'Price','Revenue']
df2 = df1[col_order]
# print(df2)

# df2.to_csv(r'E:\Projects\Portfolio_Projects\Python&BI\Online Retails 2\Transactions.csv',index=False)
# rfm.to_csv(r'E:\Projects\Portfolio_Projects\Python&BI\Online Retails 2\Customers.csv',index=False)

# create an calendar table 
start = df2['OrderDate'].min().normalize()
end = df2['OrderDate'].max().normalize()

calendar = pd.DataFrame({'Date':pd.date_range(start,end,freq='D')})

calendar['Year'] = calendar['Date'].dt.year
calendar['Quarter'] = calendar['Date'].dt.quarter
calendar['Month'] = calendar['Date'].dt.month
calendar['Month_Name'] = calendar['Date'].dt.month_name()


#Exporting the calendar tbl
# calendar.to_csv(r'E:\Projects\Portfolio_Projects\Python&BI\Online Retails 2\Calendar.csv',index=False)