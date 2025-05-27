import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from streamlit_javascript import st_javascript

st.set_page_config(page_title="Comparativo de Ativos", layout="wide")
st.title("Comparativo de Ativos e Simulação de Carteira")

ATIVOS = {
    'Bitcoin (BTC)': 'BTC-USD',
    'Solana (SOL)': 'SOL-USD',
    'Ripple (XRP)': 'XRP-USD',
    'SPY': 'SPY',
    'EWZ': 'EWZ',
    'IAU': 'IAU',
}

st.sidebar.header("Monte sua Carteira")

ativos_escolhidos = st.sidebar.multiselect(
    "Selecione os ativos:",
    list(ATIVOS.keys()),
    default=[]  # Não deixa nenhum selecionado
)

periodo = st.sidebar.selectbox(
    "Período dos dados",
    options=["5y", "3y", "1y", "YTD", "max"],
    index=0
)

if not ativos_escolhidos:
    st.markdown(
        "<div style='text-align: center; padding-top: 50px; font-size: 1.3em; color: #666;'>"
        "Selecione ao menos um ativo no menu lateral para simular a carteira e visualizar o comparativo histórico."
        "</div>",
        unsafe_allow_html=True
    )
    st.stop()

pesos = {}
total = 0
for ativo in ativos_escolhidos:
    peso = st.sidebar.number_input(
        f"Peso (%) para {ativo}:", min_value=0, max_value=100,
        value=round(100/len(ativos_escolhidos)) if len(ativos_escolhidos) > 0 else 0
    )
    pesos[ativo] = peso
    total += peso

if total != 100:
    st.sidebar.warning("A soma dos pesos deve ser igual a 100%.")

@st.cache_data(show_spinner=False)
def load_yf_data(tickers, period):
    data = yf.download(list(tickers.values()), period=period, auto_adjust=True)
    if isinstance(data.columns, pd.MultiIndex):
        close = data['Close']
        close.columns = [k for k in tickers.keys()]
    else:
        close = data[['Close']]
        close.columns = [list(tickers.keys())[0]]
    close = close.dropna()
    return close

ativos_filtrados = {k: ATIVOS[k] for k in ativos_escolhidos}
df = load_yf_data(ativos_filtrados, periodo)

# Colunas já são os nomes exibidos ao usuário
df_norm = df.copy()
for ativo in ativos_escolhidos:
    df_norm[ativo] = df_norm[ativo] / df_norm[ativo].iloc[0] * 100

# Cálculo da carteira
if total == 100:
    carteira = np.zeros(len(df_norm))
    for ativo in ativos_escolhidos:
        carteira += df_norm[ativo] * (pesos[ativo]/100)
    df_norm['Carteira'] = carteira
    ativos_grafico = ativos_escolhidos + ['Carteira']
else:
    ativos_grafico = ativos_escolhidos

# Gráfico interativo Plotly
st.subheader("Evolução dos Ativos Selecionados (Normalizados)")
df_plotly = df_norm[ativos_grafico].copy()
df_plotly['Data'] = df_norm.index
df_plotly = pd.melt(df_plotly, id_vars=['Data'], value_vars=ativos_grafico,
                    var_name='Ativo', value_name='Valor Normalizado')

fig = px.line(
    df_plotly, x="Data", y="Valor Normalizado", color="Ativo",
    labels={"Data": "Data", "Valor Normalizado": "Valor Normalizado (Base 100)", "Ativo": "Ativo"},
    title="Evolução dos Ativos e Carteira (Normalizados)"
)
fig.update_layout(legend_title_text='Ativo', xaxis_title='Data', yaxis_title='Valor Normalizado (Base 100)')
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
- O gráfico mostra a evolução dos ativos selecionados e da carteira composta conforme os pesos definidos.
- Os valores são normalizados (base 100 no início do período).
""")

if total == 100:
    st.subheader("Resumo do Desempenho ao Final do Período")
    resumo = {}
    for ativo in ativos_grafico:
        resumo[ativo] = {
            'Valor Inicial': df[ativo].iloc[0] if ativo != 'Carteira' else 100,
            'Valor Final': df[ativo].iloc[-1] if ativo != 'Carteira' else carteira[-1],
            'Variação (%)': (df[ativo].iloc[-1] / df[ativo].iloc[0] - 1) * 100 if ativo != 'Carteira' else (carteira[-1] / 100 - 1) * 100
        }
    st.dataframe(pd.DataFrame(resumo).T.round(2))

st.markdown("""
### Insights
- Explore diferentes composições de carteira para ver qual seria a performance histórica.
- Você pode usar esses dados para avaliar estratégias de diversificação.
""")

st.markdown("---")
st.caption("Desenvolvido pela Mangue Metrics - 2025")
