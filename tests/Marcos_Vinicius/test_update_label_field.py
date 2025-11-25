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
@scenario('update_label_field.feature', 'Atualizar o campo nome de uma etiqueta com sucesso')
def test_update_label_field():
    pass

@pytest.fixture
def context():
    return {}

# --- FIXTURE INTELIGENTE (SETUP & TEARDOWN) ---
@pytest.fixture
def board_temporario(context):
    """
    Esta fixture roda AUTOMATICAMENTE antes e depois do teste.
    1. Cria um Board novo.
    2. Passa o controle para o teste (yield).
    3. Deleta o Board no final.
    """
    # 1. SETUP: Criar Board
    url_create = f"{BASE}/boards/"
    payload = {
        "name": "Board Temporario BDD",
        "defaultLabels": "false",
        "defaultLists": "false"
    }
    r = requests.post(url_create, params={**AUTH, **payload})
    
    # Valida se criou para não rodar o teste em falso
    assert r.status_code == 200
    board_id = r.json()["id"]
    context['board_id'] = board_id
    
    print(f"\n[SETUP] Board criado com ID: {board_id}")

    # Pausa o código aqui e deixa o teste rodar...
    yield 

    # 3. TEARDOWN: Deletar Board (Roda mesmo se o teste falhar)
    url_delete = f"{BASE}/boards/{board_id}"
    requests.delete(url_delete, params=AUTH)
    print(f"[TEARDOWN] Board {board_id} deletado com sucesso.")


# --- PASSOS DO BDD ---

@given("que existe uma etiqueta criada no quadro para teste de campo")
def setup_label_field_test(context, board_temporario):
    # Note que passamos 'board_temporario' como argumento para garantir que ele rodou
    board_id = context['board_id']
    
    # Cria Label no Board temporário
    url_label = f"{BASE}/boards/{board_id}/labels"
    payload = {
        "name": "Nome Antigo",
        "color": "pink"
    }
    r = requests.post(url_label, params={**AUTH, **payload})
    
    assert r.status_code == 200
    context['label_id'] = r.json()["id"]
    print(f"[STEP] Label criada: {context['label_id']}")

@when('eu envio uma requisição PUT para o endpoint "/labels/{id}/name" com o novo valor')
def update_label_field_name(context):
    label_id = context['label_id']
    url = f"{BASE}/labels/{label_id}/name"
    
    context['new_value'] = "Nome Atualizado via Field"
    
    # Para o endpoint /{field}, usamos params conforme funcionou anteriormente
    query_params = {
        **AUTH,
        "value": context['new_value']
    }
    
    context['response'] = requests.put(url, params=query_params)

@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("o nome da etiqueta deve ter sido alterado corretamente")
def verificar_alteracao_campo(context):
    # Delay essencial para evitar erro de latência da API
    time.sleep(1)

    label_id = context['label_id']
    url = f"{BASE}/labels/{label_id}"
    
    r_check = requests.get(url, params=AUTH)
    
    # Valida a mudança
    assert r_check.json()['name'] == context['new_value']