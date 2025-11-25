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
@scenario('get_specific_sticker.feature', 'Buscar um sticker especifico pelo ID')
def test_get_specific_sticker():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE: SETUP (CRIAR TUDO) & TEARDOWN (LIMPAR TUDO) ---
@pytest.fixture
def setup_full_environment(context):
    """
    Cria a cadeia completa: Board -> List -> Card -> Sticker.
    Isso é necessário para termos IDs válidos para consultar.
    No final, deleta o Board.
    """
    print("\n[SETUP] Construindo ambiente de teste...")

    # 1. CRIAR BOARD
    r_board = requests.post(f"{BASE_URL}/boards", params={**AUTH, "name": "Specific Sticker Test", "defaultLists": "false"})
    assert r_board.status_code == 200
    board_id = r_board.json()["id"]
    context['board_id'] = board_id

    try:
        # 2. CRIAR LISTA
        r_list = requests.post(f"{BASE_URL}/lists", params={**AUTH, "name": "Lista Sticker", "idBoard": board_id})
        list_id = r_list.json()["id"]

        # 3. CRIAR CARTÃO
        r_card = requests.post(f"{BASE_URL}/cards", params={**AUTH, "name": "Cartão do Sticker", "idList": list_id})
        card_id = r_card.json()["id"]
        context['card_id'] = card_id

        # 4. CRIAR STICKER
        sticker_payload = {
            "image": "check", # Vamos usar o 'check' desta vez
            "top": 50,
            "left": 50,
            "zIndex": 1
        }
        url_create_sticker = f"{BASE_URL}/cards/{card_id}/stickers"
        r_sticker = requests.post(url_create_sticker, params={**AUTH, **sticker_payload})
        assert r_sticker.status_code == 200
        
        sticker_data = r_sticker.json()
        context['sticker_id'] = sticker_data["id"]
        context['sticker_image'] = sticker_data["image"]
        
        print(f"[SETUP] Sticker criado! ID: {context['sticker_id']} no Card: {card_id}")

        # --- O TESTE RODA AQUI ---
        yield 

    finally:
        # --- TEARDOWN ---
        print(f"\n[TEARDOWN] Deletando Board {board_id}...")
        requests.delete(f"{BASE_URL}/boards/{board_id}", params=AUTH)

# --- PASSOS DO BDD ---

@given("que preparei um cartao e adicionei um sticker nele")
def check_setup(context, setup_full_environment):
    # Garante que a fixture rodou
    assert context.get('sticker_id') is not None
    assert context.get('card_id') is not None

@when("eu envio uma requisicao GET para buscar esse sticker especifico")
def get_specific_sticker_request(context):
    card_id = context['card_id']
    sticker_id = context['sticker_id']
    
    # Endpoint alvo: GET /cards/{id}/stickers/{idSticker}
    url = f"{BASE_URL}/cards/{card_id}/stickers/{sticker_id}"
    
    print(f"[TEST] Buscando sticker específico: {sticker_id}")
    context['response'] = requests.get(url, params=AUTH)

@then("o status code da resposta deve ser 200")
def check_status_200(context):
    assert context['response'].status_code == 200, \
        f"Erro ao buscar sticker: {context['response'].text}"

@then("a resposta deve conter o ID e a imagem do sticker criado")
def check_sticker_details(context):
    data = context['response'].json()
    
    # Valida se o objeto retornado é exatamente o que criamos
    assert data['id'] == context['sticker_id']
    assert data['image'] == context['sticker_image']
    print("[SUCCESS] Sticker validado com sucesso.")