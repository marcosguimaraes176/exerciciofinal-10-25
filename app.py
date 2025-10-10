import streamlit as st

st.image("fotos/ifes.png")

    
def titulo_com_tamanho(texto, tamanho=36, fonte='Georgia', negrito=True, cor='F5276C'):
    """Função para criar texto com tamanho personalizado"""
    estilo_negrito = "font-weight: bold;" if negrito else ""
    
    st.markdown(f"<p style='font-size: {tamanho}px; font-family: {fonte}; color: {cor}; {estilo_negrito}'>{texto}</p>", 
                unsafe_allow_html=True)


titulo_com_tamanho("Instituto Federal do Espírito Santo", tamanho=36, cor='F5276C')
# st.title("Instituto Federal do Espírito Santo - IFES") 

def texto_com_tamanho(texto, tamanho=30, cor='F54927'):
    """Função para criar texto com tamanho personalizado"""
    st.markdown(f"<p style='font-size: {tamanho}px; color: {cor};'>{texto}</p>", 
                unsafe_allow_html=True)
texto_com_tamanho("Campus Serra", tamanho=30, cor='F54927')


titulo_com_tamanho("Disciplina:Cloud Computing para Produtos de Dados", tamanho=36, cor='#0000ff')
texto_com_tamanho("Professor Maxwell Monteiro", tamanho=30, cor='#1e90ff')
#st.title("Disciplina:Cloud Computing para Produtos de Dados")
#st.text("Professor Maxwell Monteiro")

st.title("Pesquisa: Programa Música na Rede")
st.text("Aluno: Marcos Valerio Guimaraes")