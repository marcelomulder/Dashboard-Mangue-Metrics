import streamlit as st
import pandas as pd
import plotly.express as px
from src.visualizacao import grafico_waterfall_carteira_percentual


def rodape_mangue_metrics():
    st.markdown("""
        <div style='text-align: center; color: #bbb; font-size: 0.9em; margin-top: 100px;'>
            © 2025 Mangue Metrics - Versão 0.5
        </div>
    """, unsafe_allow_html=True)

# analise-ativo.py -------------------------------------
def sidebar(ativos_disponiveis, df_ativo):
    
    st.sidebar.image("images/logo-dark.png", use_container_width=True, width=1)

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
    st.sidebar.markdown("---")
    mostrar_ma = st.sidebar.checkbox("Mostrar Médias Móveis", value=False)
    mostrar_rsi = st.sidebar.checkbox("Mostrar RSI ao invés de Volume", value=False)
    mostrar_cruzamentos = st.sidebar.checkbox("Mostrar Cruzamentos no Gráfico", value=False)

    return ativo_escolhido, data_inicio, data_fim, mostrar_ma, mostrar_rsi, tipo_grafico, mostrar_cruzamentos

def exibir_resumo_tendencias(df_periodo, ma_periodos):
    #st.subheader("📌 Resumo das Tendências")
    if 'RSI' in df_periodo.columns and not df_periodo['RSI'].isnull().all():
        ultimo_rsi = df_periodo['RSI'].iloc[-1]
        st.html('<span class="left_indicator"></span>')
        st.write(f"**IFR Atual:** {ultimo_rsi:.2f}")

    if all(f"MA{p}" in df_periodo.columns for p in ma_periodos):
        ultima_ma_curta = df_periodo[f"MA{ma_periodos[0]}"]
        ultima_ma_longa = df_periodo[f"MA{ma_periodos[1]}"]

        if not ultima_ma_curta.isnull().all() and not ultima_ma_longa.isnull().all():
            # st.write(f"**Última MA {ma_periodos[0]} dias:** {ultima_ma_curta.dropna().iloc[-1]:.2f}")
            # st.write(f"**Última MA {ma_periodos[1]} dias:** {ultima_ma_longa.dropna().iloc[-1]:.2f}")

            if ultima_ma_curta.dropna().iloc[-1] > ultima_ma_longa.dropna().iloc[-1]:
                st.html('<span class="left_indicator"></span>')
                st.success("Tendência de Alta: MA curta acima da MA longa")

            else:
                st.html('<span class="left_indicator"></span>')
                st.error("Tendência de Baixa: MA curta abaixo da MA longa")


# comparativo.py -------------------------------------
def highlight_carteira(s):
    return ['background-color: #222; color: #fff' if s.name == 'Carteira' else '' for _ in s]

def moeda(valor):
    return f"${valor:,.2f}"

def percentual(valor):
    return f"{valor:,.2f}"

def exibir_resultado_carteira(
    ativos_com_dados, valores_iniciais_ativos, df_valor, 
    valor_inicial, pesos, total
):
    if total == 100:
        labels = list(pesos.keys())
        values = list(pesos.values())
        resumo = {}
        for ativo in ativos_com_dados:
            valor_inicial_ativo = valores_iniciais_ativos[ativo]
            valor_final_ativo = df_valor[ativo].iloc[-1]
            variacao_ativo = (valor_final_ativo / valor_inicial_ativo - 1) * 100
            resumo[ativo] = {
                'Valor Inicial': valor_inicial_ativo,
                'Valor Final': valor_final_ativo,
                'Variação (%)': variacao_ativo
            }
        resumo['Carteira'] = {
            'Valor Inicial': valor_inicial,
            'Valor Final': df_valor['Carteira'].iloc[-1],
            'Variação (%)': (df_valor['Carteira'].iloc[-1] / valor_inicial - 1) * 100
        }
        resumo_df = pd.DataFrame(resumo).T.round(2)
        resumo_df['variacao_float'] = pd.to_numeric(resumo_df['Variação (%)'], errors='coerce')
        resumo_df['Valor Inicial'] = resumo_df['Valor Inicial'].apply(moeda)
        resumo_df['Valor Final'] = resumo_df['Valor Final'].apply(moeda)
        resumo_df['Variação (%)'] = resumo_df['Variação (%)'].apply(percentual)

        # Início da área da tabela de desempenho e cards de melhor e pior desempenho
        col_esq, col_tab, col_dir = st.columns([0.05, 2, 0.9])

        with col_tab:
            st.html('<span class="graph_indicator"></span>')
            st.markdown("#### Desempenho dos Ativos e da Carteira")
            st.dataframe(resumo_df.drop(columns=['variacao_float']).style.apply(highlight_carteira, axis=1), height=250)
            st.write("")
            

        # Melhor e pior desempenho - visual na lateral direita
        with col_dir:
            st.html('<span class="graph_indicator"></span>')
            st.markdown("#### Destaques")
            st.write("")
            st.write("")
            if len(ativos_com_dados) > 1:
                ativos_only = [a for a in resumo_df.index if a != "Carteira"]
                melhor = resumo_df.loc[ativos_only, 'variacao_float'].idxmax()
                pior = resumo_df.loc[ativos_only, 'variacao_float'].idxmin()
                # Card Melhor Desempenho (dark compact)
                st.markdown(
                    f"""
                    <div style='
                        background: #1e2a23;
                        border-left: 4px solid #3ec46d;
                        border-radius: 8px;
                        padding: 8px 12px 8px 12px;
                        margin-bottom: 12px;
                        text-align: left;
                        box-shadow: 0 1px 6px #212b26cc;'>
                        <div style='font-size:1.25em; display:inline-block; margin-right:6px;'>🏆</div>
                        <span style='font-size:1.08em; font-weight:600; color:#c6f7d0;'>{melhor}</span>
                        <span style='font-size:1em; color:#fff; margin-left:6px;'>
                            <b>{resumo_df.loc[melhor, 'Variação (%)']}%</b>
                        </span>
                        <div style='font-size:0.92em; color:#82c999;'>Melhor desempenho</div>
                    </div>
                    """, unsafe_allow_html=True
                )
                # Card Pior Desempenho (dark compact)
                st.markdown(
                    f"""
                    <div style='
                        background: #291d1d;
                        border-left: 4px solid #d34646;
                        border-radius: 8px;
                        padding: 8px 12px 8px 12px;
                        margin-bottom: 6px;
                        text-align: left;
                        box-shadow: 0 1px 6px #342222cc;'>
                        <div style='font-size:1.25em; display:inline-block; margin-right:6px;'>⚠️</div>
                        <span style='font-size:1.08em; font-weight:600; color:#ffd2d2;'>{pior}</span>
                        <span style='font-size:1em; color:#fff; margin-left:6px;'>
                            <b>{resumo_df.loc[pior, 'Variação (%)']}%</b>
                        </span>
                        <div style='font-size:0.92em; color:#e08b8b;'>Pior desempenho</div>
                    </div>
                    """, unsafe_allow_html=True
                )
        
        # Fim da área da tabela de desempenho e cards de melhor e pior desempenho       
        

        # Início da área do gráfico em cascata e composição da carteira
        col0, col1, _, col2 = st.columns([0.05, 1.7, 0.1, 1.3])

        with col1:
            st.html('<span class="graph_indicator"></span>')
            waterfall_fig = grafico_waterfall_carteira_percentual(
                labels, valores_iniciais_ativos, resumo_df, df_valor, valor_inicial
            )
            st.plotly_chart(waterfall_fig, use_container_width=True)            
            # st.markdown(
            #     "<div style='text-align:center; color: #aaa; font-size: 0.95em;'>Gráfico cascata: contribuição percentual de cada ativo para o resultado da carteira</div>",
            #     unsafe_allow_html=True
            # )

        with col2:
            st.html('<span class="graph_indicator"></span>')
            st.markdown("#### Composição da Carteira (%)")
            pie_fig = px.pie(
                names=labels,
                values=values,
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            pie_fig.update_traces(
                textinfo='percent+label',
                textfont=dict(size=15, family="sans-serif"),
                marker=dict(line=dict(color='#222', width=0.5))
            )
            pie_fig.update_layout(
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=350
            )
            st.plotly_chart(pie_fig, use_container_width=True)
            st.markdown(
                "<div style='text-align:center; color: #aaa; font-size: 0.95em;'>Distribuição dos ativos escolhidos na carteira (%)</div>",
                unsafe_allow_html=True
            )
        # Fim da área do gráfico em cascata e composição da carteira
