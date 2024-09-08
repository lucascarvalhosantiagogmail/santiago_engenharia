import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path
from PIL import Image

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
page_title="Plataforma Santiago Engenharia",
page_icon="https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
layout="wide")


# TÍTULO DA PÁGINA
st.title("CONSULTORIA")
st.header("Empresa: Engenharia LTDA")
st.logo(r"https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

path = Path(__file__).parent.parent
    
df_data = pd.read_excel(path / "dataset" / "Planilha.xlsx", sheet_name="fConsultoria")
df_data["Data de visita técnica"] = pd.to_datetime(df_data["Data de visita técnica"]).dt.date
df_data = df_data.set_index("Data de visita técnica")


licencas = list(df_data["Código Licença"].unique())
calendario = list(df_data.index.unique())

licencas_selecionadas = st.sidebar.multiselect("Selecione a licença", licencas, licencas)
datas_selecionadas = st.sidebar.multiselect("Selecione as datas", calendario, calendario) 

col1, col2 = st.sidebar.columns(2)
status_filtrar = col1.button("Filtrar")


if status_filtrar:
    df_filtrado = df_data[(df_data["Código Licença"].isin(licencas_selecionadas)) &
                      (df_data.index.isin(datas_selecionadas))]
else:
    df_filtrado = df_data
    
st.dataframe(df_filtrado)

caminho_imagens = path / "dataset" / "Imagens"

def exibir_imagens(data_visita):
    for i in range(1, 5):  # Supondo que você tenha 4 imagens por visita
        imagem_path = caminho_imagens / f"{data_visita}_imagem{i}.jpg"  # Ajuste a extensão conforme necessário
        if imagem_path.exists():
            imagem = Image.open(imagem_path)
            st.image(imagem, caption=f"Imagem {i} - {data_visita}", use_column_width=True)

# Exibir as imagens associadas à data selecionada
for data_visita in datas_selecionadas:
    exibir_imagens(data_visita)



















st.divider()
st.sidebar.markdown("Desenvolvido por Santiago Engenharia (https://santiagoengenharia.com)")