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
@scenario('delete_label.feature', 'Deletar uma etiqueta existente com sucesso')
def test_delete_label():
    pass

@pytest.fixture
def context():
    return {}

@given("que existe uma etiqueta criada no quadro para ser deletada")
def setup_label_to_delete(context):
    # 1. Busca o ID do Board através do cartão estável
    url_card = f"{BASE}/cards/{STABLE_CARD_ID}"
    r_card = requests.get(url_card, params=AUTH)
    board_id = r_card.json()["idBoard"]
    
    # 2. Cria uma label temporária para ser excluída
    url_label = f"{BASE}/boards/{board_id}/labels"
    payload = {
        "name": "Label To Delete",
        "color": "black"
    }
    r = requests.post(url_label, params={**AUTH, **payload})
    
    # Armazena o ID da label criada no contexto
    context['label_id'] = r.json()["id"]

@when('eu envio uma requisição DELETE para o endpoint "/labels/{id}"')
def delete_label_request(context):
    label_id = context['label_id']
    url = f"{BASE}/labels/{label_id}"
    
    # Executa o DELETE
    context['response'] = requests.delete(url, params=AUTH)

@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("a etiqueta não deve mais ser encontrada ao consultar a API")
def verificar_delecao_real(context):
    label_id = context['label_id']
    url = f"{BASE}/labels/{label_id}"
    
    # Tenta buscar a label deletada
    r_check = requests.get(url, params=AUTH)
    
    # O Trello retorna 404 Not Found se a label foi deletada com sucesso
    assert r_check.status_code == 404