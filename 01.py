## Importing libraries
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
# column = Poster_Link,Series_Title,Released_Year,Certificate,Runtime,Genre,IMDB_Rating,Overview,Meta_score,Director,Star1,Star2,Star3,Star4,No_of_Votes,Gross
local_filename = 'imdb_top_1000.csv'

# set_genre= set(['Thriller', 'Horror', 'Mystery', 'Drama', 'Animation', 'Adventure', 'Sport', 'Romance', 'Musical', 'History', 'Action', 'Fantasy', 'Film-Noir', 'War', 'Music', 'Western', 'Crime', 'Biography', 'Comedy', 'Sci-Fi', 'Family'])

#cache
@st.cache(suppress_st_warning=True)

# alternative...
def det_genre():
    set_gen=set([])
    #print(df["Genre"])
    for i,k in df.iterrows():
        k["Genre"]=k["Genre"].split(",")
        for i in k["Genre"]:
            if i not in set_gen:
                set_gen.add(i.strip())
        #print(k["Genre"])

# FUNZ CARICAMENTO DATAFRAME
def load_dataset():
    df = pd.read_csv(local_filename) #leggp
    #df= df.fillna(value=0)
    df.dropna(axis=0,inplace=True)
    df.dropna(inplace=True) # delte arrow with element nan
    return df

def convert_gross(df):
    df['Gross']=df['Gross'].str.replace(',','',regex=True) # eliminate ',' in the gross
    #df=df.dropna(subset = ['Gross'])
    df['Gross']=df['Gross'].astype('int64')
    return df

# COLONNA con il primo genere
def select_first_genre(df):
    genere_one=[]
    for i,k in df.iterrows():
        k["Genre"]=k["Genre"].split(",")
        genere_one.append(k["Genre"][0])
    df['genre_one']=genere_one

#CARICAMENTO DATASET
df = load_dataset()
dftmp=df['Gross'].str.replace(',','').astype(float)/100000000
df['Gross']=dftmp



# CALCOLO SIDEBAR
list_genre= []
for row in df['Genre']:
    for genre in row.split(','):
    #print(e.replace(" ",""))
        list_genre.append(genre.replace(" ",""))
set_genre =set(list_genre)

# NOME SIDEBAR
st.sidebar.header("Filtri")

# SCELTA NOME FILM E ATTORI
name = st.sidebar.text_input('Nome Film')
Attore = st.sidebar.text_input('Nome Attore')

# SCELTA VALORI MIN E MAX
min_date= st.sidebar.slider('Anno min',min(df["Released_Year"]),max(df["Released_Year"]))
max_date=st.sidebar.slider('Anno max',min(df["Released_Year"]),max(df["Released_Year"]),value=max(df["Released_Year"]))

min_imdb= st.sidebar.slider('Min IMDB_Rating',min(df["IMDB_Rating"]),max(df["IMDB_Rating"]))
min_meta=st.sidebar.slider('Min Meta score',min(df["Meta_score"]),max(df["Meta_score"]))

df_gross_min = df['Gross'].min()
df_gross_max = df['Gross'].max()

gross_th=st.sidebar.slider('Min grossing * mld',df_gross_min,df_gross_max,0.001)



# SCELTA generi
states = st.sidebar.multiselect(
    "Generi",
    options=set_genre
)

# SCELTA tipo genere
tipo_genere=st.sidebar.radio('Genere specifico',('Specifico', 'Generale'))

# FUNZ ricerca genere
def search_genre(df,states,tipo_genere):
    fine=[] #
    tmp=[] #
    if tipo_genere=='Generale': # se devo prendere piu valore
        if(len(states)==0): # se non seleziono nessun genere torna tutti i valori
            fine=True
        else:
            for s in states: # per ogni genere che ho considerato
                tmp=df["Genre"].str.contains(s, case=False) # vero se è presente
                if s==list(states)[0]: # 
                    fine=tmp
                fine=fine | tmp
    else: # ciclo specifico
        # (drama,triller) -> (drama , triller , cook) -> False
        for i,k in df.iterrows(): # scorro il df
            k["Genre"]=[z.strip() for z in k["Genre"].split(",")] #
            enable=True
            for s in k["Genre"]: # scorri i generi nella riga
                for z in states: # scorri i generi selezionati
                    if s not in states or z not in k["Genre"] : # ogni elemento si deve trovare nel altro
                        enable=False
            fine.append(enable)
    return fine

#FILTER
df_filtered = df[
    (df["Released_Year"] >= min_date) &
    (df["Released_Year"] <= max_date) & df["Series_Title"].str.contains(name) &
    (df["IMDB_Rating"]>=min_imdb) & (df["Meta_score"]>=min_meta)  &
    (search_genre(df,states,tipo_genere)) &
    (df["Star1"].str.contains(Attore,case=False) | df["Star2"].str.contains(Attore,case=False)
     | df["Star3"].str.contains(Attore,case=False) | df["Star4"].str.contains(Attore,case=False)) 
     & (df['Gross']>gross_th)
    ]

#TITLE
st.title("Dataset Imdb :film_frames:")

#KPI 
avg_IMDB_Rating = df_filtered["IMDB_Rating"].mean()
avg_Metacritic =df_filtered["Meta_score"].mean()
avg_grossing =df_filtered["Gross"].mean()
col1, col2, col3 = st.columns(3)
col1.metric("Average IMDb rating",round(avg_IMDB_Rating,2))
col2.metric("Average Meta score",round(avg_Metacritic,2))
col3.metric("Average grossing * mld", round(avg_grossing,2))   

#Piecharts
genere_one=[]
for i,k in df_filtered.iterrows():
    k["Genre"]=k["Genre"].split(",")
    genere_one.append(k["Genre"][0])
df_filtered['genre_one']=genere_one


### Showing dataset
st.text("Selected movies")
st.dataframe(df_filtered)


col1_, col2_= st.columns(2)
with col1_:
    st.text("Genre distribution")
    fig1 = px.pie(df_filtered,names='genre_one') 
    st.plotly_chart(fig1, use_container_width=True)

with col2_:
    st.text("Gross distribution for genre")
    fig2 = px.pie(df_filtered,values='Gross',names='genre_one')
    st.plotly_chart(fig2, use_container_width=True)






