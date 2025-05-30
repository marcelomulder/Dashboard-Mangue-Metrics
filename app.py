import streamlit as st

#st.set_page_config(page_title="Mangue Metrics - Dashboard", layout="wide") 

# Define as páginas
main_page = st.Page("pages/capa.py", title="Início", icon="🏠")
page_1 = st.Page("pages/analise-ativo.py", title="Análise de Ativo", icon="💵")
page_2 = st.Page("pages/comparativo.py", title="Simulador de Carteira", icon="💵")
page_3 = st.Page("pages/chatbot.py", title="Chatbot", icon="🤖")


pg = st.navigation([main_page, page_1, page_2, page_3])

pg.run()