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
@scenario('get_label.feature', 'Obter uma etiqueta existente com sucesso')
def test_get_label():
    pass

# Fixture para o contexto compartilhado
@pytest.fixture
def context():
    return {}

@given("que existe uma etiqueta criada no quadro")
def setup_label(context):
    # Passo 1: Descobrir o ID do Board através do Cartão (para poder criar a label)
    url_card = f"{BASE}/cards/{STABLE_CARD_ID}"
    r_card = requests.get(url_card, params=AUTH)
    board_id = r_card.json()["idBoard"]
    
    # Passo 2: Criar a label nesse Board
    url_label = f"{BASE}/boards/{board_id}/labels"
    payload = {
        "name": "Label BDD Test",
        "color": "green"
    }
    # Mescla AUTH com o payload
    r = requests.post(url_label, params={**AUTH, **payload})
    
    # Guarda o ID e o Nome no contexto para validação posterior
    context['label_id'] = r.json()["id"]
    context['label_name'] = r.json()["name"]

@when('eu envio uma requisição GET para o endpoint "/labels/{id}"')
def get_label_request(context):
    label_id = context['label_id']
    url = f"{BASE}/labels/{label_id}"
    context['response'] = requests.get(url, params=AUTH)

@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("o corpo da resposta deve conter o nome correto da etiqueta")
def verificar_corpo_resposta(context):
    response_data = context['response'].json()
    # Valida se o nome retornado é igual ao nome criado no setup
    assert response_data['name'] == context['label_name']
    # Valida se o ID retornado é o mesmo que buscamos
    assert response_data['id'] == context['label_id']