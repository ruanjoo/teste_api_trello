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
@scenario('get_card_stickers.feature', 'Buscar stickers anexados a um cartao com sucesso')
def test_get_card_stickers():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE MESTRE: SETUP & TEARDOWN ---
@pytest.fixture
def setup_full_environment(context):
    """
    Constrói a hierarquia completa:
    Board -> List -> Card -> Sticker
    E deleta o Board no final.
    """
    print("\n[SETUP] Iniciando construção do ambiente...")

    # 1. CRIAR BOARD
    r_board = requests.post(f"{BASE_URL}/boards", params={**AUTH, "name": "Sticker Test Board", "defaultLists": "false"})
    assert r_board.status_code == 200
    board_id = r_board.json()["id"]
    context['board_id'] = board_id

    try:
        # 2. CRIAR LISTA
        r_list = requests.post(f"{BASE_URL}/lists", params={**AUTH, "name": "Lista Sticker", "idBoard": board_id})
        list_id = r_list.json()["id"]

        # 3. CRIAR CARTÃO
        r_card = requests.post(f"{BASE_URL}/cards", params={**AUTH, "name": "Cartão com Adesivo", "idList": list_id})
        card_id = r_card.json()["id"]
        context['card_id'] = card_id

        # 4. ADICIONAR STICKER (Para ter o que buscar no GET)
        # O Trello exige image, top, left e zIndex para criar um sticker
        sticker_payload = {
            "image": "star", # Imagens válidas: star, heart, check, warning, etc.
            "top": 0,
            "left": 0,
            "zIndex": 1
        }
        url_sticker = f"{BASE_URL}/cards/{card_id}/stickers"
        r_sticker = requests.post(url_sticker, params={**AUTH, **sticker_payload})
        assert r_sticker.status_code == 200
        
        sticker_data = r_sticker.json()
        context['sticker_id'] = sticker_data["id"]
        context['sticker_image'] = sticker_data["image"]
        print(f"[SETUP] Ambiente pronto. Sticker 'star' criado no cartão {card_id}")

        # --- O TESTE RODA AQUI ---
        yield 

    finally:
        # --- TEARDOWN (LIMPEZA) ---
        # Deletar o Board apaga Listas, Cartões e Stickers automaticamente
        print(f"\n[TEARDOWN] Deletando Board {board_id}...")
        requests.delete(f"{BASE_URL}/boards/{board_id}", params=AUTH)

# --- PASSOS DO BDD ---

@given("que preparei um cartao com um sticker anexado")
def check_setup(context, setup_full_environment):
    # Apenas invocar a fixture garante que tudo foi criado
    assert context.get('card_id') is not None
    assert context.get('sticker_id') is not None

@when("eu busco a lista de stickers desse cartao")
def get_stickers_request(context):
    card_id = context['card_id']
    
    # Endpoint alvo: GET /cards/{id}/stickers
    url = f"{BASE_URL}/cards/{card_id}/stickers"
    
    print(f"[TEST] Buscando stickers do cartão: {card_id}")
    context['response'] = requests.get(url, params=AUTH)

@then("o status code da resposta deve ser 200")
def check_status_200(context):
    assert context['response'].status_code == 200, \
        f"Erro: {context['response'].text}"

@then('a resposta deve conter o sticker "star" que foi criado')
def check_sticker_content(context):
    stickers_list = context['response'].json()
    
    # Validações
    assert isinstance(stickers_list, list), "A resposta deveria ser uma lista"
    assert len(stickers_list) > 0, "A lista de stickers voltou vazia"
    
    # Procura o sticker criado dentro da lista retornada
    sticker_encontrado = False
    for sticker in stickers_list:
        if sticker['id'] == context['sticker_id'] and sticker['image'] == "star":
            sticker_encontrado = True
            break
            
    assert sticker_encontrado, "O sticker criado não foi encontrado na resposta da API"