# Library import
import datetime as dt
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf
from prophet import Prophet

# Page configuration
st.set_page_config(
    page_title='Stock dashboard',
    page_icon=':money_with_wings:'
    )
st.title('Stock prices forecasting')

st.sidebar.subheader('Ticker query parameters')
# Ticker sidebar
with open('ticker_symbols.txt', 'r') as fp:
    ticker_list = fp.read().split('\n')
    
ticker_selection = st.sidebar.selectbox(label='Stock ticker', options=ticker_list, index=ticker_list.index('AAPL'))
period_list = ['6mo', '1y', '2y', '5y', '10y', 'max']
period_selection = st.sidebar.selectbox(label='Period', options=period_list, index=period_list.index('2y'))

# Retrieving tickers data
ticker_data = yf.Ticker(ticker_selection)
ticker_df = ticker_data.history(period=period_selection)
ticker_df = ticker_df.rename_axis('Date').reset_index()
ticker_df['Date'] = ticker_df['Date'].dt.date

# Prophet sidebar
st.sidebar.subheader('Prophet parameters configuration')
horizon_selection = st.sidebar.slider('Forecasting horizon (days)', min_value=1, max_value=365, value=90)
growth_selection = st.sidebar.radio(label='Growth', options=['linear', 'logistic'])

if growth_selection == 'logistic':
    st.sidebar.info('Configure logistic growth saturation')
    floor = st.sidebar.slider('Floor (Close min percentage)', min_value=0.8, max_value=1.2)
    cap = st.sidebar.slider('Cap (Close max percentage)', min_value=0.8, max_value=1.2, value=1.2)
    floor_close = floor*min(ticker_df['Close'])
    cap_close = cap*max(ticker_df['Close'])
    if floor_close >= cap_close:
        st.sidebar.error('Cap must be higher than floor, switching to linear growth instead')
        growth_selection = 'linear'
    else:
        ticker_df['floor']=floor_close
        ticker_df['cap']=cap_close
seasonality_selection = st.sidebar.radio(label='Seasonality', options=['additive', 'multiplicative'])

with st.sidebar.expander('Seasonality components'):
    weekly_selection = st.checkbox('Weekly', value=True)
    monthly_selection = st.checkbox('Monthly')
    yearly_selection = st.checkbox('Yearly', value=True)
    
with open('holiday_countries.txt', 'r') as fp:
    holiday_country_list = fp.read().split('\n')
    holiday_country_list.insert(0, 'None')
holiday_country_selection = st.sidebar.selectbox(label="Holiday country", options=holiday_country_list)
changepoint_scale_selection = st.sidebar.slider('Changepoint prior scale (trend flexibility)', min_value=0.01, max_value=0.5, value=0.05)
seasonality_scale_selection = st.sidebar.slider('Seasonality prior scale (seasonality flexibility)', min_value=0.1, max_value=5.0, value=1.0)

# Ticker information
logo_url = ticker_data.info['logo_url']
st.image(logo_url)
company_name = ticker_data.info['longName']
st.header(company_name)
company_summary = ticker_data.info['longBusinessSummary']
st.info(company_summary)

st.header('Ticker data')
# Ticker data
var_list = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
st.dataframe(ticker_df[var_list])

st.header('Forecasting')
# Prophet model fitting
with st.spinner('Model fitting..'):
    prophet_df = ticker_df.rename(columns={'Date': 'ds', 'Close': 'y'})
    model = Prophet(
        seasonality_mode=seasonality_selection,
        weekly_seasonality=weekly_selection,
        yearly_seasonality=yearly_selection,
        growth=growth_selection,
        changepoint_prior_scale=changepoint_scale_selection
        )
    if holiday_country_selection != 'None':
        model.add_country_holidays(country_name=holiday_country_selection)      
    if monthly_selection:
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    model.fit(prophet_df)

# Prophet model forecasting
with st.spinner('Making predictions..'):
    future = model.make_future_dataframe(periods=horizon_selection, freq='D')
    if growth_selection == 'logistic':
        future['floor'] = floor_close
        future['cap'] = cap_close
    forecast = model.predict(future)

# Prophet forecast plot
fig = px.scatter(prophet_df, x='ds', y='y', labels={'ds': 'Day', 'y': 'Close'})
fig.add_scatter(x=forecast['ds'], y=forecast['yhat'], name='yhat')
fig.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='yhat_lower')
fig.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='yhat_upper')
st.plotly_chart(fig)
