import pandas as pd
import yfinance as yf
import streamlit as st

@st.cache_data(show_spinner="Carregando dados do ativo…")
def carregar_dados(ativo_ticker):
    ticker = yf.Tickers(ativo_ticker)
    df = ticker.tickers[ativo_ticker].history(period='max', auto_adjust=False)
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.tz_localize(None)
    return df

def filtrar_periodo(df, data_inicio, data_fim):
    return df[(df['Date'] >= data_inicio) & (df['Date'] <= data_fim)].copy()
