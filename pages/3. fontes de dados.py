import streamlit as st
import pandas as pd
import io
import openpyxl

st.markdown("""
<style>
/* Zera o espaçamento abaixo dos subcabeçalhos (st.subheader) */
h3 {
    margin-bottom: 0px; 
    padding-top: 5px; 
}

/* Zera o espaçamento abaixo de st.dataframe (a tabela) */
.stDataFrame {
    margin-bottom: 0px; 
}

/* Zera o espaçamento abaixo de st.text (usado para o df.info) */
.stText {
    margin-bottom: 0px;
}

/* Ajusta a linha divisória (st.markdown("---")) */
hr {
    margin-top: 10px; 
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


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

# --- Configuração da Página e Título (exemplo) ---
st.set_page_config(layout="wide")
st.title("📊 Análise Descritiva e Evolução de Projetos")
st.markdown("---")

# Nomes dos arquivos
FILE_PROJETOS = "data/Projetos por Municípios.xlsx"
FILE_MUSICA = "data/Relatório Música na Rede1.xlsx"

df_projetos = None
df_musica = None

# Carregamento da Primeira Tabela
try:
    st.info(f"Carregando {FILE_PROJETOS}...")
    df_projetos = pd.read_excel(FILE_PROJETOS)
except FileNotFoundError:
    st.error(f"🚨 Erro: O arquivo '{FILE_PROJETOS}' não foi encontrado.")
except Exception as e:
    st.error(f"🚨 Erro ao carregar {FILE_PROJETOS}: {e}")

# Carregamento da Segunda Tabela
try:
    st.info(f"Carregando {FILE_MUSICA}...")
    df_musica = pd.read_excel(FILE_MUSICA)
except FileNotFoundError:
    st.error(f"🚨 Erro: O arquivo '{FILE_MUSICA}' não foi encontrado.")
except Exception as e:
    st.error(f"🚨 Erro ao carregar {FILE_MUSICA}: {e}")


# --- 3. FUNÇÕES AUXILIARES DE EXIBIÇÃO E CÁLCULO ---

def exibir_tabelas(df, titulo_principal):
    """
    Exibe as três visualizações (describe, head, info) para um dado DataFrame.
    """
    if df is None:
        return
        
    st.header(f"Base: {titulo_principal}")

    # 1. Tabela Descritiva (describe)
    st.subheader("1. Estatísticas Descritivas (describe)")
    
    try:
        df_descritivo = df.describe(include='all').T 
    except Exception as e:
        st.warning(f"⚠️ Aviso: Não foi possível gerar o describe completo para **{titulo_principal}**. Exibindo apenas o numérico. Erro: {e}")
        df_descritivo = df.describe().T
        
    df_descritivo.index.name = 'Variável'
    
    st.dataframe(
        df_descritivo.reset_index(),
        use_container_width=True, 
        hide_index=True 
    )

    st.markdown("---") 

    # 2. Visualização do Head (Organização da Tabela Original)
    st.subheader("2. Visualização dos Dados Originais (Primeiras Linhas)")
    st.dataframe(df.head(), use_container_width=True)

    st.markdown("---") 

    # 3. Informações da Estrutura (info)
    st.subheader("3. Tipos de Dados e Contagem de Não-Nulos (info)")

    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    st.markdown("---")


def calcular_e_plotar_musica(df):
    """
    Realiza o cálculo do total e gera o gráfico de evolução.
    """
    if df is None:
        return

    # --- CÁLCULO DO TOTAL GERAL ---
    
    # Colunas de interesse (ANOS)
    colunas_anos = ['Alunos atendidos 2023', 'Alunos atendidos 2024', 'Alunos atendidos 2025']
    
    # Tenta calcular o total, tratando erros se as colunas não existirem
    try:
        # Garante que as colunas são numéricas e soma
        total_geral = df[colunas_anos].sum().sum()
        
        # Exibição do Total Geral
        st.header("📈 Análise de Atendimentos | Música na Rede")
        st.metric(
            label="Total Geral de Estudantes Atendidos (2023-2025)", 
            value=f"{total_geral:,.0f}".replace(",", "_").replace(".", ",").replace("_", ".") # Formatação Brasileira
        )
        st.markdown("---")

    except KeyError:
        st.warning(f"⚠️ Aviso: Não foi possível calcular o Total Geral. Verifique se as colunas {colunas_anos} existem na planilha Música na Rede.")
    except Exception as e:
         st.warning(f"⚠️ Ocorreu um erro inesperado no cálculo: {e}")


    # --- GERAÇÃO DO GRÁFICO DE EVOLUÇÃO ---
    st.subheader("Evolução Anual de Atendimentos por Projeto")

    try:
        # Assume que a coluna de identificação do projeto é a primeira, se 'Projeto' não existir
        coluna_projeto = 'Projeto' if 'Projeto' in df.columns else df.columns[0]
        
        # Cria um DataFrame apenas com os dados necessários para o gráfico
        df_plot = df[[coluna_projeto] + colunas_anos].set_index(coluna_projeto)
        
        # Transforma os dados de 'wide' (colunas por ano) para 'long' (Ano, Atendimento), 
        # o que é ideal para gráficos de linha com o Streamlit/Pandas.
        df_plot = df_plot.T 
        
        # Cria e exibe o gráfico
        st.line_chart(df_plot)
        
        st.caption(f"Cada linha representa a evolução de um item da coluna: '{coluna_projeto}' ao longo dos anos.")

    except Exception as e:
        st.warning(f"⚠️ Não foi possível gerar o gráfico de linhas. Verifique se as colunas {colunas_anos} e a coluna de identificação do projeto estão corretas. Erro: {e}")


# --- 4. EXIBIÇÃO SEQUENCIAL DAS BASES ---

# Exibe a primeira base de dados
exibir_tabelas(df_projetos, "**Projetos por Municípios**")

# Adiciona um separador para diferenciar as bases
st.markdown("#") # Espaço visual
st.markdown("---") 

# Exibe o Relatório Música na Rede (com cálculo e gráfico primeiro)
calcular_e_plotar_musica(df_musica) # Novo bloco de cálculo e gráfico
exibir_tabelas(df_musica, "**Relatório Música na Rede**")