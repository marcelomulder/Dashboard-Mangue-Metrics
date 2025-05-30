import streamlit as st
from src.ui import rodape_mangue_metrics

st.set_page_config(page_title="Mangue Metrics - Dashboard", layout="wide")    

st.html("styles.html")

# Oculta menu e footer padrão 
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

# Centralizando elementos
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("images/logo-dark.png")
    st.markdown("<h3 style='text-align: center; color: #5a5a5a; margin-bottom: 24px;'>Monitoramento inteligente para ativos financeiros</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; max-width: 400px; margin: auto;'>Simplificando sua tomada de decisão com dados, gráficos e análises técnicas.</p>", unsafe_allow_html=True)
    st.write("")
    
# Rodapé 
rodape_mangue_metrics()
