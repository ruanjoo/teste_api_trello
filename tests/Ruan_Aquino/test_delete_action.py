import requests
import pytest
import os
from pathlib import Path # <--- Importe isso
from dotenv import load_dotenv
from pytest_bdd import scenario, given, when, then

# --- CORREÇÃO DO DOTENV ---
# Isso garante que ele ache o .env na raiz do projeto (2 pastas acima do teste)
arquivo_env = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(arquivo_env)

# Configurações
BASE = os.getenv("TRELLO_BASE_URL")
STABLE_CARD_ID = os.getenv("STABLE_CARD_ID")
AUTH = {
    "key": os.getenv("TRELLO_KEY"), 
    "token": os.getenv("TRELLO_TOKEN")
}

# Verifica se carregou (Debug)
if not BASE or not STABLE_CARD_ID:
    raise ValueError(f"ERRO: Variáveis de ambiente não carregadas! Verifique o caminho: {arquivo_env}")
# Liga o teste ao arquivo .feature escrito acima
@scenario('delete_action.feature', 'Deletar um comentário existente com sucesso')
def test_delete_action():
    pass

# --- DADO ---
@pytest.fixture
def context():
    return {}

@given("que existe um comentário criado em um cartão")
def setup_comentario(context):
    # Cria o comentário (igual sua fixture)
    url = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    r = requests.post(url, params={**AUTH, "text": "BDD Test"})
    context['action_id'] = r.json()["id"]

# --- QUANDO ---
@when('eu envio uma requisição DELETE para o endpoint "/actions/{id}"')
def delete_comentario(context):
    action_id = context['action_id']
    url = f"{BASE}/actions/{action_id}"
    context['response'] = requests.delete(url, params=AUTH)

# --- ENTÃO ---
@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("o comentário não deve mais ser encontrado ao consultar a API")
def verificar_delecao_real(context):
    action_id = context['action_id']
    url = f"{BASE}/actions/{action_id}"
    r_check = requests.get(url, params=AUTH)
    assert r_check.status_code == 404