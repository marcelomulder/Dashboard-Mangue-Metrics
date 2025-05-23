import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def carregar_dados(ativo_ticker):
    ticker = yf.Tickers(ativo_ticker)
    df = ticker.tickers[ativo_ticker].history(period='max', auto_adjust=False)
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.tz_localize(None)
    return df

def gerar_grafico(df, mostrar_ma, mostrar_rsi, ma_periodos):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
    )

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )

    # Médias móveis
    if mostrar_ma:
        for periodo in ma_periodos:
            df[f"MA{periodo}"] = df['Close'].rolling(window=periodo).mean()
            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df[f"MA{periodo}"],
                    mode='lines',
                    name=f'MA {periodo}'
                ),
                row=1, col=1
            )

    # RSI ou Volume
    if mostrar_rsi:
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        roll_up = gain.rolling(window=14).mean()
        roll_down = loss.rolling(window=14).mean()
        rs = roll_up / roll_down
        df['RSI'] = 100 - (100 / (1 + rs))

        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['RSI'],
                mode='lines',
                name='RSI'
            ),
            row=2, col=1
        )
    else:
        fig.add_trace(
            go.Bar(
                x=df['Date'],
                y=df['Volume'],
                name='Volume',
                marker_color='lightblue'
            ),
            row=2, col=1
        )

    fig.update_layout(
        height=500,
        font_size=16,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        margin=dict(l=50, r=50, t=50, b=50, pad=0)
    )

    return fig

def exibir_metricas(df_periodo):
    st.subheader("Period Metrics")
    st.metric(label="Lowest Volume Day Trade", value=f"{df_periodo['Volume'].min():,.0f}")
    st.metric(label="Highest Volume Day Trade", value=f"{df_periodo['Volume'].max():,.0f}")
    st.metric(label="Lowest Close Price", value=f"${df_periodo['Close'].min():.2f}")
    st.metric(label="Highest Close Price", value=f"${df_periodo['Close'].max():.2f}")
    st.metric(label="Average Daily Volume", value=f"{df_periodo['Volume'].mean():,.0f}")
    st.metric(label="Current Market Cap", value="N/A")

def sidebar(ativos_disponiveis):
    # Ativo a escolher
    ativo_escolhido = st.sidebar.selectbox("Escolha o ativo:", list(ativos_disponiveis.keys()), index=0)
    
    # Período a escolher
    periodo = st.sidebar.selectbox("Período", ["Último mês", "Último trimestre", "Último ano"])

    if periodo == "Último mês":
        data_inicio = pd.to_datetime("today") - pd.DateOffset(months=1)
    elif periodo == "Último trimestre":
        data_inicio = pd.to_datetime("today") - pd.DateOffset(months=3)
    else:
        data_inicio = pd.to_datetime("today") - pd.DateOffset(years=1)

    data_fim = pd.to_datetime("today")

    mostrar_ma = st.sidebar.checkbox("Mostrar Médias Móveis", value=True)
    mostrar_rsi = st.sidebar.checkbox("Mostrar RSI ao invés de Volume", value=False)

    return ativo_escolhido, data_inicio, data_fim, mostrar_ma, mostrar_rsi

def filtrar_periodo(df, data_inicio, data_fim):
    return df[(df['Date'] >= data_inicio) & (df['Date'] <= data_fim)].copy()

def main():
    st.set_page_config(page_title="Dashboard de Análise Técnica e de Risco", layout="wide")
    st.title("📊 Análise Técnica e de Risco de Ativos")

    ativos_disponiveis = {
        "Bitcoin": "BTC-USD",
        "Ripple": "XRP-USD",
        "Solana": "SOL-USD",
        "SPY": "SPY",
        "EWZ": "EWZ",
        "IAU": "IAU"
    }

    ativo_escolhido, data_inicio, data_fim, mostrar_ma, mostrar_rsi = sidebar(ativos_disponiveis)

    ma_periodos = [34, 80]

    ticker = ativos_disponiveis[ativo_escolhido]
    df = carregar_dados(ticker)

    col1, col2 = st.columns([2.5, 1])

    with col1:
        st.subheader("Stock Price Trends")
        df_periodo = filtrar_periodo(df, data_inicio, data_fim)

        fig = gerar_grafico(df_periodo, mostrar_ma, mostrar_rsi, ma_periodos)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        exibir_metricas(df_periodo)

    st.markdown("---")
    st.caption("Desenvolvido para fins educacionais no Projeto de Análise Técnica e Risco de Ativos - 2025")

if __name__ == "__main__":
    main()

