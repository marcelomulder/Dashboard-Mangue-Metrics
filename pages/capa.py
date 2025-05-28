import streamlit as st

# Oculta menu e footer padrão (opcional)
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Centralizando elementos usando st.columns
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

#st.image("images/logo-dark.png")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("images/logo-dark.png")
    st.markdown("<h3 style='text-align: center; color: #5a5a5a; margin-bottom: 24px;'>Monitoramento inteligente para ativos financeiros</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; max-width: 400px; margin: auto;'>Simplificando sua tomada de decisão com dados, gráficos e análises técnicas.</p>", unsafe_allow_html=True)
    st.write("")
    # st.markdown(
    #     """
    #     <div style='display: flex; justify-content: center; gap: 24px; margin-top: 32px;'>
    #         <a href='?page=analise-ativo'>
    #             <button style='padding: 12px 32px; font-size: 1.1em; background-color: #1e88e5; color: white; border: none; border-radius: 8px; cursor: pointer;'>
    #                 Análise de Ativo
    #             </button>
    #         </a>
    #         <a href='?page=simulador-carteira'>
    #             <button style='padding: 12px 32px; font-size: 1.1em; background-color: #388e3c; color: white; border: none; border-radius: 8px; cursor: pointer;'>
    #                 Simulador de Carteira
    #             </button>
    #         </a>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

# Rodapé simples centralizado
st.markdown("""
    <div style='text-align: center; color: #bbb; font-size: 0.9em; margin-top: 100px;'>
        © 2025 Mangue Metrics - Versão 0.5
    </div>
""", unsafe_allow_html=True)
