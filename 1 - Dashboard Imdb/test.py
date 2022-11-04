import datetime
import pandas as pd # https://pandas.pydata.org/docs/
import plotly_express as px # https://plotly.com/python-api-reference/index.html
import streamlit as st # https://docs.streamlit.io/
import urllib

states= set(['Thriller'])#, 'Horror', 'Mystery', 'Drama', 'Animation', 'Adventure', 'Sport', 'Romance', 'Musical', 'History', 'Action', 'Fantasy', 'Film-Noir', 'War', 'Music', 'Western', 'Crime', 'Biography', 'Comedy', 'Sci-Fi', 'Family'])
states= set(['Action','Drama','Crime'])

### Retrieving dataset
#Poster_Link,Series_Title,Released_Year,Certificate,Runtime,Genre,IMDB_Rating,Overview,Meta_score,Director,Star1,Star2,Star3,Star4,No_of_Votes,Gross
local_filename = 'imdb_top_1000.csv'

def load_dataset():
    df = pd.read_csv(local_filename)
    return df

def pulizia_df(df):
    for i,k in df.iterrows():
        k["Gross"]=k["Gross"].replace(",","")
    
    return df

def stampa():
    for i,k in df.iterrows():
        print(k["Gross"])






def search_genre(df,states):
    list=[]
    tmp=[]
    for s in states:
        #df = df.loc[df["Genre"].str.contains(s, case=False)]
        tmp=df["Genre"].str.contains(s, case=False)
        print(df)
        list=list & tmp
    print(list)









df=load_dataset()
set_gen=set([])
#print(df["Genre"])
for i,k in df.iterrows():
    k["Genre"]=k["Genre"].split(",")
    for i in k["Genre"]:
        if i not in set_gen:
            set_gen.add(i.strip())
    #print(k["Genre"])

#df = df.loc[df["Genre"].str.contains("Drama", case=False)]


def prova12():
    fine=[]
    tmp=[]
    for i,k in df.iterrows():
        k["Genre"]=k["Genre"].split(",")
        enable=True
        for i in k["Genre"]:
            if i not in states:
                enable=False
        fine.append(enable)
    fine = pd.DataFrame (fine, columns = ['Condition'])
    print(fine)

def prova2():
    for i,k in df.iterrows():
        k["Genre"]=k["Genre"].split(",")
        enable=True
        for i in k["Genre"]:
            if i not in states:
                enable=False
        fine.append(enable)
    return fine


fine=[]
tmp=[]
for s in states:
    #df = df.loc[df["Genre"].str.contains(s, case=False)]
    tmp=df["Genre"].str.contains(s, case=False)
    if s==list(states)[0]:
        fine=tmp
    #fine.iloc[:,1]=fine.iloc[:,1] & tmp.iloc[:,1]
    fine=fine & tmp

prova2()

#df=search_genre(df,states)

    #set_gen.add(genere)

    
