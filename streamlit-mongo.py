import streamlit as st
from pymongo import MongoClient

client = MongoClient(
    "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.2"
)  
db = client["meta_db"]
collection = db["metas"]


def adicionar_meta(nome, api, meta_cb, meta_ex, meta_pf, observacoes):
    meta = {
        "nome": nome,
        "api": api,
        "meta_cb": meta_cb,
        "meta_ex": meta_ex,
        "meta_pf": meta_pf,
        "observacoes": observacoes,
    }
    collection.insert_one(meta)


def buscar_produto_por_nome(nome):
    return collection.find_one({"nome": nome})


def atualizar_produto(nome_original, nome, api, meta_cb, meta_ex, meta_pf, observacoes):
    query = {"nome": nome_original}
    novos_dados = {
        "$set": {
            "nome": nome,
            "api": api,
            "meta_cb": meta_cb,
            "meta_ex": meta_ex,
            "meta_pf": meta_pf,
            "observacoes": observacoes,
        }
    }
    collection.update_one(query, novos_dados)


def exibir_metas():
    produtos = collection.find()
    for produto in produtos:
        st.write(f"**Nome do Produto**: {produto['nome']}")
        st.write(f"**API**: {produto['api']}")
        st.write(f"**Meta CB**: {produto['meta_cb']}")
        st.write(f"**Meta EX**: {produto['meta_ex']}")
        st.write(f"**Meta PF**: {produto['meta_pf']}")
        st.write(f"**Observações Gerais**: {produto['observacoes']}")
        st.write("---")


st.title("Cadastro de Metas com MongoDB")

st.header("Adicionar Nova Meta")
with st.form(key="produto_form"):
    nome = st.text_input("Nome do Produto")
    api = st.text_input("API")
    meta_cb = st.text_input("Meta CB")
    meta_ex = st.text_input("Meta EX")
    meta_pf = st.text_input("Meta PF")
    observacoes = st.text_area("Observações Gerais")

    submit_button = st.form_submit_button("Adicionar Produto")

if submit_button:
    if nome and api and meta_cb and meta_ex and meta_pf:
        adicionar_meta(nome, api, meta_cb, meta_ex, meta_pf, observacoes)
        st.success("Meta adicionado com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos obrigatórios.")

st.header("Editar Meta Existente")

nome_produto_busca = st.text_input("Digite o nome do produto que deseja editar:")

if st.button("Buscar Produto"):
    produto = buscar_produto_por_nome(nome_produto_busca)

    if produto:
        st.success(
            f"Produto '{nome_produto_busca}' encontrado! Edite os campos abaixo."
        )

        with st.form(key="editar_produto_form"):
            novo_nome = st.text_input("Nome do Produto", value=produto["nome"])
            nova_api = st.text_input("API", value=produto["api"])
            nova_meta_cb = st.text_input("Meta CB", value=produto["meta_cb"])
            nova_meta_ex = st.text_input("Meta EX", value=produto["meta_ex"])
            nova_meta_pf = st.text_input("Meta PF", value=produto["meta_pf"])
            novas_observacoes = st.text_area(
                "Observações Gerais", value=produto["observacoes"]
            )

            atualizar_button = st.form_submit_button("Atualizar Produto")

        if atualizar_button:
            if (
                novo_nome
                and nova_api
                and nova_meta_cb
                and nova_meta_ex
                and nova_meta_pf
            ):
                atualizar_produto(
                    nome_produto_busca,
                    novo_nome,
                    nova_api,
                    nova_meta_cb,
                    nova_meta_ex,
                    nova_meta_pf,
                    novas_observacoes,
                )
                st.success(f"Produto '{novo_nome}' atualizado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")
    else:
        st.error(f"Produto '{nome_produto_busca}' não encontrado.")

st.subheader("Metas Cadastrados")
exibir_metas()
