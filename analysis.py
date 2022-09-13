import pandas as pd
import numpy as np

def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally=medal_tally.groupby('region')[['Gold', 'Bronze', 'Silver']].sum().sort_values('Gold',ascending=False).reset_index()
    medal_tally['total medals']=medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['total medals'] = medal_tally['total medals'].astype('int')
    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    country=df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,'overall')
    return years,country

def fetch_medal_tally(df,year,country):

    flag=0
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # if have same team,Noc,games,participated in same year,played in same city,played same sport,same event of sport and get same medal will considered duplicates
    #  
    if year=='overall' and country=='overall':
        temp_df=medal_df

    if year =='overall' and country !='overall':# we have to print the medal of specific country for every year
        flag=1
        temp_df=medal_df[medal_df['region']==country]

    if year !='overall' and country=='overall':# means we have to print the medals of country for every year
        temp_df=medal_df[medal_df['Year']==int(year)]

    if year !='overall' and country !='overall':## means we have to print medal of specific country for specific year
        temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]

    if flag==1:
        x = temp_df.groupby('Year')[['Gold', 'Bronze', 'Silver']].sum().sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region')[['Gold', 'Bronze', 'Silver']].sum().sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def data_over_time(df,col):

    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    # if 2 rows having same year and same column name will be considered as duplicates

    if col=='region':
        data_over_time.rename(columns={'index': 'Edition', 'Year': 'Nations over time'}, inplace=True)
    if col=='Event':
        data_over_time.rename(columns={'index': 'Edition', 'Year': 'Events over time'}, inplace=True)
    if col=='Name':
        data_over_time.rename(columns={'index': 'Edition', 'Year': 'Atheletes over time'}, inplace=True)


    return data_over_time

def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])# dropping columns having null values in medals

    if sport!='overall':
        temp_df=temp_df[temp_df['Sport']==sport]


    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left',suffixes=('','_drop'))[['index','Name','Sport','region']].drop_duplicates('index')
    
    x.rename(columns={'index': 'Name', 'Name': 'Medals'}, inplace=True)
    return x

def country_wise_medal_tally_per_year(df,region):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp_df=temp_df[temp_df['region']==region]
    temp_df=temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().reset_index()
    temp_df['total medal']=temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df.drop(columns=['Gold','Bronze','Silver'],inplace=True)
    return temp_df

def country_event_heatmap(df,region):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp_df=temp_df[temp_df['region']==region]
    k=temp_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
    return k 

def country_top_performer(df,region,sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport=='overall':
        temp_df=temp_df[temp_df['region']==region]
    if sport!='overall':
        temp_df=temp_df[(temp_df['region']==region) & (temp_df['Sport']==sport)]

    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left',suffixes=('','_drop'))[['index','Name','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name': 'Medals'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


    






        


