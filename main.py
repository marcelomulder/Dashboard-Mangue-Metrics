# Importar as bibliotecas necessárias
import streamlit as st
import pandas as pd
import yfinance as yf

# Criar funções de carregamento de dados
    # Cotações do Bitcoin - 2014 a 2025
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacao_acao = dados_acao.history(period="1d", start="2010-01-01", end="2025-04-30")
    cotacao_acao = cotacao_acao["Close"]
    return cotacao_acao

acoes = ["SPY", "EWZ", "IAU", "BTC-USD", "SOL-USD", "XPR-USD"]
dados = carregar_dados(acoes)

# Criar a interface com o streamlit
st.write(""" 
# Visualizador de Preço de Criptos e ETFs
""")

# Preparar as visualizaçõe
st.sidebar.header("Filtros")

# filtro de acoes
lista_acoes = st.sidebar.multiselect("Escolha as ações para vizualizar: ", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

# filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período", min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

# Criar o gráfico
st.line_chart(dados)