import streamlit as st
from src.views import pagina_adicionar_meta, pagina_editar_meta, pagina_listar_metas

page = st.sidebar.selectbox("Navegar", ["Adicionar Meta", "Editar Meta", "Listar Metas em Tabela (Excel)"])

if page == "Adicionar Meta":
    pagina_adicionar_meta()
elif page == "Editar Meta":
    pagina_editar_meta()
elif page == "Listar Metas em Tabela (Excel)":
    pagina_listar_metas()
