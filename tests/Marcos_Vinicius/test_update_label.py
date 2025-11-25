import requests
import pytest
import os
import time
from pathlib import Path 
from dotenv import load_dotenv
from pytest_bdd import scenario, given, when, then

# Carrega as variáveis de ambiente
arquivo_env = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(arquivo_env)

# Configurações Globais
BASE = os.getenv("TRELLO_BASE_URL")
AUTH = {
    "key": os.getenv("TRELLO_KEY"), 
    "token": os.getenv("TRELLO_TOKEN")
}

# Liga o teste ao arquivo .feature
@scenario('update_label.feature', 'Atualizar uma etiqueta existente com sucesso')
def test_update_label():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE DE ISOLAMENTO (CRIA E DELETA BOARD) ---
@pytest.fixture
def board_temporario(context):
    # 1. SETUP: Criar Board
    url_create = f"{BASE}/boards/"
    payload = {
        "name": "Board Update Label Test",
        "defaultLabels": "false",
        "defaultLists": "false"
    }
    r = requests.post(url_create, params={**AUTH, **payload})
    assert r.status_code == 200
    
    board_id = r.json()["id"]
    context['board_id'] = board_id
    
    # Entrega o controle para o teste
    yield 

    # 2. TEARDOWN: Deletar Board
    url_delete = f"{BASE}/boards/{board_id}"
    requests.delete(url_delete, params=AUTH)

# --- PASSOS DO CENÁRIO ---

@given("que existe uma etiqueta criada no quadro para ser atualizada")
def setup_label_to_update(context, board_temporario):
    # Usa o ID do board criado pela fixture
    board_id = context['board_id']
    
    # Cria a label original
    url_label = f"{BASE}/boards/{board_id}/labels"
    payload = {
        "name": "Label Original",
        "color": "blue"
    }
    r = requests.post(url_label, params={**AUTH, **payload})
    
    context['label_id'] = r.json()["id"]

@when('eu envio uma requisição PUT para o endpoint "/labels/{id}" com novos dados')
def update_label(context):
    label_id = context['label_id']
    url = f"{BASE}/labels/{label_id}"
    
    context['new_name'] = "Label Editada BDD"
    context['new_color'] = "red"
    
    # APLICAÇÃO DA CORREÇÃO:
    # A documentação oficial pede "Query parameters" para este endpoint também.
    # Enviamos tudo no 'params' (URL), não no 'data' ou 'json'.
    query_params = {
        **AUTH,
        "name": context['new_name'],
        "color": context['new_color']
    }
    
    context['response'] = requests.put(url, params=query_params)

@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("o corpo da resposta deve conter o nome e cor atualizados")
def verificar_campos_atualizados(context):
    # Verifica a resposta imediata
    response_data = context['response'].json()
    assert response_data['name'] == context['new_name']
    assert response_data['color'] == context['new_color']

    # VERIFICAÇÃO EXTRA (Persistence Check)
    # Adicionamos o delay para garantir que o banco atualizou
    time.sleep(1)
    
    label_id = context['label_id']
    url = f"{BASE}/labels/{label_id}"
    r_check = requests.get(url, params=AUTH)
    
    assert r_check.json()['name'] == context['new_name']
    assert r_check.json()['color'] == context['new_color']