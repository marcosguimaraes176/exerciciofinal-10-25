import streamlit as st


st.image("fotos/maxresdefault-2.jpg")

def titulo_com_tamanho(texto, tamanho=36, fonte='Elephant', negrito=True, cor='#191970'):
    """Função para criar texto com tamanho personalizado"""
    estilo_negrito = "font-weight: bold;" if negrito else ""
    
    st.markdown(f"<p style='font-size: {tamanho}px; font-family: {fonte}; color: {cor}; {estilo_negrito}'>{texto}</p>", 
                unsafe_allow_html=True)

titulo_com_tamanho("Programa Músicana Rede: características", tamanho=36, cor='#006666')
#st.title("O Programa Música na Rede: Características")