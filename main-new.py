import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import io

# Título do Dashboard
st.set_page_config(page_title="Dashboard de Análise Técnica e de Risco", layout="wide")
st.title("Análise Técnica e de Risco de Ativos")

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
ativos_selecionados = st.sidebar.multiselect("Escolha os ativos:", ativos_nomes, default=ativos_nomes)
data_inicio = st.sidebar.date_input("Data de início:", pd.to_datetime("2019-01-01"))
data_fim = st.sidebar.date_input("Data de fim:", pd.to_datetime("2024-12-31"))

# --- Carregamento de dados com yfinance ---
@st.cache_data
def carregar_dados(ativo_ticker):
    df = yf.download(ativo_ticker, start=data_inicio, end=data_fim, auto_adjust=False)
    df.reset_index(inplace=True)
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

    return df

# --- Função para salvar figura e exportar ---
def salvar_figura(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# --- Seção 1: Visão Geral ---
st.header("Visão Geral")
df_visao_geral = []
alertas = []
for nome in ativos_selecionados:
    ticker = ativos_disponiveis[nome]
    df = carregar_dados(ticker)
    media_return = df['Daily_Return'].mean()
    media_amp = df['Daily_Amplitude'].mean()
    vol = df['Volatilidade'].mean()
    volume_medio = df['Volume'].mean()
    preco_atual = df['Close'].iloc[-1]
    df_visao_geral.append([nome, preco_atual, media_return, media_amp, vol, volume_medio])

    # Geração de alerta com base em RSI
    rsi_atual = df['RSI'].iloc[-1]
    if rsi_atual > 70:
        alertas.append(f"🚨 {nome} está em zona de sobrecompra (RSI: {rsi_atual:.2f})")
    elif rsi_atual < 30:
        alertas.append(f"📉 {nome} está em zona de sobrevenda (RSI: {rsi_atual:.2f})")

df_resumo = pd.DataFrame(df_visao_geral, columns=["Ativo", "Preço Atual", "Retorno Médio", "Amplitude Média", "Volatilidade", "Volume Médio"])
st.dataframe(df_resumo.set_index("Ativo"))

if alertas:
    st.subheader("🔔 Alertas Técnicos Baseados em RSI")
    for alerta in alertas:
        st.warning(alerta)

# --- Seção 2: Análise Técnica ---
st.header("Análise Técnica")
for nome in ativos_selecionados:
    st.subheader(f"{nome} - Indicadores Técnicos")
    ticker = ativos_disponiveis[nome]
    df = carregar_dados(ticker)
    df['MA32'] = df['Close'].rolling(window=32).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    # Gráfico de preço e médias móveis
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['Date'], df['Close'], label='Close')
    ax.plot(df['Date'], df['MA32'], label='MA32')
    ax.plot(df['Date'], df['MA200'], label='MA200')
    ax.set_title(f"Preço e Médias Móveis - {nome}")
    ax.legend()
    st.pyplot(fig)
    st.download_button("📥 Baixar gráfico de preço", data=salvar_figura(fig), file_name=f"{nome}_preco.png")

    # RSI
    fig2, ax2 = plt.subplots(figsize=(10, 2))
    ax2.plot(df['Date'], df['RSI'], label='RSI', color='orange')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_title("Índice de Força Relativa (RSI)")
    st.pyplot(fig2)
    st.download_button("📥 Baixar gráfico RSI", data=salvar_figura(fig2), file_name=f"{nome}_rsi.png")

    # MACD
    fig3, ax3 = plt.subplots(figsize=(10, 2))
    ax3.plot(df['Date'], df['MACD'], label='MACD', color='blue')
    ax3.plot(df['Date'], df['Signal'], label='Signal', color='red')
    ax3.set_title("MACD e Linha de Sinal")
    ax3.legend()
    st.pyplot(fig3)
    st.download_button("📥 Baixar gráfico MACD", data=salvar_figura(fig3), file_name=f"{nome}_macd.png")

# --- Seção 3: Análise de Risco ---
st.header("Análise de Risco")
for nome in ativos_selecionados:
    st.subheader(f"{nome} - Volatilidade e Distribuição de Retornos")
    ticker = ativos_disponiveis[nome]
    df = carregar_dados(ticker)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Volatilidade'])
        ax.set_title("Volatilidade Histórica (Rolling 21 dias)")
        st.pyplot(fig)
        st.download_button("📥 Baixar gráfico de volatilidade", data=salvar_figura(fig), file_name=f"{nome}_volatilidade.png")

    with col2:
        fig, ax = plt.subplots()
        sns.histplot(df['Daily_Return'].dropna(), kde=True, bins=50, ax=ax)
        ax.set_title("Distribuição dos Retornos Diários")
        st.pyplot(fig)
        st.download_button("📥 Baixar histograma de retornos", data=salvar_figura(fig), file_name=f"{nome}_retornos.png")

# --- Seção 4: Correlação entre Ativos ---
st.header("Correlação entre Retornos")
retornos = {}
for nome in ativos_selecionados:
    ticker = ativos_disponiveis[nome]
    df = carregar_dados(ticker)
    retornos[nome] = df.set_index("Date")["Daily_Return"]

df_corr = pd.concat(retornos, axis=1).dropna().corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(df_corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Matriz de Correlação dos Retornos Diários")
st.pyplot(fig)
st.download_button("📥 Baixar heatmap de correlação", data=salvar_figura(fig), file_name="correlacao.png")

# --- Seção 5: Comparação Normalizada ---
st.header("Comparação de Retorno Acumulado (Normalizado)")
fig, ax = plt.subplots(figsize=(10, 5))
for nome in ativos_selecionados:
    ticker = ativos_disponiveis[nome]
    df = carregar_dados(ticker)
    base = df['Close'].iloc[0]
    ax.plot(df['Date'], df['Close'] / base, label=nome)
ax.set_title("Retorno Acumulado Normalizado")
ax.legend()
st.pyplot(fig)
st.download_button("📥 Baixar gráfico comparativo", data=salvar_figura(fig), file_name="comparacao_normalizada.png")

st.markdown("---")
st.caption("Desenvolvido para fins educacionais no Projeto de Análise Técnica e Risco de Ativos - 2025")
