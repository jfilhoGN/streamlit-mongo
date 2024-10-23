from pymongo import MongoClient

def conectar_mongo():
    client = MongoClient(
        "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.2"
    )
    db = client["meta_db"]
    collection = db["metas"]
    return collection

def buscar_todos_produtos():
    collection = conectar_mongo()
    return collection.find()

def adicionar_produto(produto):
    collection = conectar_mongo()
    collection.insert_one(produto)

def buscar_produto_pelo_nome(nome):
    collection = conectar_mongo()
    return collection.find_one({"nome": nome})

def atualizar_produto(nome_produto_busca, dados_atualizados):
    collection = conectar_mongo()
    
    dados_atualizados = {k: v for k, v in dados_atualizados.items() if v is not None}

    if dados_atualizados:
        collection.update_one({"nome": nome_produto_busca}, {"$set": dados_atualizados})
