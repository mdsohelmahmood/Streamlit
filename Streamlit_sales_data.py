import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

comment='''Giving title to the page'''

st.title('Sales dashboard')

comment='''Display the data'''

df1 = st.cache(pd.read_excel)("Sales Data.xlsx", sheet_name='Sales Data')
is_check = st.checkbox("Display Sales Data")
if is_check:
    st.write(df1)

df2 = st.cache(pd.read_excel)("Sales Data.xlsx", sheet_name='Product Master')
is_check = st.checkbox("Display Product Data")
if is_check:
    st.write(df2)

df3 = st.cache(pd.read_excel)("Sales Data.xlsx", sheet_name='Emp Master')
is_check = st.checkbox("Display Employee Data")
if is_check:
    st.write(df3)


comment='''Create sidebar'''

st.sidebar.title("Filter data")


comment='''Sidebar dropdown mutiselection'''

productid_list = st.sidebar.multiselect("Select Product ID", df1['Product ID'].unique())
empid_list = st.sidebar.multiselect("Select Employee ID", df3['EMP ID'].unique())
supervisor_list = st.sidebar.multiselect("Select Supervisor", df3['Supervisor'].unique())


comment='''Create new column for revenue'''

df4 = pd.merge(df1,df2, on ='Product ID', how ='inner')
df4['Revenue']=df4['Unit Sold']*df4['Price per unit']
df5 = pd.merge(df4,df3, on ='EMP ID', how ='inner')


comment='''Sort and reset data by date and removing 00:00:00 from date'''

df5=df5.sort_values(by='Date')
df5=df5.reset_index(drop=True)
df5['Date'] = pd.to_datetime(df5['Date'], errors='coerce').dt.date


comment='''Crete start and end date for filter'''

start_date=df5['Date'].iloc[0]
end_date=df5['Date'].iloc[len(df5['Date'])-1]
start_date = st.sidebar.date_input('Start date', start_date)
end_date = st.sidebar.date_input('End date', end_date)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')


comment='''Search for respctive input in the data'''

df_filtered=df5
if productid_list!=[]:
    df_filtered = df_filtered[(df_filtered['Product ID'].isin(productid_list))]

if empid_list!=[]:
    df_filtered = df_filtered[(df_filtered['EMP ID'].isin(empid_list))]

if supervisor_list!=[]:
    df_filtered = df_filtered[(df_filtered['Supervisor'].isin(supervisor_list))]

# start_date=df_filtered['Date'].iloc[0]
# end_date=df_filtered['Date'].iloc[len(df_filtered['Date'])-1]


comment='''Check if start and end date have values. If the exact input start/end date is not 
in the data, it will increase the start date by 1 and decrease the end date by 1 
to look for the next exact match for the input start/end dates'''

if start_date!=[] and end_date!=[]:
    # start_date
    # end_date
    # df_filtered
    if df_filtered.empty==0:
        start=df_filtered[df_filtered['Date'] == start_date].index.tolist()
        if start!=[]:
            start_index=start[0]
        if start==[]:
            for i in range(1,len(df5['Date']),1):
                j=1
                start_date=pd.to_datetime(start_date)+datetime.timedelta(days=j)
                # start_date
                start1 = df_filtered[df_filtered['Date'] == start_date].index.tolist()
                if start1!=[]:
                    break
            # start1
            start_index=start1[0]

        end=df_filtered[df_filtered['Date'] == end_date].index.tolist()
        # end
        if end!=[]:
            end_index = end[len(end) - 1]
        if end==[]:
            for i in range(1,len(df5['Date']),1):
                j = -1
                end_date = pd.to_datetime(end_date) + datetime.timedelta(days=j)
                # end_date
                end1 = df_filtered[df_filtered['Date'] == end_date].index.tolist()
                if end1!=[]:
                    break
            # end1
            end_index=end1[0]

        # start_index
        # end_index
        df_filtered=df_filtered.loc[start_index:end_index]
        # df_filtered
    if df_filtered.empty == 1:
        st.subheader('No revenue earned')


comment='''Create Filter checkbox'''

df6=pd.DataFrame()
is_check = st.sidebar.checkbox("Apply Filter")
df6=df5
check=0
if is_check:
    check=1
    df6=df_filtered
    st.sidebar.subheader('Filter applied')


comment=''' Function for barplot'''

def create_barplot(df6,rev_count2):
    st.header("Revenue in Barplot by products")
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rev_count2=df6.groupby(['Product ID']).sum()['Revenue']
    # rev_count2
    if rev_count2.empty==0:
        ax.bar(
            rev_count2.nlargest(rev_count2.shape[0]).index, \
            rev_count2.nlargest(rev_count2.shape[0])
        )
        plt.xticks(rotation=90)
        st.write(fig)
    if rev_count2.empty==1:
        st.subheader('No revenue earned')


comment='''Function for piechart'''

def create_piechart(df6,rev_count1,check):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rev_count1=df6.groupby(['Supervisor']).sum()['Revenue']

    # check
    if check == 0:
        labels = df3['Supervisor'].unique()
    if check == 1:
        labels = supervisor_list

        if supervisor_list==[]:
            labels=df3['Supervisor'].unique()


    list1_as_set = set(labels)
    list2=rev_count1.index.tolist()
    intersection = list1_as_set.intersection(list2)

    st.header("Revenue in Piechart by supervisor")
    if rev_count1.empty==0:
        ax.pie(
            rev_count1,
            labels=intersection,
            autopct='%1.1f%%',
            shadow=1,
            startangle=90
        )
        st.write(fig)
    if rev_count1.empty==1:
        st.subheader('No revenue earned')


comment='''Function for ploting overtime'''

def create_trend(df3,rev_count3):
    st.header("Revenue over Time")
    fig = plt.figure()
    rev_count3=df6.groupby(['Date']).sum()['Revenue']
    if rev_count3.empty==0:
        plt.plot(rev_count3.index,rev_count3)
        plt.xticks(rotation=90)
        st.write(fig)
    if rev_count3.empty==1:
        st.subheader('No revenue earned')


rev_count1=df6.groupby(['Supervisor']).sum()['Revenue']
rev_count2=df6.groupby(['Product ID']).sum()['Revenue']
rev_count3=df6.groupby(['Date']).sum()['Revenue']

create_barplot(df6,rev_count2)
create_piechart(df6,rev_count1,check)
create_trend(df6,rev_count3)


comment='''Display total revenue besed on the filter'''

st.subheader('Total Revenue = ')
rev = st.empty()
rev.text(df6['Revenue'].sum())







