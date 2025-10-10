import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
from streamlit_folium import st_folium
import os

# -----------------------------------------------------------
# CONFIGURAÇÃO GERAL DA PÁGINA
# -----------------------------------------------------------
st.set_page_config(page_title="Programa Música na Rede", layout="wide")

st.title("🎵 Programa Música na Rede")
st.markdown(
    """
    <h1 style='font-size:20px; color:#000080;'>
        Dados por Escolas, Estudantes e Projetos:
    </h1>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# COLUNAS PRINCIPAIS DO LAYOUT
# -----------------------------------------------------------
col1, col2 = st.columns([0.5, 0.5])

with st.sidebar:
    st.markdown("[Voltar ao topo](#🎵-programa-música-na-rede)")

# -----------------------------------------------------------
# FUNÇÕES DE CARREGAMENTO DE DADOS
# -----------------------------------------------------------
@st.cache_data
def load_geodata(shapefile_path):
    """Carrega o shapefile (dados geográficos)."""
    return gpd.read_file(shapefile_path)

@st.cache_data
def load_project_data(csv_path):
    """Carrega os dados de projetos (CSV)."""
    return pd.read_csv(csv_path)

# -----------------------------------------------------------
# FUNÇÃO PARA CRIAR O MAPA COROPLÉTICO
# -----------------------------------------------------------
def create_choropleth_map(geo_data, project_data, projeto_nome, color):
    # Garantir que projeto_nome seja string
    projeto_nome = str(projeto_nome).upper()

    # Padronizar nomes das colunas do CSV
    project_data.columns = project_data.columns.str.strip().str.upper()

    # Merge com base nas colunas corretas
    merged_data = geo_data.merge(
        project_data,
        left_on='NM_MUN',        # nome do município no shapefile
        right_on='MUNICÍPIO',    # nome do município no CSV
        how='left'
    )

    # Cria coluna binária: 1 se o município tem o projeto, 0 caso contrário
    project_column = f'PROJETO_{projeto_nome}'
    merged_data[project_column] = merged_data['DETALHE_PROJETO'].apply(
        lambda x: 1 if projeto_nome in str(x).upper() else 0
    )

    # Cria o mapa base
    m = folium.Map(
        location=[-19.1834, -40.3086],  # Centralizado no ES
        zoom_start=7,
        tiles='CartoDB positron'
    )

    # Define a paleta de cores
    fill_color = (
        'YlGnBu' if color == 'blue' else
        'YlOrRd' if color == 'red' else
        'PuRd' if color == 'purple' else
        'Greens'
    )

    # Cria o coroplético
    choropleth = Choropleth(
    geo_data=merged_data.__geo_interface__,
    data=merged_data,
    columns=['NM_MUN', project_column],
    key_on='feature.properties.NM_MUN',
    fill_color=fill_color,
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f'Municípios com {projeto_nome}',
    highlight=True
    ).add_to(m)


    # Adiciona tooltip
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['NM_MUN', project_column],
            aliases=['Município:', f'{projeto_nome}:'],
            localize=True,
            style=(
                "background-color: white; color: #333333; "
                "font-family: arial; font-size: 12px; padding: 10px;"
            )
        )
    )

    return m

# -----------------------------------------------------------
# CARREGAMENTO DOS DADOS FIXOS
# -----------------------------------------------------------
try:
    geo_data = load_geodata("data/ES_Municipios_2024.shp")
    project_data = load_project_data("data/df_bandas.csv")
except Exception as e:
    st.error(f"Erro ao carregar arquivos: {e}")
    st.stop()

# -----------------------------------------------------------
# LADO ESQUERDO: BANDAS NAS ESCOLAS
# -----------------------------------------------------------
with col1:
    st.markdown(
        """
        <h1 style='font-size:20px; color:#808000;'>
            Projeto Bandas nas Escolas
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.image("fotos/bandas.jpeg", caption="Bandas nas Escolas")
    st.text("Bandas por Municípios:")

    mapa_bandas = create_choropleth_map(geo_data, project_data, projeto_nome="BANDAS", color="blue")
    st_folium(mapa_bandas, width=700, height=500)

st.text("Quantidade de Estudantes Bandas:<br>2023:1.282<br>2024:1.356<br>2025:1.289")


# -----------------------------------------------------------
# LADO DIREITO: ORQUESTRA DE VIOLÕES
# -----------------------------------------------------------
with col2:
    st.markdown(
        """
        <h1 style='font-size:20px; color:#808000;'>
            Projeto Orquestra de Violões nas Escolas
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.image("fotos/violões.jpeg", caption="Orquestra de Violões nas Escolas")
    st.text("Escolas por Municípios Escolas Violões:")
    project_data_V = load_project_data("data/df_violao.csv")
    mapa_violões = create_choropleth_map(geo_data, project_data_V, projeto_nome="VIOLÕES", color="red")
    st_folium(mapa_violões, width=700, height=500)

    st.text("Quantidade de Estudantes Violões:<br>2023:3.441<br>2024:2.295<br>2025:2.720")

# -----------------------------------------------------------
# OUTRAS SEÇÕES DE PROJETOS
# -----------------------------------------------------------
col3, col4 = st.columns([0.5, 0.5])

with col3:
    st.markdown(
        """
        <h1 style='font-size:20px; color:#808000;'>
            Projeto Corais nas Escolas
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.image("fotos/coral.jpeg", caption="Corais nas Escolas")
    st.text("Escolas por Municípios Escolas Corais:")
    project_data_C = load_project_data("data/df_corais.csv")
    mapa_corais = create_choropleth_map(geo_data, project_data_C, projeto_nome="CORAIS", color="purple")
    st_folium(mapa_corais, width=700, height=500)

    st.text("Quantidade de Estudantes Corais:<br>2023:1.158<br>2024:1.434<br>2025:1.489")

with col4:
    st.markdown(
        """
        <h1 style='font-size:20px; color:#808000;'>
            Projeto Orquestra Sinfônica Jovem
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.image("fotos/sinfônica.jpeg", caption="Orquestra Sinfônica Jovem")
    st.text("Escolas por Município Escolas Sinfônica:")
    project_data_S = load_project_data("data/df_orquestra.csv")
    mapa_sinfônica = create_choropleth_map(geo_data, project_data_S, projeto_nome="ORQUESTRA", color="yellow")
    st_folium(mapa_sinfônica, width=700, height=500)
    
    st.text("Quantidade de Estudantes Sinfônica:<br>2023:476<br>2024:501<br>2025:464")

   