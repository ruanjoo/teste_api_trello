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
@scenario('update_sticker.feature', 'Atualizar a posicao de um sticker existente')
def test_update_sticker():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE: SETUP (CRIAR TUDO) & TEARDOWN (LIMPAR TUDO) ---
@pytest.fixture
def setup_full_environment(context):
    """
    Cria a infraestrutura completa para ter um sticker editável:
    Board -> List -> Card -> Sticker (Posição 0,0)
    """
    print("\n[SETUP] Construindo ambiente para Update...")

    # 1. CRIAR BOARD
    r_board = requests.post(f"{BASE_URL}/boards", params={**AUTH, "name": "Sticker Update Test", "defaultLists": "false"})
    assert r_board.status_code == 200
    board_id = r_board.json()["id"]
    context['board_id'] = board_id

    try:
        # 2. CRIAR LISTA
        r_list = requests.post(f"{BASE_URL}/lists", params={**AUTH, "name": "Lista Update", "idBoard": board_id})
        list_id = r_list.json()["id"]

        # 3. CRIAR CARTÃO
        r_card = requests.post(f"{BASE_URL}/cards", params={**AUTH, "name": "Cartão para Mover Sticker", "idList": list_id})
        card_id = r_card.json()["id"]
        context['card_id'] = card_id

        # 4. CRIAR STICKER ORIGINAL
        # Criamos na posição (0, 0) com zIndex 1
        sticker_payload = {
            "image": "check", 
            "top": 0,
            "left": 0,
            "zIndex": 1
        }
        url_create = f"{BASE_URL}/cards/{card_id}/stickers"
        r_sticker = requests.post(url_create, params={**AUTH, **sticker_payload})
        assert r_sticker.status_code == 200
        
        context['sticker_id'] = r_sticker.json()["id"]
        print(f"[SETUP] Sticker criado na posição (0,0). ID: {context['sticker_id']}")

        # --- O TESTE RODA AQUI ---
        yield 

    finally:
        # --- TEARDOWN ---
        print(f"\n[TEARDOWN] Deletando Board {board_id}...")
        requests.delete(f"{BASE_URL}/boards/{board_id}", params=AUTH)

# --- PASSOS DO BDD ---

@given("que preparei um cartao com um sticker original na posicao zero")
def check_setup(context, setup_full_environment):
    # A fixture já rodou e criou tudo
    assert context.get('sticker_id') is not None

@when("eu envio uma requisicao PUT para mover o sticker para novas coordenadas")
def update_sticker_request(context):
    card_id = context['card_id']
    sticker_id = context['sticker_id']
    
    # Endpoint alvo: PUT /cards/{id}/stickers/{idSticker}
    url = f"{BASE_URL}/cards/{card_id}/stickers/{sticker_id}"
    
    # Novos valores para atualizar
    context['new_top'] = 50
    context['new_left'] = 80
    context['new_zIndex'] = 2
    
    # Documentação diz: Query Parameters. Então vai no 'params'.
    payload = {
        "top": context['new_top'],
        "left": context['new_left'],
        "zIndex": context['new_zIndex']
    }
    
    print(f"[TEST] Movendo sticker para: {payload}")
    context['response'] = requests.put(url, params={**AUTH, **payload})

@then("o status code da resposta deve ser 200")
def check_status_200(context):
    assert context['response'].status_code == 200, \
        f"Erro ao atualizar: {context['response'].text}"

@then("a resposta deve conter as novas coordenadas atualizadas")
def check_updated_values(context):
    data = context['response'].json()
    
    # Valida se a resposta imediata reflete a mudança
    assert data['top'] == context['new_top']
    assert data['left'] == context['new_left']
    assert data['zIndex'] == context['new_zIndex']
    
    # Validação Extra: GET para confirmar persistência
    card_id = context['card_id']
    sticker_id = context['sticker_id']
    url_check = f"{BASE_URL}/cards/{card_id}/stickers/{sticker_id}"
    
    r_check = requests.get(url_check, params=AUTH)
    data_persistido = r_check.json()
    
    assert data_persistido['top'] == context['new_top']
    assert data_persistido['left'] == context['new_left']
    
    print("[SUCCESS] Sticker movido e validado com sucesso.")