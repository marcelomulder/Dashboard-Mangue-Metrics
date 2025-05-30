import pandas as pd
import yfinance as yf
import streamlit as st


# analise-ativo.py -------------------------------------
@st.cache_data(show_spinner="Carregando dados do ativo…")
def carregar_dados(ativo_ticker):
    ticker = yf.Tickers(ativo_ticker)
    df = ticker.tickers[ativo_ticker].history(period='max', auto_adjust=False)
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.tz_localize(None)
    return df

def filtrar_periodo(df, data_inicio, data_fim):
    return df[(df['Date'] >= data_inicio) & (df['Date'] <= data_fim)].copy()

# comparativo.py -------------------------------------

def carregar_dados_yf(tickers, periodo):
    data = yf.download(list(tickers.values()), period=periodo, auto_adjust=True)
    if isinstance(data.columns, pd.MultiIndex):
        close = data['Close']
        ticker_to_nome = {v: k for k, v in tickers.items()}
        close = close.rename(columns=ticker_to_nome)
    else:
        close = data[['Close']]
        close.columns = [list(tickers.keys())[0]]
    close = close.dropna()
    return close

def filtrar_ativos_disponiveis(df, ativos_escolhidos):
    return [a for a in ativos_escolhidos if a in df.columns and not df[a].dropna().empty]
