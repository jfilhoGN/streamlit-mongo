from pymongo import MongoClient

# Conexão com o MongoDB
def conectar_mongo():
    client = MongoClient(
        "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.2"
    )
    db = client["meta_db"]
    collection = db["metas"]
    return collection

# Função para buscar todos os produtos/metas
def buscar_todos_produtos():
    collection = conectar_mongo()
    return collection.find()

# Função para adicionar um produto/meta no MongoDB
def adicionar_produto(produto):
    collection = conectar_mongo()
    collection.insert_one(produto)

# Função para buscar um produto/meta pelo nome
def buscar_produto_pelo_nome(nome):
    collection = conectar_mongo()
    return collection.find_one({"nome": nome})

# Função para atualizar apenas os campos modificados
def atualizar_produto(nome_produto_busca, dados_atualizados):
    collection = conectar_mongo()
    
    # Remove campos com valor None (não modificados)
    dados_atualizados = {k: v for k, v in dados_atualizados.items() if v is not None}

    # Atualiza apenas os campos que foram modificados
    if dados_atualizados:
        collection.update_one({"nome": nome_produto_busca}, {"$set": dados_atualizados})
