import streamlit as st

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    
    st.image("fotos/ifes.png", width=400)

    
def titulo_com_tamanho(texto, tamanho=36, fonte='Georgia', negrito=True, alinhamento = 'center', cor='#191970'):
    """Função para criar texto com tamanho personalizado"""
    estilo_negrito = "font-weight: bold;" if negrito else ""
    
    st.markdown(f"<p style='font-size: {tamanho}px; font-family: {fonte}; color: {cor}; {estilo_negrito}; text-align: {alinhamento}'>{texto}</p>", 
                unsafe_allow_html=True)


titulo_com_tamanho("Instituto Federal do Espírito Santo", tamanho=36, cor='#191970')
# st.title("Instituto Federal do Espírito Santo - IFES") 

def texto_com_tamanho(texto, tamanho=30, fonte='Verdana', italico=True, alinhamento = 'center', cor='#191970'):
    """Função para criar texto com tamanho personalizado"""
    estilo_italico = "font-style: italic;" if italico else ""
    st.markdown(f"<p style='font-size: {tamanho}px; ont-family: {fonte}; color: {cor}; {estilo_italico}; text-align: {alinhamento}'>{texto}</p>", 
                unsafe_allow_html=True)
texto_com_tamanho("Campus Serra", tamanho=30, cor='#191970')


titulo_com_tamanho("Disciplina:Cloud Computing para Produtos de Dados", tamanho=36, cor='#0000ff')
texto_com_tamanho("Professor Maxwell Monteiro", tamanho=30, cor='#1e90ff')
#st.title("Disciplina:Cloud Computing para Produtos de Dados")
#st.text("Professor Maxwell Monteiro")

titulo_com_tamanho("Programa Música na Rede", tamanho=36, cor='#008080')
#st.title("Pesquisa: Programa Música na Rede")
texto_com_tamanho("Aluno: Marcos Valério Guimarães", tamanho=30, cor='#5f8080')
#st.text("Aluno: Marcos Valerio Guimaraes")