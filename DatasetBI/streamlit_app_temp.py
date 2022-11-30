import streamlit as st 
import plotly_express as px
import pandas as pd

st.set_page_config(
    page_title="Cows Dataset Insights",
    page_icon="🐄",
    layout="wide"
)
st.title("Cows Dataset 🐄🥛")


#df['Dates'] = pd.to_datetime(df['date']).dt.date
#df['Time'] = pd.to_datetime(df['date']).dt.time


df = pd.read_csv("MungituraEventi.csv")
gruppi = ['<scegli gruppo>']+ list(df["Gruppo"].unique())
tipi = ['<scegli tipo>']+ list(df["Tipo"].unique())
with st.sidebar:
    st.text("Filtri")
    numero_animale = st.text_input('Numero animale',df["Numero animale"].min(), df["Numero animale"].max(),1)
    gruppo = st.selectbox("Gruppo",gruppi)
    tipo = st.selectbox("Tipo",tipi)

mask_gruppo = True
mask_tipo = True
mask_animale = True

if numero_animale.isnumeric():
    mask_animale = (df["Numero animale"]== int(numero_animale))

if gruppo != '<scegli gruppo>':   
    mask_gruppo = (df['Gruppo']==gruppo)

if tipo != '<scegli tipo>':    
    mask_tipo = (df['Tipo']==tipo)

mask = mask_animale & mask_gruppo & mask_tipo
df_filtered = df[mask]

with st.expander("Eventi mungitura"):
    st.write(df)

with st.expander("Grafici"):
    col1,col2 = st.columns(2)
    with col1:
        st.text("Pie chart gruppi")
        fig0 = px.pie(df,names="Gruppo")
        st.plotly_chart(fig0,use_container_width=True)
    with col2:
        st.text("Pie chart tipi")
        fig1 = px.pie(df,names="Tipo")
        st.plotly_chart(fig1,use_container_width=True)



with st.expander("Eventi mungitura filtrati"):
    st.write(df_filtered)

with st.expander("Grafici filtrati"):
    st.text("Pie chart tipo")
    fig1_ = px.pie(df_filtered,names="Tipo")
    st.plotly_chart(fig1_,use_container_width=True)

    st.text("Pie chart utenti")
    fig2_ = px.pie(df_filtered,names="Utente")
    st.plotly_chart(fig2_,use_container_width=True)

