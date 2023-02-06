import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='StartUp Analysis')



df=pd.read_csv("cleaned_startup_data.csv")

def load_investor_details(investors):
    #function to get the details of the perticular investor
    st.header(investors)
    # last 5 investments
    last_5_df=df[df['investor'].str.contains(investors)].head()[['date','startup','vertical','city','round','amount']].sort_values('date',ascending=False)
    st.subheader("Most recent investments:-")
    st.dataframe(last_5_df)
    #big investments
    big_invest_series=df[df['investor'].str.contains(investors)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    st.subheader("Biggest Investment")
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(big_invest_series)
    with col2:
        fig,ax=plt.subplots()
        ax.bar(big_invest_series.index,big_invest_series.values)
        st.pyplot(fig)
    ####Sector invested in
    st.subheader("Sector Invested In-")
    vertical_series=df[df['investor'].str.contains(investors)].groupby('vertical')['amount'].sum()
    fig1,ax=plt.subplots()
    ax.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
    st.pyplot(fig1)
    #stages invested in:-

    st.subheader("Stages Invested In-")
    round_series=df[df['investor'].str.contains('Sequoia Capital')].groupby('round')['amount'].sum()
    fig2,ax=plt.subplots()
    ax.pie(round_series,labels=round_series.index,autopct="%0.01f%%")
    st.pyplot(fig2)

    # City invested in:-

    st.subheader('City invested in-')
    city_series=df[df['investor'].str.contains(investors)].groupby('city')['amount'].sum()
    fig3,ax=plt.subplots()
    ax.pie(city_series,labels=city_series.index,autopct="%0.01f%%")
    st.pyplot(fig3)

    # Year on year investment-

    st.subheader("Year on Year Investment-")
    yoy_series=df[df['investor'].str.contains('Sequoia Capital')].groupby('year')['amount'].sum()
    fig4,ax=plt.subplots()
    ax.plot(yoy_series.index,yoy_series.values)
    st.pyplot(fig4)



def load_startup_details(startups):
    #function to getthe details of a particular startup....
    st.header(startups)
    st.subheader("Industry:  {}".format(df[df['startup']==startups]['vertical'].iloc[0]))
    st.subheader("Sub Industry:  {}".format(df[df['startup']==startups]['subvertical'].iloc[0]))
    st.subheader("Location:  {}".format(df[df['startup']==startups]['city'].iloc[0]))
    st.subheader("Funding Rounds:")
    round_df=df[df['startup']==startups][['round','investor','date']]
    st.dataframe(round_df)


def load_overall_analysis():
    #total invested amount
    col1,col2,col3,col4=st.columns(4)
    with col1:
        total=round(df['amount'].sum())
        st.metric("Total",str(total)+" Cr")
    #max amount invested
    with col2:
        maxx=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).iloc[0]
        #on=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).index[0]
        st.metric('Maximum_invested',str(maxx)+" Cr")
    with col3:
        #Avg investment
        avg=round(df.groupby('startup')['amount'].sum().mean())
        st.metric("Avg. INvestment",str(avg)+" Cr")
    with col4:
        #Total funded startups
        total_funded=df['startup'].nunique()
        st.metric("Total Funded startups",str(total_funded))
    

    #mom chart
    
    st.header("Month on month graph:")
    selected_option=st.selectbox('selected_type',['Total','Count'])
    
    if selected_option=='Total':
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
        temp_df['x_axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
        fig4,ax4=plt.subplots()
        ax4.plot(temp_df['x_axis'],temp_df['amount'])
        plt.xticks(rotation ='vertical')
        st.pyplot(fig4)
    elif selected_option=='Count':
        temp_df=df.groupby(['year','month'])['startup'].count().reset_index()
        temp_df['x_axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
        fig5,ax5=plt.subplots()
        ax5.plot(temp_df['x_axis'],temp_df['startup'])
        plt.xticks(rotation ='vertical')
        st.pyplot(fig5)


    # Sector Analysis
    st.subheader("Sector Analysis")
    col5,col6=st.columns(2)
    with col5:
        st.write("Count of Sectors-")
        cnt_series=df.groupby('vertical').size().sort_values(ascending=False).head(10)
        fig7,ax7=plt.subplots()
        ax7.pie(cnt_series,labels=cnt_series.index,autopct="%0.01f%%")
        st.pyplot(fig7)
    with col6:
        st.write("Amount of investment done in a sector-")
        amnt_series=round(df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10))
        fig8,ax8=plt.subplots()
        ax8.pie(amnt_series,labels=amnt_series.index,autopct="%0.01f%%")
        st.pyplot(fig8)
    st.subheader("City wise funding-")
    city_fund_series=round(df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10))
    fig9,ax9=plt.subplots()
    ax9.pie(city_fund_series,labels=city_fund_series.index,autopct="%0.01f%%")
    st.pyplot(fig9)

    #Top startups->year wise->total

    st.subheader("Top StartUps and Investors-")
    col7,col8=st.columns(2)
    with col7:
        st.write("Startups-")
        top_su_series=round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10))
        fig10,ax10=plt.subplots()
        ax10.bar(top_su_series.index,top_su_series.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig10)
    
    #Top Investors ->overall
    with col8:
        st.write("Investors-")
        top_in_series=round(df.groupby('investor')['amount'].sum().sort_values(ascending=False).head(10))
        fig11,ax11=plt.subplots()
        ax11.bar(top_in_series.index,top_in_series.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig11)

st.sidebar.title("Startup Funding Analysis")
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    st.title('Overall Analysis')
    load_overall_analysis()
elif option=='Startup':
    selected_startup=st.sidebar.selectbox('Select Strartup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("Find StartUp Details")
    st.title('StartUp Analysis')
    if(btn1):
        load_startup_details(selected_startup)
else:
    selected_investor=st.sidebar.selectbox('Select StartUp',sorted(set(df['investor'].str.split(",").sum())))
    btn2=st.sidebar.button("Find Investor Details")
    st.title('Investor Analysis')
    if(btn2):
        load_investor_details(selected_investor)

