import streamlit as st

def titulo_com_tamanho(texto, tamanho=36, fonte='Georgia', negrito=True, alinhamento = 'center', cor='#000080'):
    """Função para criar texto com tamanho personalizado"""
    estilo_negrito = "font-weight: bold;" if negrito else ""
    
    st.markdown(f"<p style='font-size: {tamanho}px; font-family: {fonte}; color: {cor}; {estilo_negrito}; text-align: {alinhamento}'>{texto}</p>", 
                unsafe_allow_html=True)
titulo_com_tamanho("Metodologia e Objetivos", tamanho=36, cor='#000080')


st.text ("Pesquisa de campo para levantar dados de funcionamento do programa")
st.text("Análise de dados fornecidos pela gestão do Programa Música na Rede")
st.text ("Pesquisa em banco de dados do SEGES para avaliar desempenho escolar antes e depois da participação no Programa MnR")

st.text("Objetivo: Desenvolver um aplicativo para registrar as presenças dos estudantes nos projetos e acompanhar o desempenho escolar.")

st.text("OBS: Os campos de acesso dos dados diários de presença e desempenho escolar estão em desenvolvimento e, por sua complexidade, não foi possível deixar funcional no prazo para análises dos colegas.")