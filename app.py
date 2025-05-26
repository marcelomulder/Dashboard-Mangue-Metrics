import streamlit as st
from config import ATIVOS_DISPONIVEIS, MA_PERIODOS
from dados import carregar_dados, filtrar_periodo
from indicadores import calcular_medias_moveis, calcular_rsi, detectar_cruzamentos, gerar_alertas
from visualizacao import gerar_grafico, exibir_metricas
from ui import sidebar, exibir_resumo_tendencias

def main():
    st.set_page_config(page_title="Mangue Metrics - Dashboard", layout="wide")
    # st.title("📊 Análise Técnica e de Risco de Ativos")

    ativo_padrao = "Bitcoin"
    df_ativo_padrao = carregar_dados(ATIVOS_DISPONIVEIS[ativo_padrao])
    ativo_escolhido, data_inicio, data_fim, mostrar_ma, mostrar_rsi, tipo_grafico, mostrar_cruzamentos = sidebar(ATIVOS_DISPONIVEIS, df_ativo_padrao)
    ticker = ATIVOS_DISPONIVEIS[ativo_escolhido]
    df = carregar_dados(ticker)

    df = calcular_medias_moveis(df, MA_PERIODOS)
    df = calcular_rsi(df)
    df_periodo = filtrar_periodo(df, data_inicio, data_fim)

    col1, col2 = st.columns([2.5, 1])
    with col1:
        st.subheader("Gráfico de Preço")
        cruzamentos = detectar_cruzamentos(df_periodo, MA_PERIODOS)
        fig = gerar_grafico(df_periodo, mostrar_ma, mostrar_rsi, MA_PERIODOS, tipo_grafico, cruzamentos, mostrar_cruzamentos)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        exibir_metricas(df_periodo)

    col_alertas, col_resumo = st.columns(2)
    alertas_rsi, alertas_cruz = gerar_alertas(df_periodo, MA_PERIODOS, cruzamentos)
    with col_alertas:
        st.subheader("🔔 Alertas Técnicos")
        st.markdown("**IFR (RSI):**")
        if alertas_rsi:
            for alerta in reversed(alertas_rsi):
                st.warning(alerta)
        else:
            st.info("Nenhum alerta recente de sobrecompra/sobrevenda.")

        st.markdown("**Médias Móveis:**")
        if alertas_cruz:
            for alerta in reversed(alertas_cruz):
                st.warning(alerta)
        else:
            st.info("Nenhum alerta de cruzamento recente.")

    with col_resumo:
        exibir_resumo_tendencias(df_periodo, MA_PERIODOS)

    st.caption("Desenvolvido pela Mangue Metrics - 2025")

if __name__ == "__main__":
    main()


