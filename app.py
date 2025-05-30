import streamlit as st

# Define the pages
main_page = st.Page("pages/capa.py", title="Início", icon="🏠")
page_1 = st.Page("pages/analise-ativo.py", title="Análise de Ativo", icon="💵")
page_2 = st.Page("pages/comparativo.py", title="Simulador de Carteira", icon="💵")



# Set up navigation
pg = st.navigation([main_page, page_1, page_2])

# Run the selected page
pg.run()