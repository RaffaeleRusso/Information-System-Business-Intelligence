import datetime
import pandas as pd # https://pandas.pydata.org/docs/
import plotly_express as px # https://plotly.com/python-api-reference/index.html
import streamlit as st # https://docs.streamlit.io/
import urllib

states= set(['Thriller'])#, 'Horror', 'Mystery', 'Drama', 'Animation', 'Adventure', 'Sport', 'Romance', 'Musical', 'History', 'Action', 'Fantasy', 'Film-Noir', 'War', 'Music', 'Western', 'Crime', 'Biography', 'Comedy', 'Sci-Fi', 'Family'])
states= set(['Action','Drama','Crime'])

local_filename = 'imdb_top_1000.csv'

def load_dataset():
    df = pd.read_csv(local_filename)
    return df

def prova2():
    fine=[]
    for i,k in df.head(4).iterrows():
        k["Genre"]=[z.strip() for z in k["Genre"].split(",")]
        enable=True
        for s in k["Genre"]:
            print(s, "\t",states,"\t", enable)
            for z in states:
                if s not in states or z not in k["Genre"] :
                    enable=False
        print(k["Genre"], "\t",enable,"\n\n")
        fine.append(enable)
    print(fine)

df = load_dataset()
prova2()