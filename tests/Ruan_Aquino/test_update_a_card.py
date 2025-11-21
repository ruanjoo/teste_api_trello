import pytest
import requests
import os
import time
from pytest_bdd import scenario, given, when, then, parsers
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# -----------------------------------------------------------
# Fixtures (Contexto Compartilhado)
# -----------------------------------------------------------
@pytest.fixture
def context():
    """
    Dicionário para compartilhar dados entre os passos (steps).
    Armazena a resposta da API e os dados enviados para comparação.
    """
    return {}

# -----------------------------------------------------------
# Ligação com o arquivo .feature
# -----------------------------------------------------------
@scenario('update_a_card.feature', 'Atualizar nome e descrição de um cartão com sucesso')

def test_update_card():
    """A função de teste fica vazia, pois o pytest-bdd orquestra os passos."""
    pass

# -----------------------------------------------------------
# Implementação dos Steps (Passos)
# -----------------------------------------------------------

@given("que possuo credenciais válidas e o ID de um cartão existente")
def setup_credentials(context):
    context['base_url'] = os.getenv("TRELLO_BASE_URL")
    context['card_id'] = os.getenv("STABLE_CARD_ID")
    context['auth'] = {
        "key": os.getenv("TRELLO_KEY"),
        "token": os.getenv("TRELLO_TOKEN")
    }

@when("eu envio uma requisição PUT para atualizar o nome e a descrição")
def send_update_request(context):
    # Gerar dados dinâmicos
    timestamp = int(time.time())
    novo_nome = f"Card BDD {timestamp}"
    nova_desc = f"Descrição BDD em {timestamp}"
    
    # Salva no contexto para conferir depois no assert
    context['input_data'] = {
        "name": novo_nome,
        "desc": nova_desc
    }
    
    url = f"{context['base_url']}/cards/{context['card_id']}"
    
    # Monta payload (Auth + Dados)
    payload = {**context['auth'], **context['input_data']}
    
    # Realiza a requisição
    response = requests.put(url, params=payload)
    context['response'] = response

@then("o código de status da resposta deve ser 200")
def check_status_code(context):
    assert context['response'].status_code == 200

@then("os dados retornados devem corresponder aos novos valores enviados")
def check_response_data(context):
    data = context['response'].json()
    expected = context['input_data']
    
    assert data["name"] == expected["name"]
    assert data["desc"] == expected["desc"]