import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import plotly.express as px 


# CARREGAR OS DADOS DA PLANILHA

if "data" not in st.session_state:
    all_sheets = pd.read_excel("dataset\Planilha.xlsx", sheet_name=None)
    df_data = pd.concat(all_sheets.values(), ignore_index=True, join="outer")
    df_data["Licença-Data de validade"] = pd.to_datetime(df_data["Licença-Data de validade"])
    st.session_state["data"] = df_data
    
else:
    df_data = st.session_state["data"]

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
page_title="Plataforma Santiago Engenharia",
page_icon= "https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
layout="wide"
)

# TÍTULO DA PÁGINA
st.title("CONTROLE DE LICENÇAS")
st.header("Empresa: Engenharia LTDA")
st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

# DESCRITIVO INICIAL
st.subheader("Número de Licenças: 2")
st.subheader("Código da licença 1: L-1234")
st.subheader("Código da licença 2: L-5678")

# INSERIR OPÇÃO PARA ESCOLHA DA LICENÇA
licenca = df_data["Código Licença"].unique()
licenca_selecionada = st.sidebar.selectbox("Licenças", licenca)

df_filtrado = df_data[df_data["Código Licença"] == licenca_selecionada]

contagem_por_data = df_filtrado.groupby("Licença-Data de validade")["Código Licença"].count().reset_index()

st.divider()

if licenca_selecionada == "L-1234":
    st.header("Licença L-1234")
else:
    st.header("Licença L-5678")

if not df_filtrado.empty:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Data de emissão da licença:", value=df_filtrado["Licença-Data de emissão"].iloc[0].strftime("%d/%m/%Y"))
    col2.metric(label="Data da validade da licença:", value=df_filtrado["Licença-Data de validade"].iloc[0].strftime("%d/%m/%Y"))
    col3.metric(label="Dias para vencimento:", value=int(df_filtrado["Dias restantes"].iloc[0]))
    col4.metric(label="Status:", value=df_filtrado["Status da licença"].iloc[0])
else:
    st.warning("Não há licença para a condição selecionada.")

st.divider()

# VENCIMENTO

st.subheader("Vencimento")

# CRIANDO CORES DAS BARRAS DO GRÁFICO

df_filtrado["Cor"] = df_filtrado["Status da licença"].map({
    "Dentro do prazo": "green",
    "Vencida": "red",
    "Renovar": "yellow"
})

# 1º GRÁFICO

contagem_por_data = contagem_por_data.merge(df_filtrado[["Licença-Data de validade", "Cor"]].drop_duplicates(), on="Licença-Data de validade", how="left") 



fig = px.bar(
    contagem_por_data,
    x="Licença-Data de validade",
    y="Código Licença",
    color="Cor",
    labels={"Licença-Data de validade": "Data de Validade", "Quantidade de licenças": "Número de Licenças"},
    template="plotly_dark",
    color_discrete_map={"green":"green","red":"red","yellow":"yellow"}
)

#CONFIGURANDO O TAMANHO DO GRÁFICO
fig.update_layout(
    width=600,
    height=400
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.plotly_chart(fig)

st.divider()
st.sidebar.markdown("Desenvolvido por Santiago Engenharia (https://santiagoengenharia.com)")