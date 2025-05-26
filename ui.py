import streamlit as st
import pandas as pd

def sidebar(ativos_disponiveis, df_ativo):
    ativo_escolhido = st.sidebar.selectbox("Escolha o ativo:", list(ativos_disponiveis.keys()), index=0)

    periodos = ["Último mês", "Último trimestre", "Último ano", "Últimos 3 anos", "Últimos 5 anos", "Máximo"]
    periodo = st.sidebar.selectbox("Período", periodos, index=2)

    min_date = df_ativo['Date'].min()
    max_date = df_ativo['Date'].max()
    data_fim = st.session_state.get("today", pd.to_datetime("today"))
    if periodo == "Máximo":
        data_inicio = min_date
    elif periodo == "Último mês":
        data_inicio = data_fim - pd.DateOffset(months=1)
    elif periodo == "Último trimestre":
        data_inicio = data_fim - pd.DateOffset(months=3)
    elif periodo == "Últimos 3 anos":
        data_inicio = data_fim - pd.DateOffset(years=3)
    elif periodo == "Últimos 5 anos":
        data_inicio = data_fim - pd.DateOffset(years=5)
    else:
        data_inicio = data_fim - pd.DateOffset(years=1)
    if data_inicio < min_date:
        data_inicio = min_date
    if data_fim > max_date:
        data_fim = max_date

    tipo_grafico = st.sidebar.selectbox("Tipo de Gráfico", ["Linha", "Candlestick"], index=0)
    mostrar_ma = st.sidebar.checkbox("Mostrar Médias Móveis", value=False)
    mostrar_rsi = st.sidebar.checkbox("Mostrar RSI ao invés de Volume", value=False)
    mostrar_cruzamentos = st.sidebar.checkbox("Mostrar Cruzamentos no Gráfico", value=False)

    return ativo_escolhido, data_inicio, data_fim, mostrar_ma, mostrar_rsi, tipo_grafico, mostrar_cruzamentos

def exibir_resumo_tendencias(df_periodo, ma_periodos):
    st.subheader("📌 Resumo das Tendências")
    if 'RSI' in df_periodo.columns and not df_periodo['RSI'].isnull().all():
        ultimo_rsi = df_periodo['RSI'].iloc[-1]
        st.write(f"**RSI Atual:** {ultimo_rsi:.2f}")
    if all(f"MA{p}" in df_periodo.columns for p in ma_periodos):
        ultima_ma_curta = df_periodo[f"MA{ma_periodos[0]}"]
        ultima_ma_longa = df_periodo[f"MA{ma_periodos[1]}"]
        if not ultima_ma_curta.isnull().all() and not ultima_ma_longa.isnull().all():
            st.write(f"**Última MA {ma_periodos[0]} dias:** {ultima_ma_curta.dropna().iloc[-1]:.2f}")
            st.write(f"**Última MA {ma_periodos[1]} dias:** {ultima_ma_longa.dropna().iloc[-1]:.2f}")
            if ultima_ma_curta.dropna().iloc[-1] > ultima_ma_longa.dropna().iloc[-1]:
                st.success("Tendência de Alta: MA curta acima da MA longa")
            else:
                st.error("Tendência de Baixa: MA curta abaixo da MA longa")


