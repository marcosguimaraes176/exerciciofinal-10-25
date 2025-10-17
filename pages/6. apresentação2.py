import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
from streamlit_folium import st_folium

# -----------------------------------------------------------
# CONFIGURAÇÃO GERAL DA PÁGINA
# -----------------------------------------------------------
st.set_page_config(page_title="Programa Música na Rede", layout="wide")

# --- CSS e títulos ---
st.markdown(
    """
    <style>
    .central-title {
        text-align: center;
        font-family: Georgia, serif;
        font-size: 36px !important;
        color: #8B0000;
        padding-bottom: 5px;
    }
    .central-subtitle {
        text-align: center;
        font-family: Georgia, serif;
        font-size: 20px;
        color: #4682B4;
        margin-top: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="central-title">🎵 Programa Música na Rede</div>', unsafe_allow_html=True)
st.markdown('<p class="central-subtitle">Dados por Municípios, Estudantes e Projetos</p>', unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------
with st.sidebar:
    st.header("Escolha o Projeto")
    projeto_escolhido = st.selectbox(
        "Selecione um projeto para visualizar:",
        [
            "Bandas nas Escolas",
            "Orquestra de Violões nas Escolas",
            "Corais nas Escolas",
            "Orquestra Sinfônica Jovem"
        ]
    )
    st.markdown("[Voltar ao topo](#🎵-programa-música-na-rede)")

# -----------------------------------------------------------
# FUNÇÕES DE CARREGAMENTO
# -----------------------------------------------------------
@st.cache_data
def load_geodata(shapefile_path):
    return gpd.read_file(shapefile_path)

@st.cache_data
def load_project_data(csv_path):
    return pd.read_csv(csv_path)

def create_choropleth_map(geo_data, project_data, projeto_nome, color):
    projeto_nome = str(projeto_nome).upper()
    project_data.columns = project_data.columns.str.strip().str.upper()

    merged_data = geo_data.merge(
        project_data,
        left_on='NM_MUN',
        right_on='MUNICÍPIO',
        how='left'
    )

    project_column = f'PROJETO_{projeto_nome}'
    merged_data[project_column] = merged_data['DETALHE_PROJETO'].apply(
        lambda x: 1 if projeto_nome in str(x).upper() else 0
    )

    m = folium.Map(location=[-19.1834, -40.3086], zoom_start=7, tiles='CartoDB positron')

    fill_color = {
        "blue": "YlGnBu",
        "red": "YlOrRd",
        "purple": "PuRd",
        "yellow": "Greens"
    }[color]

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

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['NM_MUN', project_column],
            aliases=['Município:', f'{projeto_nome}:'],
            localize=True,
            style=("background-color: white; color: #333333; "
                   "font-family: arial; font-size: 12px; padding: 10px;")
        )
    )

    return m

# -----------------------------------------------------------
# CARREGAMENTO DOS DADOS BASE
# -----------------------------------------------------------
try:
    geo_data = load_geodata("data/ES_Municipios_2024.shp")
except Exception as e:
    st.error(f"Erro ao carregar shapefile: {e}")
    st.stop()

# -----------------------------------------------------------
# EXIBIÇÃO CONDICIONAL DO PROJETO ESCOLHIDO
# -----------------------------------------------------------
if projeto_escolhido == "Bandas nas Escolas":
    st.markdown("<h1 style='font-size:20px; color:#808000;'>Projeto Bandas nas Escolas</h1>", unsafe_allow_html=True)
    st.image("fotos/bandas.jpeg", caption="Bandas nas Escolas", use_container_width=False, width=350)
    project_data = load_project_data("data/df_bandas.csv")
    mapa = create_choropleth_map(geo_data, project_data, "BANDAS", color="blue")
    st_folium(mapa, width=700, height=500)
    st.markdown("""
    **Quantidade de Estudantes Bandas:**  
    2023: 1.282  
    2024: 1.356  
    2025: 1.289
    """)

elif projeto_escolhido == "Orquestra de Violões nas Escolas":
    st.markdown("<h1 style='font-size:20px; color:#808000;'>Projeto Orquestra de Violões nas Escolas</h1>", unsafe_allow_html=True)
    st.image("fotos/violões.jpeg", caption="Orquestra de Violões nas Escolas")
    project_data = load_project_data("data/df_violao.csv")
    mapa = create_choropleth_map(geo_data, project_data, "VIOLÕES", color="red")
    st_folium(mapa, width=700, height=500)
    st.markdown("""
    **Quantidade de Estudantes Violões:**  
    2023: 3.441  
    2024: 2.295  
    2025: 2.720
    """)

elif projeto_escolhido == "Corais nas Escolas":
    st.markdown("<h1 style='font-size:20px; color:#808000;'>Projeto Corais nas Escolas</h1>", unsafe_allow_html=True)
    st.image("fotos/coral.jpeg", caption="Corais nas Escolas")
    project_data = load_project_data("data/df_corais.csv")
    mapa = create_choropleth_map(geo_data, project_data, "CORAIS", color="purple")
    st_folium(mapa, width=700, height=500)
    st.markdown("""
    **Quantidade de Estudantes Corais:**  
    2023: 1.158  
    2024: 1.434  
    2025: 1.489
    """)

elif projeto_escolhido == "Orquestra Sinfônica Jovem":
    st.markdown("<h1 style='font-size:20px; color:#808000;'>Projeto Orquestra Sinfônica Jovem</h1>", unsafe_allow_html=True)
    st.image("fotos/sinfônica.jpeg", caption="Orquestra Sinfônica Jovem")
    project_data = load_project_data("data/df_orquestra.csv")
    mapa = create_choropleth_map(geo_data, project_data, "ORQUESTRA", color="yellow")
    st_folium(mapa, width=700, height=500)
    st.markdown("""
    **Quantidade de Estudantes Sinfônica:**  
    2023: 476  
    2024: 501  
    2025: 464
    """)
