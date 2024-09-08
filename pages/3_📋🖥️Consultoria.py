import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path
from PIL import Image

# FUNÇÃO QUE DEFINE A PARA A LOGO
def imagem(caminho):
    img = mpimg.imread(caminho)
    plt.axis("off")
    plt.imshow(img)

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
page_title="Plataforma Santiago Engenharia",
page_icon= imagem(r"C:\Users\User\Desktop\GitHub\santiago_engenharia\Santiago.png"),
layout="wide")


# TÍTULO DA PÁGINA
st.title("CONSULTORIA")
st.header("Empresa: Engenharia LTDA")
st.logo(r"C:\Users\User\Desktop\GitHub\santiago_engenharia\Santiago.png")

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