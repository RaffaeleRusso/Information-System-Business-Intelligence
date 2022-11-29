## Importing libraries
import pandas as pd # https://pandas.pydata.org/docs/
import plotly_express as px # https://plotly.com/python-api-reference/index.html
import streamlit as st # https://docs.streamlit.io/

### Setting up webpage attributes
st.set_page_config(
    page_title="Studio IMDb",
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
df["Runtime"] = df["Runtime"].str.extract('(\d+)').astype(int)



# CALCOLO SIDEBAR
list_genre= []
for row in df['Genre']:
    for genre in row.split(','):
    #print(e.replace(" ",""))
        list_genre.append(genre.replace(" ",""))
set_genre =set(list_genre)

# NOME SIDEBAR
st.sidebar.header("Filters")

# SCELTA NOME FILM E ATTORI
name = st.sidebar.text_input('Film name')
Attore = st.sidebar.text_input('Actor name')

# SCELTA VALORI MIN E MAX
min_date= st.sidebar.slider('Min year',min(df["Released_Year"]),max(df["Released_Year"]))
max_date=st.sidebar.slider('Max year',min(df["Released_Year"]),max(df["Released_Year"]),value=max(df["Released_Year"]))

min_imdb= st.sidebar.slider('Min IMDb Rating',min(df["IMDB_Rating"]),max(df["IMDB_Rating"]))
min_meta=st.sidebar.slider('Min Metascore',min(df["Meta_score"]),max(df["Meta_score"]))

min_duration=st.sidebar.slider('Min Runtime',min(df['Runtime']),max(df["Runtime"]))


df_gross_min = df['Gross'].min()
df_gross_max = df['Gross'].max()

gross_th=st.sidebar.slider('Min grossing (bil)',df_gross_min,df_gross_max,0.00001)



# SCELTA generi
states = st.sidebar.multiselect(
    "Genres",
    options=set_genre
)

# SCELTA tipo genere
tipo_genere=st.sidebar.radio('Genre',('Single', 'Multi'))

# FUNZ ricerca genere
def search_genre(df,states,tipo_genere):
    fine=[] #
    tmp=[] #
    if tipo_genere=='Multi': # se devo prendere piu valore
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
df_filtered = df
df_filtered = df[
    (df["Released_Year"] >= min_date) &
    (df["Released_Year"] <= max_date) & 
    (df["Series_Title"].str.contains(name)) &
    (df["IMDB_Rating"]>=min_imdb) & 
    (df["Meta_score"]>=min_meta) &
    (search_genre(df,states,tipo_genere))&
    (df["Star1"].str.contains(Attore,case=False) | df["Star2"].str.contains(Attore,case=False)
     | df["Star3"].str.contains(Attore,case=False) | df["Star4"].str.contains(Attore,case=False)) 
     & (df['Gross']>=gross_th)
     & (df['Runtime']>=min_duration)
     ]
    

#TITLE
st.title("Dataset IMDb :film_frames:")

#KPI 
avg_IMDB_Rating = df_filtered["IMDB_Rating"].mean()
avg_Metacritic =df_filtered["Meta_score"].mean()
avg_grossing =df_filtered["Gross"].mean()

avg_IMDB_Rating_df = df["IMDB_Rating"].mean()
avg_Metacritic_df = df["Meta_score"].mean()
avg_grossing_df = df["Gross"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Average IMDb Rating",round(avg_IMDB_Rating,2),delta=avg_IMDB_Rating-avg_IMDB_Rating_df)
col2.metric("Average Metascore",round(avg_Metacritic,2),delta=avg_Metacritic-avg_Metacritic_df)
col3.metric("Average grossing (bil)", round(avg_grossing,2),delta=avg_grossing-avg_grossing_df)   



#Piecharts
genere_one=[]
for i,k in df_filtered.iterrows():
    k["Genre"]=k["Genre"].split(",")
    genere_one.append(k["Genre"][0])
df_filtered['genre_one']=genere_one



if df_filtered.shape[0]==0:
    st.warning("0 Movies found")#,icon="🚨")
else:
    ### Showing dataset
    st.success(str(df_filtered.shape[0])+" Movies found")
    with st.expander("Display movies"):
        st.dataframe(df_filtered)

    with st.expander("Display Charts"):
        col1_, col2_= st.columns(2)
        with col1_:
            st.text("Genre distribution")
            fig1 = px.pie(df_filtered,names='genre_one') 
            st.plotly_chart(fig1, use_container_width=True)

        with col2_:
            st.text("Gross distribution (bil) for genre")
            fig2 = px.pie(df_filtered,values='Gross',names='genre_one')
            st.plotly_chart(fig2, use_container_width=True)

        st.text("Histogram Genres")
        fig11 = px.histogram(df_filtered, x='genre_one',color="genre_one")
        st.plotly_chart(fig11, use_container_width=True)

        st.text("No of Votes")
        fig12 = px.histogram(df_filtered, x='No_of_Votes',color="genre_one")
        st.plotly_chart(fig12, use_container_width=True)
        col3_, col4_= st.columns(2)
        with col3_:
            st.text("IMDb Rating histogram")
            fig3 = px.histogram(df_filtered,x='IMDB_Rating',color=genere_one) 
            st.plotly_chart(fig3, use_container_width=True)
        with col4_:
            st.text("Metascore histogram")
            fig4 = px.histogram(df_filtered,x='Meta_score',color=genere_one) 
            st.plotly_chart(fig4, use_container_width=True)#,color_discrete_sequence = ['darkred'])
        col5_, col6_= st.columns(2)
        with col5_:
            st.text("Gross histogram")
            fig5 = px.histogram(df_filtered,x='Gross',color=genere_one) 
            st.plotly_chart(fig5, use_container_width=True)
        with col6_:
            st.text("Release Year")
            fig6 = px.histogram(df_filtered,x='Released_Year',color=genere_one) 
            st.plotly_chart(fig6, use_container_width=True)
        col7_, col8_= st.columns(2)
        with col7_:
            st.text("Runtime histogram")
            fig7 = px.histogram(df_filtered,x='Runtime',color=genere_one) 
            st.plotly_chart(fig7, use_container_width=True)
            
        with col8_:
            st.text("Scatter Runtime-IMDb Rating")
            fig8 = px.scatter(df_filtered, x="Runtime", y="IMDB_Rating",color=genere_one)
            st.plotly_chart(fig8, use_container_width=True)

        col9_, col10_= st.columns(2)
        with col9_:
            st.text("Scatter Gross-IMDb Rating")
            fig9 = px.scatter(df_filtered, x="Gross", y="IMDB_Rating",color=genere_one) 
            st.plotly_chart(fig9, use_container_width=True)
            
        with col10_:
            st.text("Scatter Gross-Metascore")
            fig10 = px.scatter(df_filtered, x="Gross", y="Meta_score",color=genere_one)
            st.plotly_chart(fig10, use_container_width=True)
        
       
            
            





