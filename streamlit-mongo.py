import streamlit as st
from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.2"
)  
db = client["meta_db"]
collection = db["metas"]

def buscar_todos_produtos():
    return collection.find()

def converter_para_dataframe():
    produtos = buscar_todos_produtos()
    lista_produtos = []
    for produto in produtos:
        lista_produtos.append({
            "Nome": produto.get("nome"),
            "API": produto.get("api"),
            "Meta CB": produto.get("meta_cb"),
            "Meta EX": produto.get("meta_ex"),
            "Meta PF": produto.get("meta_pf"),
            "Observações": produto.get("observacoes")
        })
    
    df = pd.DataFrame(lista_produtos)
    return df

page = st.sidebar.selectbox("Navegar", ["Adicionar Meta", "Editar Meta", "Listar Metas em Tabela (Excel)"])

if page == "Adicionar Meta":
    st.title("Cadastro de Metas com MongoDB")

    st.header("Adicionar Nova Meta")
    with st.form(key='produto_form'):
        nome = st.text_input("Nome do Produto")
        api = st.text_input("API")
        meta_cb = st.text_input("Meta CB")
        meta_ex = st.text_input("Meta EX")
        meta_pf = st.text_input("Meta PF")
        observacoes = st.text_area("Observações Gerais")
        
        submit_button = st.form_submit_button("Adicionar Produto")

    if submit_button:
        if nome and api and meta_cb and meta_ex and meta_pf:
            produto = {
                "nome": nome,
                "api": api,
                "meta_cb": meta_cb,
                "meta_ex": meta_ex,
                "meta_pf": meta_pf,
                "observacoes": observacoes
            }
            collection.insert_one(produto)
            st.success("Meta adicionada com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

elif page == "Editar Meta":
    st.title("Editar Meta Existente")

    nome_produto_busca = st.text_input("Digite o nome do produto que deseja editar:")

    if st.button("Buscar Produto"):
        produto = collection.find_one({"nome": nome_produto_busca})

        if produto:
            st.success(f"Produto '{nome_produto_busca}' encontrado! Edite os campos abaixo.")
            
            with st.form(key='editar_produto_form'):
                novo_nome = st.text_input("Nome do Produto", value=produto['nome'])
                nova_api = st.text_input("API", value=produto['api'])
                nova_meta_cb = st.text_input("Meta CB", value=produto['meta_cb'])
                nova_meta_ex = st.text_input("Meta EX", value=produto['meta_ex'])
                nova_meta_pf = st.text_input("Meta PF", value=produto['meta_pf'])
                novas_observacoes = st.text_area("Observações Gerais", value=produto['observacoes'])
                
                atualizar_button = st.form_submit_button("Atualizar Produto")

            if atualizar_button:
                if novo_nome and nova_api and nova_meta_cb and nova_meta_ex and nova_meta_pf:
                    collection.update_one({"nome": nome_produto_busca}, {"$set": {
                        "nome": novo_nome,
                        "api": nova_api,
                        "meta_cb": nova_meta_cb,
                        "meta_ex": nova_meta_ex,
                        "meta_pf": nova_meta_pf,
                        "observacoes": novas_observacoes
                    }})
                    st.success(f"Produto '{novo_nome}' atualizado com sucesso!")
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
        else:
            st.error(f"Produto '{nome_produto_busca}' não encontrado.")

elif page == "Listar Metas em Tabela (Excel)":
    st.title("Listar Metas em Tabela")

    df_produtos = converter_para_dataframe()

    st.dataframe(df_produtos)
    csv = df_produtos.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='produtos.csv',
        mime='text/csv',
    )
