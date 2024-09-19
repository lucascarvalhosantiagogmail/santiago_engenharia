import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path

path = Path(__file__).parent.parent

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Plataforma Santiago Engenharia",
    page_icon="https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
    layout="wide"
)
st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

#CONTROLE DE LOGIN

if not st.session_state.get("logged_in", False):
    st.subheader("Você precisa fazer login para acessar este menu.")
    st.subheader("Volte para a página inicial.")
else:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.subheader("Logoff")
    with col2:
        if st.button("Sair"):
            st.session_state.logged_in = False
            st.session_state.page = "1_🌍Home" 
            st.write("Você foi desconectado. Clique [aqui](#/1_🌍Home) para voltar à página inicial.")



    # TÍTULO DA PÁGINA
    st.title("CONDICIONANTES AMBIENTAIS")
    st.header("Empresa: Engenharia LTDA")
    st.logo(r"https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")


    if "data" in st.session_state:
        df_data = st.session_state["data"]
        df_data = df_data.dropna(subset=["Número da condicionante",
                                        "Condicionantes ambientais",
                                        "Status das condicionantes",
                                        "Comentário",
                                        "Código Licença"])
        df_data = df_data[(df_data["Número da condicionante"] != "") &
                        (df_data["Condicionantes ambientais"] != "") &
                        (df_data["Status das condicionantes"] != "") &
                        (df_data["Comentário"] != "") &
                        (df_data["Código Licença"] != "") ]
        df_data = df_data.set_index("Número da condicionante")
        df_data = df_data[["Condicionantes ambientais",
                        "Status das condicionantes",
                        "Comentário",
                        "Código Licença"]]
        
            
        licencas = list(df_data["Código Licença"].unique())
        status = list(df_data["Status das condicionantes"].unique())

        licencas_selecionadas = st.sidebar.multiselect("Selecione a licença", licencas, licencas)
        status_selecionadas = st.sidebar.multiselect("Selecione o status", status, status)

        col1, col2 = st.sidebar.columns(2)
        status_filtrar = col1.button("Filtrar")
    
        if status_filtrar:
            df_filtrado = df_data[(df_data["Código Licença"].isin(licencas_selecionadas)) & 
                                df_data["Status das condicionantes"].isin(status_selecionadas)]
        else:
            df_filtrado = df_data
        
        col1, col2 = st.columns([2,1])

        with col1:
            st.dataframe(df_filtrado)
        
        with col2:
            status_counts = df_filtrado["Status das condicionantes"].value_counts()
            color_map = {
            "Regularizado": "green",
            "Acompanhamento": "yellow",
            "Não Regularizado": "red"}

            fig = px.pie(
                names=status_counts.index,
                values=status_counts.values,
                labels={"names": "Status", "values":"Quantidade"},
                color=status_counts.index,
                color_discrete_map=color_map,
                template="plotly_dark",
                hole=0.3

            )

            
            fig.update_layout(
                title={
                    "text": "Status das Condicionantes",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                }
            )
            st.plotly_chart(fig)


        total_condicionantes = len(df_filtrado)
        regularizado_count = df_filtrado["Status das condicionantes"].value_counts().get("Regularizado", 0)
        porcentagem_regularizado = (regularizado_count / total_condicionantes) * 100 if total_condicionantes > 0 else 0
        st.header(f"Desempenho Ambiental: {porcentagem_regularizado:.0f}%")
        st.subheader(f"Compreende-se neste cálculo que, {regularizado_count} itens das condicionantes da licença ambiental, do total de {total_condicionantes} itens, estão deferidos")
        
            

    else:
        st.write("Dados não correlacionados")

    st.divider()

    # FUNÇÃO QUE DEFINE A PARA A LOGO
        
    st.sidebar.image("Santiago.png", caption="Plataforma de Controle")
    st.sidebar.markdown("Desenvolvido por Santiago Engenharia (https://santiagoengenharia.com)")