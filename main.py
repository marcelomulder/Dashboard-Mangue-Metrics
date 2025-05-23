import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

# --- Configuração da página ---
st.set_page_config(page_title="Dashboard de Análise Técnica e de Risco", layout="wide")
st.title("📊 Análise Técnica e de Risco de Ativos")

# --- Sidebar ---
st.sidebar.header("Filtros")
ativos_disponiveis = {
    "Bitcoin": "BTC-USD",
    "Ripple": "XRP-USD",
    "Solana": "SOL-USD",
    "SPY": "SPY",
    "EWZ": "EWZ",
    "IAU": "IAU"
}
ativos_nomes = list(ativos_disponiveis.keys())
ativos_selecionados = st.sidebar.multiselect("Escolha os ativos:", ativos_nomes, default=["Bitcoin"])
data_inicio = st.sidebar.date_input("Data de início:", pd.to_datetime("2019-01-01"))
data_fim = st.sidebar.date_input("Data de fim:", pd.to_datetime("2024-12-31"))

# --- Função para carregar dados ---
@st.cache_data
def carregar_dados(ativo_ticker, data_inicio, data_fim):
    df = yf.download(ativo_ticker, start=data_inicio, end=data_fim, auto_adjust=False)

    if df.empty:
        return pd.DataFrame()

    df.reset_index(inplace=True)

    # Simplifica colunas se for MultiIndex ou tiver sufixos
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df.columns = [col.split('_')[0] if '_' in col else col for col in df.columns]

    # Cálculos
    df['Daily_Return'] = (df['Close'] - df['Open']) / df['Open']
    df['Daily_Amplitude'] = df['High'] - df['Low']
    df['Volatilidade'] = df['Daily_Return'].rolling(window=21).std()

    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    roll_up = gain.rolling(window=14).mean()
    roll_down = loss.rolling(window=14).mean()
    rs = roll_up / roll_down
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    df['MA32'] = df['Close'].rolling(window=32).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    return df

# --- Dashboard ---
for nome in ativos_selecionados:
    with st.expander(f"🔍 {nome} - Análise Completa", expanded=False):
        df = carregar_dados(ativos_disponiveis[nome], data_inicio, data_fim)

        if df.empty:
            st.warning(f"Nenhum dado encontrado para {nome} no período selecionado.")
            continue

        # Gráfico de preço com médias móveis
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
        fig_price.add_trace(go.Scatter(x=df['Date'], y=df['MA32'], mode='lines', name='MA32'))
        fig_price.add_trace(go.Scatter(x=df['Date'], y=df['MA200'], mode='lines', name='MA200'))
        fig_price.update_layout(title=f'{nome} - Preço e Médias Móveis', xaxis_title='Data', yaxis_title='Preço')
        st.plotly_chart(fig_price, use_container_width=True)

        # Gráfico RSI
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI', line=dict(color='orange')))
        fig_rsi.add_shape(type="line", x0=df['Date'].min(), x1=df['Date'].max(), y0=70, y1=70,
                          line=dict(dash="dash", color="red"))
        fig_rsi.add_shape(type="line", x0=df['Date'].min(), x1=df['Date'].max(), y0=30, y1=30,
                          line=dict(dash="dash", color="green"))
        fig_rsi.update_layout(title='RSI (Índice de Força Relativa)', xaxis_title='Data', yaxis_title='RSI')
        st.plotly_chart(fig_rsi, use_container_width=True)

        # Gráfico MACD
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name='MACD', line=dict(color='blue')))
        fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['Signal'], name='Signal', line=dict(color='red')))
        fig_macd.update_layout(title='MACD e Linha de Sinal', xaxis_title='Data', yaxis_title='MACD')
        st.plotly_chart(fig_macd, use_container_width=True)

        # Gráfico de volatilidade
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(x=df['Date'], y=df['Volatilidade'], mode='lines', name='Volatilidade'))
        fig_vol.update_layout(title='Volatilidade Histórica (21 dias)', xaxis_title='Data', yaxis_title='Volatilidade')
        st.plotly_chart(fig_vol, use_container_width=True)

        # Histograma de retornos
        fig_hist = px.histogram(df, x='Daily_Return', nbins=50, title='Distribuição dos Retornos Diários')
        st.plotly_chart(fig_hist, use_container_width=True)

# --- Comparação Normalizada ---
with st.expander("📈 Comparação de Retorno Acumulado (Normalizado)", expanded=False):
    fig_norm = go.Figure()
    for nome in ativos_selecionados:
        df = carregar_dados(ativos_disponiveis[nome], data_inicio, data_fim)
        if df.empty:
            continue
        base = df['Close'].iloc[0]
        fig_norm.add_trace(go.Scatter(x=df['Date'], y=df['Close'] / base, mode='lines', name=nome))
    fig_norm.update_layout(title='Retorno Acumulado Normalizado', xaxis_title='Data', yaxis_title='Retorno')
    st.plotly_chart(fig_norm, use_container_width=True)

# --- Correlação entre Retornos ---
with st.expander("🔗 Matriz de Correlação dos Retornos", expanded=False):
    retornos = {}
    for nome in ativos_selecionados:
        df = carregar_dados(ativos_disponiveis[nome], data_inicio, data_fim)
        if df.empty:
            continue
        retornos[nome] = df.set_index("Date")["Daily_Return"]
    
    if retornos:
        df_corr = pd.concat(retornos, axis=1).dropna().corr()
        fig_corr = px.imshow(df_corr, color_continuous_scale="RdBu_r", aspect="auto")
        fig_corr.update_layout(title="Correlação entre Retornos Diários")
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("Sem dados suficientes para calcular correlação.")

st.markdown("---")
st.caption("Desenvolvido para fins educacionais no Projeto de Análise Técnica e Risco de Ativos - 2025")

