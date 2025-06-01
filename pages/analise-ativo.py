import streamlit as st
from src.config import ATIVOS_DISPONIVEIS, MA_PERIODOS
from src.dados import carregar_dados, filtrar_periodo
from src.indicadores import calcular_medias_moveis, calcular_rsi, detectar_cruzamentos, gerar_alertas
from src.visualizacao import gerar_grafico, exibir_metricas
from src.ui import sidebar, exibir_resumo_tendencias
from src.widgets import tradingview_heatmap
from src.widgets import tradingview_ticker_tape
from src.ui import rodape_mangue_metrics
from src.widgets import tradingview_technical_analysis

def tooltip(texto, dica):
    return f"<span title='{dica}' style='text-decoration:underline dotted; cursor:help;'>{texto}</span>"

def main():
    st.set_page_config(page_title="Análise de Ativos", layout="wide")    
    st.html("styles.html")

    st.title("Análise e Tendência de Ativos")
    

    #Adiciona a fita de ativos no topo da página
    tradingview_ticker_tape(height=110, color_theme="dark")    

    ativo_padrao = "Bitcoin"    
    df_ativo_padrao = carregar_dados(ATIVOS_DISPONIVEIS[ativo_padrao])

    ativo_escolhido, data_inicio, data_fim, mostrar_ma, mostrar_rsi, tipo_grafico, mostrar_cruzamentos = sidebar(ATIVOS_DISPONIVEIS, df_ativo_padrao)
    
    ticker = ATIVOS_DISPONIVEIS[ativo_escolhido]
    
    df = carregar_dados(ticker)
    
    df = calcular_medias_moveis(df, MA_PERIODOS)
    df = calcular_rsi(df)
    df_periodo = filtrar_periodo(df, data_inicio, data_fim)


    # Colunas do Gráfico e Metricas
    col1, col2 = st.columns([2.2, 1])
    with col1:
        st.html('<span class="graph_indicator"></span>')
        st.subheader(f"Acompanhamento da Variação de Preço — {ativo_escolhido}")
    
        if mostrar_ma:
            cruzamentos = detectar_cruzamentos(df_periodo, MA_PERIODOS)
        else:
            cruzamentos = []

        fig = gerar_grafico(
            df_periodo,
            mostrar_ma,
            mostrar_rsi,
            MA_PERIODOS,
            tipo_grafico,
            cruzamentos,
            mostrar_cruzamentos,
            # titulo=f"Gráfico de Preço — {ativo_escolhido}",
            y_label_preco="Preço (USD)",
            y_label_indicador="Volume" if not mostrar_rsi else "RSI"
        )
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.html('<span class="graph_indicator"></span>')        
        exibir_metricas(df_periodo)        
        exibir_resumo_tendencias(df_periodo, MA_PERIODOS)
    

    with st.expander("🔔 Alertas Técnicos", expanded=False):
    # Colunas do Alerta e Resumo
    
        col_alertas, _, col_resumo = st.columns([1, 0.1, 1])
        alertas_rsi, alertas_cruz = gerar_alertas(df_periodo, MA_PERIODOS, cruzamentos)
        
        with col_alertas:
            st.html('<span class="graph_indicator"></span>')
                                    
            st.markdown(
                f"**RSI** {tooltip(' **(IFR):**', 'Índice de Força Relativa: mede o momentum do ativo em relação ao seu histórico recente.')}.",
                unsafe_allow_html=True
            )
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
            st.html('<span class="graph_indicator"></span>')            
            st.markdown(
                f"**📊** {tooltip(' **Indicação - Análise Técnica:**', 'Informa a tendência do ativo no período escolhido utilizando 25 indicadores diferentes')}.",
                unsafe_allow_html=True
            )
            
            
            # Ajuste o símbolo conforme o ativo escolhido
            SYMBOLS_TV = {
                "Bitcoin": "BITSTAMP:BTCUSD",
                "Solana": "BITSTAMP:SOLUSD",
                "Ripple": "BITSTAMP:XRPUSD",
                "SPY": "AMEX:SPY",
                "EWZ": "AMEX:EWZ",
                "IAU": "AMEX:IAU"
            }
            tv_symbol = SYMBOLS_TV.get(ativo_escolhido, "BITSTAMP:BTCUSD")
            tradingview_technical_analysis(symbol=tv_symbol)


    # Widget de Heatmap
    with st.expander(":fire: Heatmap de Criptomoedas - Performance do Mês", expanded=False):
        tradingview_heatmap()

    # Rodapé
    rodape_mangue_metrics()

if __name__ == "__main__":
    main()


