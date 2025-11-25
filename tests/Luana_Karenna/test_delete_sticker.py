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
@scenario('delete_sticker.feature', 'Remover um sticker existente de um cartao')
def test_delete_sticker():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE: SETUP (CRIAR TUDO) & TEARDOWN (LIMPAR TUDO) ---
@pytest.fixture
def setup_full_environment(context):
    """
    Cria a infraestrutura completa para ter o que deletar:
    Board -> List -> Card -> Sticker
    """
    print("\n[SETUP] Construindo ambiente para Delete...")

    # 1. CRIAR BOARD
    r_board = requests.post(f"{BASE_URL}/boards", params={**AUTH, "name": "Sticker Delete Test", "defaultLists": "false"})
    assert r_board.status_code == 200
    board_id = r_board.json()["id"]
    context['board_id'] = board_id

    try:
        # 2. CRIAR LISTA
        r_list = requests.post(f"{BASE_URL}/lists", params={**AUTH, "name": "Lista Delete", "idBoard": board_id})
        list_id = r_list.json()["id"]

        # 3. CRIAR CARTÃO
        r_card = requests.post(f"{BASE_URL}/cards", params={**AUTH, "name": "Cartão Alvo", "idList": list_id})
        card_id = r_card.json()["id"]
        context['card_id'] = card_id

        # 4. CRIAR STICKER (Para ser deletado)
        sticker_payload = {
            "image": "heart", 
            "top": 20,
            "left": 20,
            "zIndex": 1
        }
        url_create = f"{BASE_URL}/cards/{card_id}/stickers"
        r_sticker = requests.post(url_create, params={**AUTH, **sticker_payload})
        assert r_sticker.status_code == 200
        
        context['sticker_id'] = r_sticker.json()["id"]
        print(f"[SETUP] Sticker criado para deleção. ID: {context['sticker_id']}")

        # --- O TESTE RODA AQUI ---
        yield 

    finally:
        # --- TEARDOWN ---
        print(f"\n[TEARDOWN] Deletando Board {board_id}...")
        requests.delete(f"{BASE_URL}/boards/{board_id}", params=AUTH)

# --- PASSOS DO BDD ---

@given("que preparei um cartao com um sticker para ser deletado")
def check_setup(context, setup_full_environment):
    # Garante que a fixture rodou
    assert context.get('sticker_id') is not None

@when("eu envio uma requisicao DELETE para remover esse sticker")
def delete_sticker_request(context):
    card_id = context['card_id']
    sticker_id = context['sticker_id']
    
    # Endpoint alvo: DELETE /cards/{id}/stickers/{idSticker}
    url = f"{BASE_URL}/cards/{card_id}/stickers/{sticker_id}"
    
    print(f"[TEST] Deletando sticker ID: {sticker_id}")
    context['response'] = requests.delete(url, params=AUTH)

@then("o status code da resposta deve ser 200")
def check_status_200(context):
    assert context['response'].status_code == 200, \
        f"Erro ao deletar: {context['response'].text}"

@then("o sticker nao deve mais ser encontrado no cartao")
def check_deleted_real(context):
    card_id = context['card_id']
    sticker_id = context['sticker_id']
    
    # Tenta buscar o sticker específico novamente
    url_check = f"{BASE_URL}/cards/{card_id}/stickers/{sticker_id}"
    
    r_check = requests.get(url_check, params=AUTH)
    
    # AJUSTE AQUI:
    # O Trello pode retornar 404 (Não Encontrado) ou 400 (ID Inválido/Não existe).
    # Ambos confirmam que o objeto foi deletado com sucesso.
    assert r_check.status_code in [404, 400], \
        f"Falha! O sticker ainda parece existir ou erro inesperado. Status: {r_check.status_code}"
    
    print(f"[SUCCESS] Sticker removido. API retornou: {r_check.status_code}")