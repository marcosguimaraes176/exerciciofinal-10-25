import streamlit as st

def titulo_com_tamanho(texto, tamanho=36, fonte='Georgia', negrito=True, alinhamento = 'center', cor='#000080'):
    """Função para criar texto com tamanho personalizado"""
    estilo_negrito = "font-weight: bold;" if negrito else ""
    
    st.markdown(f"<p style='font-size: {tamanho}px; font-family: {fonte}; color: {cor}; {estilo_negrito}; text-align: {alinhamento}'>{texto}</p>", 
                unsafe_allow_html=True)
titulo_com_tamanho("fonte de dados", tamanho=36, cor='#000080')


st.write("1. Site do Programa Música na Rede")
st.markdown("https://musicanarede.fames.es.gov.br/")

st.write("2. Sistema de Gestão:")
st.text("SEGES - Sistema Estadual de Gestão Escolar")