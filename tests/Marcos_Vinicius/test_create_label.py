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
@scenario('create_label.feature', 'Criar uma nova etiqueta no quadro com sucesso')
def test_create_label():
    pass

@pytest.fixture
def context():
    return {}

@given("que possuo um ID de quadro valido para criar a etiqueta")
def setup_board_id(context):
    # Precisamos do idBoard para criar uma label.
    # Buscamos ele através do cartão de teste que já temos no .env
    url_card = f"{BASE}/cards/{STABLE_CARD_ID}"
    r = requests.get(url_card, params=AUTH)
    
    # Armazena o ID do Board no contexto para usar no passo When
    context['board_id'] = r.json()["idBoard"]

@when('eu envio uma requisição POST para o endpoint "/labels" com nome e cor')
def create_label_request(context):
    url = f"{BASE}/labels"
    
    # Dados da nova etiqueta
    context['sent_name'] = "Label Criada via POST"
    context['sent_color'] = "lime"
    board_id = context['board_id']
    
    # Monta a query string com os dados obrigatórios (name, color, idBoard)
    query_params = {
        **AUTH,
        "name": context['sent_name'],
        "color": context['sent_color'],
        "idBoard": board_id
    }
    
    context['response'] = requests.post(url, params=query_params)

@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("a resposta deve conter o ID, nome e cor da nova etiqueta")
def verificar_criacao(context):
    response_data = context['response'].json()
    
    # Verifica se os dados retornados batem com o que enviamos
    assert response_data['name'] == context['sent_name']
    assert response_data['color'] == context['sent_color']
    assert response_data['idBoard'] == context['board_id']
    
    # Verifica se gerou um ID (prova que foi salvo no banco)
    assert "id" in response_data