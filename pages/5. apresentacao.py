from turtle import color
import streamlit as st
import time
import pandas as pd
import numpy as np
import openpyxl
st.title("Programa Música na Rede")
#st.header("Escolas, Estudantes, Projetos")
st.markdown(
    """
    <h1 style='font-size:20px; color:#000080;'>
        Dados por Escolas, Estudantes e Projetos:
    </h1>
    """,
    unsafe_allow_html=True
)
col1, col2=st.columns([0.50,0.50])

with st.sidebar:
    st.markdown("[Coluna1](#projetos)")
with st.container (border=1):
    with col1:
        #st.subheader("Bandas nas Escolas")
        st.markdown(
        """
        <h1 style='font-size:20px; color:#808000;'>
            Projeto Bandas nas Escolas
        </h1>
        """,
        unsafe_allow_html=True
    )
        st.image("fotos/bandas.jpeg", caption="bandas")
        with st.container(border=True,horizontal=True):
            st.text("Bandas por Municípios:")
import geopandas as gpd
import folium
from folium import Choropleth
from streamlit_folium import st_folium 
import tempfile
import os 

# Configuração da página
st.set_page_config(page_title="Programa Música na Rede", layout="wide")

# Função para carregar os dados geográficos
@st.cache_data
def load_geodata(caminho_geodata):
    """Carrega os dados do shapefile"""
    return gpd.read_file('data/ES_Municipios_2024.shp')

# Função para carregar os dados dos projetos
@st.cache_data
def load_project_data(csv_path):
    """Carrega os dados dos projetos do CSV"""
    return pd.read_csv(csv_path)

geo_data = gpd.read_file("data/ES_Municipios_2024.shp")
project_data = pd.read_csv("data/df_bandas.csv")

    
        
# Função para criar mapa
def create_choropleth_map(geo_data, project_data, BANDAS, blue):

# Merge dos dados geográficos com os dados do projeto
    merged_data = geo_data.merge(
        project_data, 
        left_on='NM_MUN',  # Ajuste conforme a coluna de nome do município no shapefile
        right_on='municipio',  # Ajuste conforme a coluna no CSV
        how='left'
    )

    # Criar coluna binária para o projeto específico
    project_column = f'projeto_{BANDAS.upper()}'
    merged_data[project_column] = merged_data['projeto'].apply(
        lambda x: 1 if BANDAS.upper() in str(x) else 0
    )        
    # Criar o mapa
    m = folium.Map(
        location=[-19.1834, -40.3086], 
        zoom_start=7,
        tiles='CartoDB positron'
    )  # Centralizado no Espírito Santo
    
    choropleth = Choropleth(
        geo_data=merged_data.__geo_interface__,
        data=merged_data,
        columns=['NM_MUN', project_column],  # Ajuste conforme as colunas
        key_on='feature.properties.NM_MUN',  # Ajuste conforme o GeoJSON
        fill_color='YlGnBu' if color == 'blue' else 'YlOrRd' if color == 'red' else 'PuRd' if color == 'purple' else 'Greens',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Municípios com {BANDAS}',
        bins=[0, 0.5, 1],  # Para mostrar apenas 0 e 1
        highlight=True
    ).add_to(m)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['NM_MUN', project_column],
            aliases=['Município:', f'{BANDAS}:'],
            localize=True,
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
# Adicionar tooltip com nome do município
    folium.features.GeoJson(
        merged_data,
        style_function=lambda x: {
            'fillColor': color if x['properties'][project_column] == 1 else 'lightgray',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7 if x['properties'][project_column] == 1 else 0.3
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=['NM_MUN', project_column],
            aliases=['Município:', f'{BANDAS}:'],
            localize=True,
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    ).add_to(m)
    
    return m

def main():
    st.title("🎵 Programa Música na Rede")
    st.markdown("### Mapa de Oferta dos Projetos Musicais por Município")

 # Upload dos arquivos
    st.sidebar.header("Upload de Arquivos")
    
    # Upload do CSV
    csv_file = st.sidebar.file_uploader("Carregar arquivo CSV", type=['csv'], key='csv')
    
    # Upload dos arquivos do shapefile
    shp_file = st.sidebar.file_uploader("Carregar arquivo .shp", type=['shp'], key='shp')
    shx_file = st.sidebar.file_uploader("Carregar arquivo .shx", type=['shx'], key='shx')
    dbf_file = st.sidebar.file_uploader("Carregar arquivo .dbf", type=['dbf'], key='dbf')
    prj_file = st.sidebar.file_uploader("Carregar arquivo .prj", type=['prj'], key='prj')
    
    # Se estiver usando dados fixos (sem upload), ajuste os caminhos aqui:
USE_UPLOAD = False  # Mude para True se quiser usar upload

def run_data_loading():
    # Definir as variáveis de upload dentro da função para garantir o escopo correto
    csv_file = st.sidebar.file_uploader("Carregar arquivo CSV", type=['csv'], key='csv')
    shp_file = st.sidebar.file_uploader("Carregar arquivo .shp", type=['shp'], key='shp')
    shx_file = st.sidebar.file_uploader("Carregar arquivo .shx", type=['shx'], key='shx')
    dbf_file = st.sidebar.file_uploader("Carregar arquivo .dbf", type=['dbf'], key='dbf')
    prj_file = st.sidebar.file_uploader("Carregar arquivo .prj", type=['prj'], key='prj')

    if USE_UPLOAD:
        if csv_file and shp_file and shx_file and dbf_file:
            # Salvar arquivos temporários
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Salvar arquivos do shapefile
                shp_path = os.path.join(tmp_dir, shp_file.name)
                with open(shp_path, 'wb') as f:
                    f.write(shp_file.getvalue())
                
                shx_path = os.path.join(tmp_dir, shx_file.name)
                with open(shx_path, 'wb') as f:
                    f.write(shx_file.getvalue())
                
                dbf_path = os.path.join(tmp_dir, dbf_file.name)
                with open(dbf_path, 'wb') as f:
                    f.write(dbf_file.getvalue())
                
                if prj_file:
                    prj_path = os.path.join(tmp_dir, prj_file.name)
                    with open(prj_path, 'wb') as f:
                        f.write(prj_file.getvalue())

                # Carregar dados
                geo_data = load_geodata(shp_path)
                project_data = load_project_data(csv_file)
        else:
            st.warning("Por favor, carregue todos os arquivos necessários (CSV, SHP, SHX, DBF)")
            return None, None
    else:
        # Usando caminhos fixos - AJUSTE ESTES CAMINHOS PARA OS SEUS ARQUIVOS
        try:
            shapefile_path = "data/ES_Municipios_2024.shp"  # AJUSTE ESTE CAMINHO
            csv_path = "data/df_bandas.csv"  # AJUSTE SE NECESSÁRIO
        
            geo_data = load_geodata('data/ES_Municipios_2024.shp')
            project_data = load_project_data('data/df_bandas.csv')
        except Exception as e:
            st.error(f"Erro ao carregar arquivos fixos: {e}")
            return None, None

    return geo_data, project_data

geo_data, project_data = run_data_loading()

# Verificar se os dados foram carregados corretamente
st.sidebar.subheader("Pré-visualização dos Dados")
if geo_data is not None and st.sidebar.checkbox("Mostrar dados geográficos"):
    st.sidebar.write(geo_data.head())

if project_data is not None and st.sidebar.checkbox("Mostrar dados dos projetos"):
    st.sidebar.write(project_data.head())

st.text("Quantidade de Estudantes Bandas:")
        

with col2:
    #st.subheader("Orquestra de Violões nas Escolas")
    st.markdown(
    """
    <h1 style='font-size:20px; color:#808000;'>
        Projeto Orquestra de Violões nas Escolas
    </h1>
    """,
    unsafe_allow_html=True
)
    st.image("fotos/violões.jpeg", caption="violões")
    with st.container(border=True,horizontal=True):
     st.text("Quantidade de Escolas Violões:")
     st.text("Quantidade de Estudantes Violões:")

col3, col4=st.columns([0.50,0.50])

with col3:
    #col3.subheader("Projeto Corais nas Escolas")
    st.markdown(
    """
    <h1 style='font-size:20px; color:#808000;'>
        Projeto Corais nas Escolas
    </h1>
    """,
    unsafe_allow_html=True
)
    st.image("fotos/coral.jpeg", caption="coral")
    with st.container(border=True,horizontal=True):
     st.text("Quantidade de Escolas Corais:")
     st.text("Quantidade de Estudantes Corais:")

with col4:
       #col4.subheader("Projeto Orquestra Sinfônica Jovem")
       st.markdown(
    """
    <h1 style='font-size:20px; color:#808000;'>
        Projeto Orquestra Sinfônica Jovem
    </h1>
    """,
    unsafe_allow_html=True
)
       st.image("fotos/sinfônica.jpeg", caption="sinfônica")
       with st.container(border=True,horizontal=True):
        st.text("Quantidade de Escolas Sinfônica:")
        st.text("Quantidade de Estudantes Sinfônica:")