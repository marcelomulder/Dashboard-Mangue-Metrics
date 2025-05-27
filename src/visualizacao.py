import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Gráfico principal da aplicação
def gerar_grafico(df, mostrar_ma, mostrar_rsi, ma_periodos, tipo_grafico, cruzamentos=[], mostrar_cruzamentos=True):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "xy"}], [{"type": "scatter"}]]
    )

    # Seleciona o tipo de gráfico
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

    # Mostra ou não as médias móveis
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

    #Dá a opção do usuário escolher entre Volume e IFR.
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
        cores = np.where(df['Close'] >= df['Open'], 'rgba(34, 139, 34, 0.7)', 'rgba(220,20,60,0.7)')
        fig.add_trace(
            go.Bar(
                x=df['Date'],
                y=df['Volume'],
                name='Volume',
                marker_color=cores
            ),
            row=2, col=1
        )

    #Dá a opação de mostrar os cruzamentos de média móveis no gráfico
    if mostrar_cruzamentos:
        for cruz in cruzamentos:
            fig.add_trace(
                go.Scatter(
                    x=[cruz['data']],
                    y=[cruz['preco']],
                    mode='markers',
                    marker=dict(color='red' if cruz['tipo']=='baixa' else 'green', size=12, symbol='arrow'),
                    text=[cruz['label']],
                    textposition='top center',
                    name=cruz['label'],
                    showlegend=False
                ),
                row=1, col=1
            )

    # Configura o fomrato do gráfico
    fig.update_layout(
        height=500,
        font_size=16,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        margin=dict(l=50, r=50, t=50, b=50, pad=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# Mostra as principais métricas do período
def exibir_metricas(df_periodo):
    st.subheader("Métricas do Período")
    st.metric(label="Menor Volume Diário", value=f"{df_periodo['Volume'].min():,.0f}")
    st.metric(label="Maior Volume Diário", value=f"{df_periodo['Volume'].max():,.0f}")
    st.metric(label="Menor Preço de Fechamento", value=f"${df_periodo['Close'].min():.2f}")
    st.metric(label="Maior Preço de Fechamento", value=f"${df_periodo['Close'].max():.2f}")
    st.metric(label="Média de Volume Diário", value=f"{df_periodo['Volume'].mean():,.0f}")    

