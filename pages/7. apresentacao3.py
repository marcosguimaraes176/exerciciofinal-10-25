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

# --- CSS global para títulos e textos ---
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
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Títulos principais ---
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
    }.get(color, "YlGnBu")

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
# FUNÇÃO CENTRALIZADA DE EXIBIÇÃO
# -----------------------------------------------------------
def exibir_centralizado(elemento_func):
    """Cria colunas para centralizar o elemento."""
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        elemento_func()

def exibir_projeto(titulo, imagem, csv, nome_projeto, cor, texto_estudantes):
    st.markdown(f"<h1 style='font-size:22px; color:#808000; text-align:center;'>{titulo}</h1>", unsafe_allow_html=True)

    # Centraliza imagem
    exibir_centralizado(lambda: st.image(imagem, caption=titulo, use_container_width=False))

    # Centraliza mapa
    project_data = load_project_data(csv)
    mapa = create_choropleth_map(geo_data, project_data, nome_projeto, cor)
    exibir_centralizado(lambda: st_folium(mapa, width=700, height=500))

    # Centraliza texto dos dados
    st.markdown(f"<p class='centered-text'>{texto_estudantes}</p>", unsafe_allow_html=True)

# -----------------------------------------------------------
# EXIBIÇÃO DO PROJETO SELECIONADO
# -----------------------------------------------------------
if projeto_escolhido == "Bandas nas Escolas":
    exibir_projeto(
        "Projeto Bandas nas Escolas",
        "fotos/bandas.jpeg",
        "data/df_bandas.csv",
        "BANDAS",
        "blue",
        """
        <b>Quantidade de Estudantes Bandas:</b><br>
        2023: 1.282<br>
        2024: 1.356<br>
        2025: 1.289
        """
    )

elif projeto_escolhido == "Orquestra de Violões nas Escolas":
    exibir_projeto(
        "Projeto Orquestra de Violões nas Escolas",
        "fotos/violões.jpeg",
        "data/df_violao.csv",
        "VIOLÕES",
        "red",
        """
        <b>Quantidade de Estudantes Violões:</b><br>
        2023: 3.441<br>
        2024: 2.295<br>
        2025: 2.720
        """
    )

elif projeto_escolhido == "Corais nas Escolas":
    exibir_projeto(
        "Projeto Corais nas Escolas",
        "fotos/coral.jpeg",
        "data/df_corais.csv",
        "CORAIS",
        "purple",
        """
        <b>Quantidade de Estudantes Corais:</b><br>
        2023: 1.158<br>
        2024: 1.434<br>
        2025: 1.489
        """
    )

elif projeto_escolhido == "Orquestra Sinfônica Jovem":
    exibir_projeto(
        "Projeto Orquestra Sinfônica Jovem",
        "fotos/sinfônica.jpeg",
        "data/df_orquestra.csv",
        "ORQUESTRA",
        "yellow",
        """
        <b>Quantidade de Estudantes Sinfônica:</b><br>
        2023: 476<br>
        2024: 501<br>
        2025: 464
        """
    )
