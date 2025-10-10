import streamlit as st

st.image("fotos/ifes.png")


def texto_com_tamanho(texto, tamanho=16, cor='blue'):
    """Função para criar texto com tamanho personalizado"""
    st.markdown(f"<p style='font-size: {tamanho}px; color: {cor};'>{texto}</p>", 
                unsafe_allow_html=True)
st.title("Instituto Federal do Espírito Santo - IFES") 


texto_com_tamanho("Campus Serra")

st.title("Disciplina:Cloud Computing para Produtos de Dados")
st.text("Professor Maxwell Monteiro")

st.title("Pesquisa: Programa Música na Rede")
st.text("Aluno: Marcos Valerio Guimaraes")