def checar_limite_mensagens(maximo=5):
    import streamlit as st
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0
    if st.session_state.message_count >= maximo:
        st.info(f"Você atingiu o limite de {maximo} perguntas nesta sessão. Recarregue a página para reiniciar.")
        return False
    return True