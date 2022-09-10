import pandas as pd

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

def preprocess():
    global df,region_df
    df=df[df['Season']=='Summer']
    df=df.merge(region_df,on='NOC',how='left',suffixes=('','_drop'))
    for col in df.columns:
        if 'drop' in col:
            df.drop(columns=[col],axis=1,inplace=True)
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df