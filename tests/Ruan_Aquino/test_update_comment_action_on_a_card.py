import requests
import pytest
import os
import time
from dotenv import load_dotenv

# Configurações
load_dotenv()
BASE = os.getenv("TRELLO_BASE_URL")
AUTH = {
    "key": os.getenv("TRELLO_KEY"),
    "token": os.getenv("TRELLO_TOKEN")
}

# -------------------------
# FIXTURE: O Grande Faxineiro
# -------------------------
@pytest.fixture
def board_temporario():
    # SETUP
    nome_board = f"Board_Teste_{int(time.time())}"
    r = requests.post(f"{BASE}/boards", params={**AUTH, "name": nome_board})
    assert r.status_code == 200
    board_id = r.json()["id"]
    
    yield board_id
    
    # TEARDOWN (O Trello apaga listas e cards automaticamente ao apagar o board)
    requests.delete(f"{BASE}/boards/{board_id}", params=AUTH)

def setup_cenario(board_id):
    # 1. Cria Lista
    r_lista = requests.post(f"{BASE}/lists", params={**AUTH, "name": "Lista 1", "idBoard": board_id})
    list_id = r_lista.json()["id"]
    
    # 2. Cria Card
    r_card = requests.post(f"{BASE}/cards", params={**AUTH, "name": "Card Teste", "idList": list_id})
    card_id = r_card.json()["id"]
    
    return card_id


##TC Atualizar um Comentário em um Card
@pytest.mark.integration
def test_lifecycle_comment_update(board_temporario):
    board_id = board_temporario
    
    card_id = setup_cenario(board_id)
    
    #Criar Comentário
    comentario_original = "Texto Inicial"
    r_post = requests.post(
        f"{BASE}/cards/{card_id}/actions/comments", 
        params={**AUTH, "text": comentario_original}
    )
    assert r_post.status_code == 200
    action_id = r_post.json()["id"]
    
    # Validação rápida da criação
    assert r_post.json()["data"]["text"] == comentario_original

    #Atualizar Comentário
    novo_texto = "Texto Atualizado - Sucesso"
    r_put = requests.put(
        f"{BASE}/cards/{card_id}/actions/{action_id}/comments", 
        params={**AUTH, "text": novo_texto}
    )
    assert r_put.status_code == 200

    #Verificar Atualização
    resp_json = r_put.json()
    
    # Se a chave não existir, o teste quebra aqui
    texto_retornado = resp_json["data"]["text"]
    assert texto_retornado == novo_texto
    