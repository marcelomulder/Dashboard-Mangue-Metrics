import streamlit as st

# Define the pages
main_page = st.Page("pages/analise-ativo.py", title="Início", icon="🏠")
page_2 = st.Page("pages/comparativo.py", title="Simulação de Carteira", icon="💵")


# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()