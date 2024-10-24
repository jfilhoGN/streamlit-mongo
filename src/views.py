import streamlit as st
import pandas as pd
from src.mongo_db import adicionar_produto, buscar_produto_pelo_nome, atualizar_produto, buscar_todos_produtos

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

def pagina_adicionar_meta():
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
            adicionar_produto(produto)
            st.success("Meta adicionada com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")


def pagina_editar_meta():
    st.title("Editar Meta Existente")
    
    nome_produto_busca = st.text_input("Digite o nome do produto que deseja editar:")

    if st.button("Buscar Produto"):
        produto = buscar_produto_pelo_nome(nome_produto_busca)

        if produto:
            st.success(f"Produto '{nome_produto_busca}' encontrado! Edite os campos abaixo.")
            
            with st.form(key='editar_produto_form'):
                novo_nome = st.text_input("Nome do Produto", value=produto.get('nome', ''))
                nova_api = st.text_input("API", value=produto.get('api', ''))
                nova_meta_cb = st.text_input("Meta CB", value=produto.get('meta_cb', ''))
                nova_meta_ex = st.text_input("Meta EX", value=produto.get('meta_ex', ''))
                nova_meta_pf = st.text_input("Meta PF", value=produto.get('meta_pf', ''))
                novas_observacoes = st.text_area("Observações Gerais", value=produto.get('observacoes', ''))
                
                atualizar_button = st.form_submit_button("Atualizar Produto")

            if atualizar_button:
                dados_atualizados = {
                    "nome": novo_nome if novo_nome else None,
                    "api": nova_api if nova_api else None,
                    "meta_cb": nova_meta_cb if nova_meta_cb else None,
                    "meta_ex": nova_meta_ex if nova_meta_ex else None,
                    "meta_pf": nova_meta_pf if nova_meta_pf else None,
                    "observacoes": novas_observacoes if novas_observacoes else None
                }
                
                atualizar_produto(nome_produto_busca, dados_atualizados)
                st.success(f"Produto '{novo_nome or nome_produto_busca}' atualizado com sucesso!")
        else:
            st.error(f"Produto '{nome_produto_busca}' não encontrado.")


def pagina_listar_metas():
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
