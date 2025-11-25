import pytest
import requests
import os
from pytest_bdd import scenario, given, when, then
from dotenv import load_dotenv
from pathlib import Path

# Carrega ambiente
arquivo_env = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(arquivo_env)

BASE_URL = "https://api.trello.com/1"
AUTH = {
    "key": os.getenv("TRELLO_KEY"),
    "token": os.getenv("TRELLO_TOKEN")
}

# Liga o teste ao arquivo feature
@scenario('add_card_sticker.feature', 'Adicionar um sticker de coracao a um cartao criado dinamicamente')
def test_add_card_sticker():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE: SETUP (CRIAR AMBIENTE) & TEARDOWN (LIMPAR) ---
@pytest.fixture
def setup_card_environment(context):
    """
    Cria: Board -> List -> Card
    Para que possamos colar um sticker nesse card.
    No final, deleta o Board.
    """
    print("\n[SETUP] Construindo infraestrutura...")

    # 1. CRIAR BOARD
    r_board = requests.post(f"{BASE_URL}/boards", params={**AUTH, "name": "Sticker POST Test", "defaultLists": "false"})
    assert r_board.status_code == 200
    board_id = r_board.json()["id"]
    context['board_id'] = board_id

    try:
        # 2. CRIAR LISTA
        r_list = requests.post(f"{BASE_URL}/lists", params={**AUTH, "name": "Lista POST", "idBoard": board_id})
        list_id = r_list.json()["id"]

        # 3. CRIAR CARTÃO
        r_card = requests.post(f"{BASE_URL}/cards", params={**AUTH, "name": "Cartão Alvo", "idList": list_id})
        card_id = r_card.json()["id"]
        context['card_id'] = card_id
        
        print(f"[SETUP] Cartão criado com ID: {card_id}")

        # --- O TESTE RODA AQUI ---
        yield 

    finally:
        # --- LIMPEZA ---
        print(f"\n[TEARDOWN] Deletando Board {board_id}...")
        requests.delete(f"{BASE_URL}/boards/{board_id}", params=AUTH)

# --- PASSOS DO BDD ---

@given("que preparei um cartao para receber um sticker")
def check_setup(context, setup_card_environment):
    # Garante que o setup rodou e gerou um ID de cartão
    assert context.get('card_id') is not None

@when('eu envio uma requisicao POST para adicionar um sticker "heart" com coordenadas validas')
def post_sticker_request(context):
    card_id = context['card_id']
    
    # Endpoint alvo: POST /cards/{id}/stickers
    url = f"{BASE_URL}/cards/{card_id}/stickers"
    
    # Parâmetros obrigatórios segundo a documentação
    payload = {
        "image": "heart",   # Imagem do sticker
        "top": 0,           # Posição Y (0 a 100)
        "left": 0,          # Posição X (0 a 100)
        "zIndex": 1         # Camada (Inteiro)
    }
    
    # A documentação diz que são Query Parameters, então vão no 'params'
    print(f"[TEST] Adicionando sticker 'heart' ao cartão {card_id}...")
    context['response'] = requests.post(url, params={**AUTH, **payload})

@then("o status code da resposta deve ser 200")
def check_status_200(context):
    assert context['response'].status_code == 200, \
        f"Erro ao adicionar sticker: {context['response'].text}"

@then("a resposta deve conter o ID do sticker e a imagem correta")
def check_sticker_response(context):
    data = context['response'].json()
    
    # Validações
    assert "id" in data
    assert data['image'] == "heart"
    assert data['top'] == 0
    assert data['left'] == 0
    assert data['zIndex'] == 1
    
    print(f"[SUCCESS] Sticker criado com ID: {data['id']}")