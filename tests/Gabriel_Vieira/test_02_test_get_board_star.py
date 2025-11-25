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
@scenario('get_board_star.feature', 'Buscar um board star especifico criado dinamicamente')
def test_get_board_star():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE: SETUP & TEARDOWN COMPLETO ---
@pytest.fixture
def setup_cenario(context):
    """
    1. Cria um Board.
    2. Cria um Star (Favorito) para esse Board.
    3. Entrega o controle para o teste.
    4. Deleta o Star.
    5. Deleta o Board.
    """
    # [PASSO 1] Criar Board Temporário
    print("\n[SETUP] Criando Board Temporário...")
    url_board = f"{BASE_URL}/boards/"
    payload_board = {"name": "Board Star Test BDD", "defaultLabels": "false"}
    r_board = requests.post(url_board, params={**AUTH, **payload_board})
    assert r_board.status_code == 200
    board_id = r_board.json()["id"]
    context['board_id'] = board_id

    # [PASSO 2] Criar o Star (Favoritar o Board)
    print(f"[SETUP] Favoritando o Board {board_id}...")
    url_star_create = f"{BASE_URL}/members/me/boardStars"
    payload_star = {
        "idBoard": board_id,
        "pos": "top"
    }
    # O endpoint de criar star exige JSON no corpo
    r_star = requests.post(url_star_create, params=AUTH, json=payload_star)
    assert r_star.status_code == 200
    star_id = r_star.json()["id"]
    context['star_id'] = star_id
    print(f"[SETUP] Star criado com ID: {star_id}")

    # --- O TESTE RODA AQUI ---
    yield 

    # [PASSO 3] Deletar o Star (Limpeza 1)
    print("\n[TEARDOWN] Deletando Star...")
    url_star_del = f"{BASE_URL}/members/me/boardStars/{star_id}"
    requests.delete(url_star_del, params=AUTH)

    # [PASSO 4] Deletar o Board (Limpeza 2)
    print(f"[TEARDOWN] Deletando Board {board_id}...")
    url_board_del = f"{BASE_URL}/boards/{board_id}"
    requests.delete(url_board_del, params=AUTH)

# --- STEPS DO BDD ---

@given("que eu criei um quadro e o favoritei para gerar um ID de star")
def validar_setup(context, setup_cenario):
    # Apenas invocar a fixture 'setup_cenario' já garante que tudo foi criado
    assert context.get('star_id') is not None
    assert context.get('board_id') is not None

@when("eu busco esse board star especifico pelo ID")
def get_request_star(context):
    star_id = context['star_id']
    # Endpoint alvo: /members/{id}/boardStars/{idStar}
    # Usamos 'me' como ID do membro para facilitar
    url = f"{BASE_URL}/members/me/boardStars/{star_id}"
    
    context['response'] = requests.get(url, params=AUTH)

@then("o status code da resposta deve ser 200")
def check_status(context):
    assert context['response'].status_code == 200, \
        f"Erro: {context['response'].text}"

@then("a resposta deve conter o ID do quadro correto")
def check_payload(context):
    data = context['response'].json()
    
    # Valida se o Star recuperado aponta para o Board que criamos
    assert data['id'] == context['star_id']
    assert data['idBoard'] == context['board_id']