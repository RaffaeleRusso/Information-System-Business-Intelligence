### Importing libraries
import datetime
from numpy import empty, true_divide
import pandas as pd # https://pandas.pydata.org/docs/
import plotly_express as px # https://plotly.com/python-api-reference/index.html
import streamlit as st # https://docs.streamlit.io/
import urllib


### Setting up webpage attributes
st.set_page_config(
    page_title="Studio Imdb",
    page_icon=":film_frames:",
    layout="wide"
)

### Retrieving dataset
#Poster_Link,Series_Title,Released_Year,Certificate,Runtime,Genre,IMDB_Rating,Overview,Meta_score,Director,Star1,Star2,Star3,Star4,No_of_Votes,Gross
local_filename = 'imdb_top_1000.csv'
set_genre= set(['Thriller', 'Horror', 'Mystery', 'Drama', 'Animation', 'Adventure', 'Sport', 'Romance', 'Musical', 'History', 'Action', 'Fantasy', 'Film-Noir', 'War', 'Music', 'Western', 'Crime', 'Biography', 'Comedy', 'Sci-Fi', 'Family'])

@st.cache(suppress_st_warning=True)


def det_genre():
    set_gen=set([])
    #print(df["Genre"])
    for i,k in df.iterrows():
        k["Genre"]=k["Genre"].split(",")
        for i in k["Genre"]:
            if i not in set_gen:
                set_gen.add(i.strip())
        print(k["Genre"])

def load_dataset():
    df = pd.read_csv(local_filename)
    df= df.fillna(value=0)
    df['Gross']=df['Gross'].replace([','],'',inplace=True)

    return df

df = load_dataset()
df = df.dropna(axis=1)

st.sidebar.header("Filtri")

name = st.sidebar.text_input('Nome Film')
Attore = st.sidebar.text_input('Nome Attore')

#Poster_Link,Series_Title,Released_Year,Certificate,Runtime,Genre,IMDB_Rating,Overview,Meta_score,Director,Star1,Star2,Star3,Star4,No_of_Votes,Gross
min_date= st.sidebar.slider('Anno min',min(df["Released_Year"]),max(df["Released_Year"]))
max_date=st.sidebar.slider('Anno max',min(df["Released_Year"]),max(df["Released_Year"]),value=max(df["Released_Year"]))

min_imdb= st.sidebar.slider('Min IMDB_Rating',min(df["IMDB_Rating"]),max(df["IMDB_Rating"]))
min_meta=st.sidebar.slider('Mix Meta score',min(df["Meta_score"]),max(df["Meta_score"]))

states = st.sidebar.multiselect(
    "Generi",
    options=set_genre
)

tipo_genere=st.sidebar.radio('Genere specifico',('Specifico', 'Generale'))

def search_genre(df,states,tipo_genere):
    fine=[]
    tmp=[]
    if tipo_genere=='Generale':
        for s in states:
            tmp=df["Genre"].str.contains(s, case=False)
            if s==list(states)[0]:
                fine=tmp
            fine=fine & tmp
    else:
        for i,k in df.iterrows():
            k["Genre"]=[z.strip() for z in k["Genre"].split(",")]
            enable=True
            for s in k["Genre"]:
                for z in states:
                    if s not in states or z not in k["Genre"] :
                        enable=False
            fine.append(enable)
    return fine
    
    

df_filtered = df[
    (df["Released_Year"] >= min_date) &
    (df["Released_Year"] <= max_date) & df["Series_Title"].str.contains(name) &
    (df["IMDB_Rating"]>=min_imdb) & (df["Meta_score"]>=min_meta) &
    (search_genre(df,states,tipo_genere)) &
    (df["Star1"].str.contains(Attore,case=False) | df["Star2"].str.contains(Attore,case=False)
     | df["Star3"].str.contains(Attore,case=False) | df["Star4"].str.contains(Attore,case=False))
    ]


### Filter sidebar



st.title("Dataset Imdb :film_frames:")

### Showing dataset
st.dataframe(df_filtered)



