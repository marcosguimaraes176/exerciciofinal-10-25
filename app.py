import streamlit as st

st.image("fotos/ifes.png")


def titulo_com_tamanho(texto, tamanho=32, cor='blue'):
    """Função para criar texto com tamanho personalizado"""
    st.markdown(f"<p style='font-size: {tamanho}px; color: {cor};'>{texto}</p>", 
                unsafe_allow_html=True)
titulo_com_tamanho("Instituto Federal do Espírito Santo", tamanho=32, cor='red')
# st.title("Instituto Federal do Espírito Santo - IFES") 

def texto_com_tamanho(texto, tamanho=24, cor='blue'):
    """Função para criar texto com tamanho personalizado"""
    st.markdown(f"<p style='font-size: {tamanho}px; color: {cor};'>{texto}</p>", 
                unsafe_allow_html=True)
texto_com_tamanho("Campus Serra", tamanho=24, cor='blue')

st.title("Disciplina:Cloud Computing para Produtos de Dados")
st.text("Professor Maxwell Monteiro")

st.title("Pesquisa: Programa Música na Rede")
st.text("Aluno: Marcos Valerio Guimaraes")