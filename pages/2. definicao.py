import streamlit as st

def titulo_com_tamanho(texto, tamanho=36, fonte='Georgia', negrito=True, alinhamento = 'center', cor='#000080'):
    """Função para criar texto com tamanho personalizado"""
    estilo_negrito = "font-weight: bold;" if negrito else ""
    
    st.markdown(f"<p style='font-size: {tamanho}px; font-family: {fonte}; color: {cor}; {estilo_negrito}; text-align: {alinhamento}'>{texto}</p>", 
                unsafe_allow_html=True)
    
titulo_com_tamanho("Definição", tamanho=36, cor='#000080')

st.text("Do tema: O Programa Música na Rede é uma iniciativa da SEDU-ES, FAPES e FAMES, que visa promover a educação musical nas escolas públicas do Espírito Santo. São ofertados quatro projetos: Bandas nas Escolas, Orquestra de Violões nas Escolas, Corais nas Escolas e Oruqestra Sinfônica Jovem nas Escolas")

st.text("Do Objetivo da pesquisa: Investigar a influência do Programa Música na Rede no desempenho escolar dos estudantes da educação básica da Rede Estadual do Espírito Santo.")

#col1, col2, col3 = st.columns([1, 4, 1]) 

#with col2:
    # A imagem é colocada na coluna 2 (a central), centralizando-a
    #st.image("fotos/MnR SantaJazz.jpeg", use_container_width=True)

st.header("Imagem do Projeto")
# Colunas: 1 (espaço vazio) | 4 (imagem) | 1 (espaço vazio)
col_img_left, col_img_center, col_img_right = st.columns([1, 4, 1]) 

with col_img_center:
    st.image(
        "fotos/MnR SantaJazz.jpeg",
        # Altere o número 500 para a largura desejada em pixels
        width=400 
    )