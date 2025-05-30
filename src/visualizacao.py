import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import plotly.express as px
import pandas as pd

# analise-ativo.py -------------------------------------
# Gráfico principal da aplicação

def gerar_grafico(
    df,
    mostrar_ma,
    mostrar_rsi,
    ma_periodos,
    tipo_grafico,
    cruzamentos=[],
    mostrar_cruzamentos=True,
    titulo="",
    y_label_preco="Preço",
    y_label_indicador="Volume/RSI"
):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "xy"}], [{"type": "scatter"}]]
    )

    # Gráfico de Preço (linha ou candlestick)
    if tipo_grafico == "Candlestick":
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
    else:
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Close'],
                mode='lines',
                name='Preço de Fechamento'
            ),
            row=1, col=1
        )

    # Médias móveis (se ativado)
    if mostrar_ma:
        for periodo in ma_periodos:
            mm_x = df['Date'][~df[f"MA{periodo}"].isna()]
            mm_y = df[f"MA{periodo}"].dropna()
            fig.add_trace(
                go.Scatter(
                    x=mm_x,
                    y=mm_y,
                    mode='lines',
                    name=f'MA {periodo} dias'
                ),
                row=1, col=1
            )

    # RSI ou Volume
    if mostrar_rsi:
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['RSI'],
                mode='lines',
                name='RSI'
            ),
            row=2, col=1
        )
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    else:
        cores = np.where(df['Close'] >= df['Open'], 'rgba(34,139,34,0.7)', 'rgba(220,20,60,0.7)')
        fig.add_trace(
            go.Bar(
                x=df['Date'],
                y=df['Volume'],
                name='Volume',
                marker_color=cores
            ),
            row=2, col=1
        )

    # Cruzamentos (apenas se mostrar_ma e mostrar_cruzamentos)
    if mostrar_cruzamentos and mostrar_ma and cruzamentos:
        for cruz in cruzamentos[-2:]:
            fig.add_trace(
                go.Scatter(
                    x=[cruz['data']],
                    y=[cruz['preco']],
                    mode='markers',
                    marker=dict(
                        color='red' if cruz['tipo'] == 'baixa' else 'green',
                        size=13,
                        symbol='star'
                    ),
                    name=cruz['label'],
                    showlegend=False
                ),
                row=1, col=1
            )

    # Atualiza layout com labels dinâmicos
    fig.update_layout(
        height=500,
        font_size=16,
        showlegend=True,
        margin=dict(l=50, r=50, t=50, b=50, pad=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title=dict(
            text=titulo,
            font=dict(size=20),
            x=0.5  # Centralizado
        ),
    )
    fig.update_xaxes(title_text="Data", row=2, col=1)
    fig.update_yaxes(title_text=y_label_preco, row=1, col=1)
    fig.update_yaxes(title_text=y_label_indicador, row=2, col=1)

    # Remove o range slider (existe só na xaxis primária)
    fig.update_layout(xaxis_rangeslider_visible=False)

    return fig


# Mostra as principais métricas do período
def exibir_metricas(hist):
    """
    Exibe métricas essenciais do ativo baseado no DataFrame do período escolhido.
    Espera DataFrame com colunas: 'Close', 'Open', 'High', 'Low', 'Volume'.
    """

    # Garante que o DataFrame não está vazio
    if hist.empty:
        st.warning('Nenhum dado disponível para o período selecionado.')
        return

    # Preço de fechamento atual (última linha)
    preco_atual = hist['Close'].iloc[-1]

    # Variação diária atual (% em relação ao dia anterior)
    if len(hist) >= 2:
        variacao_diaria = (hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100
    else:
        variacao_diaria = np.nan

    # Preço Máximo e Mínimo do período escolhido
    preco_max = hist['High'].max()
    preco_min = hist['Low'].min()

    # Volume médio do período
    volume_medio = hist['Volume'].mean()

    # Volatilidade histórica do período (desvio padrão dos retornos diários, anualizado)
    retornos_diarios = hist['Close'].pct_change().dropna()
    volatilidade = retornos_diarios.std() * np.sqrt(252) * 100  # Expressa em %
    
    st.write("")
    st.write("")
    st.subheader("Métricas do Período")

    col1, col2, col3, col4 = st.columns([0.05, 1.2, 1.2, 0.05])
    with col2:
        st.html('<span class="left_indicator"></span>')
        st.metric("Fechamento Atual", f"$ {preco_atual:,.2f}", border=True)
        st.metric("Preço Máximo", f"$ {preco_max:,.2f}", border=True)
        st.metric("Volume Médio", f"$ {volume_medio:,.0f}", border=True)        
        
    
    with col3:
        st.html('<span class="right_indicator"></span>')
        st.metric("Variação Diária Atual", f"{variacao_diaria:.2f} %", border=True)
        st.metric("Preço Mínimo", f"$ {preco_min:,.2f}", border=True)    
        st.metric("Volatilidade Histórica", f"{volatilidade:.2f} %", border=True)
        

# comparativo.py -------------------------------------


def grafico_evolucao_percentual(df_pct, ativos_grafico):
    df_plotly = df_pct[ativos_grafico].copy()
    df_plotly['Data'] = df_pct.index
    df_plotly = pd.melt(df_plotly, id_vars=['Data'], value_vars=ativos_grafico,
                        var_name='Ativo', value_name='Variação Percentual')
    fig = px.line(
        df_plotly, x="Data", y="Variação Percentual", color="Ativo",
        labels={"Data": "Data", "Variação Percentual": "Variação Percentual (%)", "Ativo": "Ativo"},
        line_shape="spline",  # suaviza as curvas
    )
    fig.update_traces(line=dict(width=1.5))  # linhas mais espessas

    fig.update_layout(
        legend_title_text='Ativo',
        xaxis_title='Data',
        yaxis_title='Variação Percentual (%)',
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.08,
            xanchor="right", x=1,
            font=dict(size=13),
        ),
        margin=dict(l=30, r=30, t=30, b=10),
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',  # fundo transparente
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Grid mais suave
    fig.update_xaxes(showgrid=True, gridcolor="rgba(150,150,150,0.12)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(150,150,150,0.12)")

    return fig

def adicionar_anotacoes_percentuais(fig, df_pct, ativos_grafico):
    for idx, ativo in enumerate(ativos_grafico):
        x_final = df_pct.index[-1]
        y_final = df_pct[ativo].iloc[-1]
        variacao_txt = f"{y_final:+.2f}%"
        cor_serie = fig.data[idx].line.color if idx < len(fig.data) else "#333"
        fig.add_annotation(
            x=x_final,
            y=y_final,
            text=variacao_txt,
            showarrow=True,
            arrowhead=1,
            ax=40,
            ay=0,
            font=dict(size=13, color=cor_serie, family="monospace"),            
            bordercolor=cor_serie,
            borderwidth=1,
            borderpad=3,
            arrowcolor=cor_serie,
            align="left"
        )
    return fig

