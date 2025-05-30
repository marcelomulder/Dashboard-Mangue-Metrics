import streamlit as st
import plotly.express as px
from src.dados import carregar_dados_yf, filtrar_ativos_disponiveis
from src.indicadores import calcular_valorizacao_percentual, calcular_valor_monetario
from src.visualizacao import grafico_evolucao_percentual, adicionar_anotacoes_percentuais
from src.ui import highlight_carteira, moeda
from src.widgets import tradingview_ticker_tape
from src.ui import exibir_resultado_carteira
from src.ui import rodape_mangue_metrics



st.set_page_config(page_title="Simulador de Carteira", layout="wide")

st.html("styles.html")

st.title("Simulador de Carteira")

tradingview_ticker_tape(height=110, color_theme="dark")

ATIVOS = {
    'Bitcoin': 'BTC-USD',
    'Solana': 'SOL-USD',
    'Ethereum': 'ETH-USD',
    'Ripple': 'XRP-USD',
    'SPY': 'SPY',
    'EWZ': 'EWZ',
    'IAU': 'IAU',
}

st.sidebar.image("images/logo-dark.png", use_container_width=True, width=1)
st.sidebar.header("Monte sua Carteira")

ativos_escolhidos = st.sidebar.multiselect(
    "Selecione os ativos:",
    list(ATIVOS.keys()),
    default=[]
)

valor_inicial = st.sidebar.number_input(
    "Valor inicial da carteira:",
    min_value=10.0,
    value=1000.0,
    step=100.0,
    format="%.2f"
)

PERIODOS_LABELS = {
    "1 ano": "1y",    
    "3 anos": "3y",
    "5 anos": "5y",        
    "Ano Atual": "YTD",
    "6 meses": "6mo",
    "1 mês": "1mo"
    
}

periodo_label = st.sidebar.selectbox(
    "Período dos dados",
    options=list(PERIODOS_LABELS.keys()),
    index=0
)
periodo = PERIODOS_LABELS[periodo_label]  # Valor técnico usado no yfinance

st.sidebar.markdown("---")

if valor_inicial < 100.0:
    st.sidebar.info("Considere inserir um valor inicial maior para simulações mais realistas.")

if not ativos_escolhidos:
    st.markdown(
        """
        <div style='
            text-align: center; 
            padding-top: 70px; 
            font-size: 1.3em; 
            color: #444; 
            background: rgba(30,30,30,0.05); 
            border-radius: 8px; 
            padding: 30px; 
            margin: 30px 0; 
            box-shadow: 0 1px 8px #0001;'>
            <b>Bem-vindo!</b><br>
            Selecione ao menos um ativo no menu lateral para montar sua carteira e visualizar o comparativo histórico.<br>
            <span style='font-size:0.95em; color: #888;'>Dica: você pode ajustar os pesos dos ativos para simular diferentes estratégias.</span>
        </div>
        """, unsafe_allow_html=True
    )
    rodape_mangue_metrics()
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

#Mostrar erro caso a carteira não esteja 100%
if total != 100:
    if total < 100:
        faltando = 100 - total
        st.warning(f"Faltam {faltando}% para completar 100% da alocação.")
    else:
        excedente = total - 100
        st.warning(f"Excedeu em {excedente}% o limite de 100% da alocação.")

ativos_filtrados = {k: ATIVOS[k] for k in ativos_escolhidos}
df = carregar_dados_yf(ativos_filtrados, periodo)
ativos_com_dados = filtrar_ativos_disponiveis(df, ativos_escolhidos)

if not ativos_com_dados:
    st.warning("Nenhum dos ativos selecionados possui dados disponíveis para o período escolhido.")     
    
    st.stop()

# Gráfico Simulação de Carteira
col1, col2, col3 = st.columns([0.1, 3, 0.3])


with col2:
    st.html('<span class="graph_indicator"></span>')
    st.subheader("Gráfico - Evolução da Carteira e Ativos")
    df_pct, ativos_grafico = calcular_valorizacao_percentual(df, ativos_com_dados, pesos, total)
    fig = grafico_evolucao_percentual(df_pct, ativos_grafico)
    fig = adicionar_anotacoes_percentuais(fig, df_pct, ativos_grafico)
    st.plotly_chart(fig, use_container_width=True)

# Cálculo monetário para o resumo
df_valor, valores_iniciais_ativos = calcular_valor_monetario(df, ativos_com_dados, pesos, valor_inicial, total)

with st.expander("Resultado da Carteira", expanded=False):
    exibir_resultado_carteira(
        ativos_com_dados=ativos_com_dados,
        valores_iniciais_ativos=valores_iniciais_ativos,
        df_valor=df_valor,
        valor_inicial=valor_inicial,
        pesos=pesos,
        total=total
    )

#st.markdown("---")
rodape_mangue_metrics()

