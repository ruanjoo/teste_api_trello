import requests
import pytest
import os
from pathlib import Path 
from dotenv import load_dotenv
from pytest_bdd import scenario, given, when, then


arquivo_env = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(arquivo_env)

# Configurações
BASE = os.getenv("TRELLO_BASE_URL")
STABLE_CARD_ID = os.getenv("STABLE_CARD_ID")
AUTH = {
    "key": os.getenv("TRELLO_KEY"), 
    "token": os.getenv("TRELLO_TOKEN")
}

# Liga o teste ao arquivo .feature 
@scenario('delete_action.feature', 'Deletar um comentário existente com sucesso')
def test_delete_action():
    pass

# TC Deletar um comentário existente com sucesso
@pytest.fixture
def context():
    return {}

@given("que existe um comentário criado em um cartão")
def setup_comentario(context):
    url = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    r = requests.post(url, params={**AUTH, "text": "BDD Test"})
    context['action_id'] = r.json()["id"]

@when('eu envio uma requisição DELETE para o endpoint "/actions/{id}"')
def delete_comentario(context):
    action_id = context['action_id']
    url = f"{BASE}/actions/{action_id}"
    context['response'] = requests.delete(url, params=AUTH)

@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("o comentário não deve mais ser encontrado ao consultar a API")
def verificar_delecao_real(context):
    action_id = context['action_id']
    url = f"{BASE}/actions/{action_id}"
    r_check = requests.get(url, params=AUTH)
    assert r_check.status_code == 404