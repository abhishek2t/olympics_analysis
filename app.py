import streamlit as st
import pandas as pd
import preprocessor,helper#( importing file that we made named preprocessor.py)
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df=preprocessor.preprocess()
df.drop_duplicates(inplace=True)
st.sidebar.title('Olympics Analysis')## adding title on the top of side bar
# creating sidebar having options we have to select from that options
user_menu = st.sidebar.radio("Select An Option",('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))


if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')#if medal tally is selected then display this
    years,country=helper.country_year_list(df)
    select_year=st.sidebar.selectbox('select years',years)
    select_country = st.sidebar.selectbox('select country', country)
    medal_tally=helper.fetch_medal_tally(df,select_year,select_country)
    if select_year=='overall' and select_country=='overall':
        st.title("Overall Tally")

    if select_year!='overall' and select_country=='overall':
        st.title("Medal Tally In Year " + str(select_year))
    if select_year=='overall' and select_country!='overall':
        st.title(select_country + "overall performance")

    if select_year!='overall' and select_country!='overall':
        st.title(select_country + " Performance in " + str(select_year) + " Olympics")
    st.table(medal_tally)## using st.table instead of dataframe for better look

if user_menu=='Overall Analysis':
    sport=df['Sport'].dropna().unique().tolist()
    sport.sort()
    sport.insert(0,'overall')

    select_sport=st.sidebar.selectbox('Sport Name',sport)

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    
    fig1 = px.line(nations_over_time, x="Edition", y="Nations over time")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig1)

    events_over_time = helper.data_over_time(df, 'Event')
    fig2 = px.line(events_over_time, x="Edition", y="Events over time")
    st.title("Events over the years")
    st.plotly_chart(fig2)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig3 = px.line(athlete_over_time, x="Edition", y="Atheletes over time")
    st.title("Athletes over the years")
    st.plotly_chart(fig3)


    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most sucessful player')
    x=helper.most_successful(df,select_sport)
    st.table(x)


if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    regions=df['region'].dropna().unique().tolist()
    regions.sort()
    
    select_country_Name=st.sidebar.selectbox('Select Country Name',regions)

    countriymedal_over_time = helper.country_wise_medal_tally_per_year(df,select_country_Name)
    fig1 = px.line(countriymedal_over_time, x="Year", y="total medal")
    st.title("{} Medal Tally Over the year ".format(select_country_Name))
    st.plotly_chart(fig1)


    st.title("{} excel in the following Sport ".format(select_country_Name))
    fig2,ax = plt.subplots(figsize=(20,20))
    
    ax = sns.heatmap(helper.country_event_heatmap(df,select_country_Name),annot=True)
    st.pyplot(fig2)

    sport=df['Sport'].dropna().unique().tolist()
    sport.sort()
    sport.insert(0,'overall')

    select_sport=st.sidebar.selectbox('Sport Name',sport)
    if select_sport=='overall':
        st.title('Most sucessful player of {} '.format(select_country_Name))
    if select_sport!='overall':
        st.title('Most sucessful player of {} in {} '.format(select_country_Name,select_sport))
        
    x=helper.country_top_performer(df,select_country_Name,select_sport)
    st.table(x)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()# removing null values in age for bronze medal

    fig1 = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False,width=1000,height=600)#increasing the size of figure
    st.title("Distribution of Age")
    st.plotly_chart(fig1)


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig2 = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig2.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig2)


    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    
    selected_sport = st.sidebar.selectbox('Select a Sport', sport_list)
    st.title('Height Vs Weight for {}'.format(selected_sport))
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



 


 

