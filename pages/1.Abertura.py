import streamlit as st

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("fotos/maxresdefault-2.jpg", width=2000)
#st.image("fotos/maxresdefault-2.jpg", width=1200)

def titulo_com_tamanho(texto, tamanho=36, fonte='Bookman Old Style', negrito=True, alinhamento = 'center', cor='#191970'):
    """Função para criar texto com tamanho personalizado"""
    estilo_negrito = "font-weight: bold;" if negrito else ""
    
    st.markdown(f"<p style='font-size: {tamanho}px; font-family: {fonte}; color: {cor}; {estilo_negrito}; text-align: {alinhamento}'>{texto}</p>", 
                unsafe_allow_html=True)

titulo_com_tamanho("Programa Músicana Rede:<br> Características", tamanho=36, cor='#006666')

#st.title("O Programa Música na Rede: Características")