import pytest
import requests
import os
from pytest_bdd import scenario, given, when, then, parsers
from dotenv import load_dotenv

# --- CONFIGURAÇÕES ---
load_dotenv()
BASE = os.getenv("TRELLO_BASE_URL")     # Ex: https://api.trello.com/1
STABLE_CARD_ID = os.getenv("STABLE_CARD_ID")
AUTH = {
    "key": os.getenv("TRELLO_KEY"),
    "token": os.getenv("TRELLO_TOKEN")
}

# --- LIGAÇÃO COM O ARQUIVO FEATURE ---
@scenario('get_an_specific_field_on_an_action.feature', 'Validar o retorno do campo "type" via URL direta')
def test_action_field_path():
    pass

# --- FIXTURE DE CONTEXTO ---
@pytest.fixture
def context():
    return {}

# --- FIXTURE DE SETUP/TEARDOWN ---
@pytest.fixture
def action_id_temporaria():
    # 1. SETUP: Cria um comentário para termos um ID de Action válido
    url = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    payload = {**AUTH, "text": "Teste de Path Parameter"}
    r = requests.post(url, params=payload)
    assert r.status_code == 200
    
    id_action = r.json()["id"]
    yield id_action # Entrega o ID para o teste
    
    # 2. TEARDOWN: Limpa a sujeira
    requests.delete(f"{BASE}/actions/{id_action}", params=AUTH)

# --- STEPS ---

@given("que eu tenho credenciais válidas do Trello")
def check_creds():
    assert AUTH["key"] and AUTH["token"]

@given("existe um comentário recém-criado no card padrão")
def setup_action(context, action_id_temporaria):
    context["action_id"] = action_id_temporaria

# --- AQUI ESTÁ A MUDANÇA PRINCIPAL ---
@when(parsers.parse('eu faço um GET na rota específica "/actions/{{id}}/{{field}}" buscando o campo "{campo}"'))
def get_field_via_path(context, campo):
    action_id = context["action_id"]
    
    # IMPLEMENTAÇÃO EXATA DA DOCUMENTAÇÃO:
    # A url é montada com o campo no final: .../actions/ID/CAMPO
    url = f"{BASE}/actions/{action_id}/{campo}"
    
    # Note que 'params' agora tem APENAS a autenticação.
    # Não passamos 'fields=' aqui, pois o field já está na URL.
    response = requests.get(url, params=AUTH)
    
    context["response"] = response

@then(parsers.parse('o status code da resposta deve ser {status_code:d}'))
def check_status(context, status_code):
    assert context["response"].status_code == status_code

@then(parsers.parse('o JSON de resposta deve conter a chave "{chave_esperada}" com o valor "{valor_esperado}"'))
def check_json_value(context, chave_esperada, valor_esperado):
    data = context["response"].json()
    
    # Debug para você ver o retorno no console se falhar
    print(f"Retorno da API: {data}")
    
    assert chave_esperada in data
    assert data[chave_esperada] == valor_esperado