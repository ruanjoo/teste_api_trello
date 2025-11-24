import requests
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv
from pytest_bdd import scenario, given, when, then

# --- CONFIGURAÇÃO ---
arquivo_env = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(arquivo_env)

BASE = os.getenv("TRELLO_BASE_URL")
STABLE_CARD_ID = os.getenv("STABLE_CARD_ID")
AUTH = {
    "key": os.getenv("TRELLO_KEY"), 
    "token": os.getenv("TRELLO_TOKEN")
}

if not BASE or not STABLE_CARD_ID:
    raise ValueError("ERRO: Variáveis de ambiente não carregadas.")

# Liga o teste ao arquivo .feature
@scenario('update_an_action.feature', 'Atualizar o texto de um comentário existente com sucesso')
def test_update_action():
    pass

# --- FIXTURE CONTEXTO ---
@pytest.fixture
def context():
    return {}

# --- DADO (GIVEN) ---
@given('que existe um comentário com o texto "Texto Original"')
def setup_comentario_original(context):
    """Cria o comentário inicial que será editado"""
    url = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    
    # Cria com um texto fixo
    r = requests.post(url, params={**AUTH, "text": "Texto Original"})
    r.raise_for_status()
    
    context['action_id'] = r.json()["id"]

# --- QUANDO (WHEN) ---
@when('eu envio uma requisição PUT para alterar o texto para "Texto Editado via BDD"')
def atualizar_comentario(context):
    action_id = context['action_id']
    novo_texto = "Texto Editado via BDD"
    
    # Endpoint: /actions/{id}
    url = f"{BASE}/actions/{action_id}"
    
    parametros_atualizacao = {
        **AUTH,
        "text": novo_texto
    }
    
    context['response'] = requests.put(url, params=parametros_atualizacao)
    
    # Guardamos o texto esperado para a validação no passo seguinte
    context['expected_text'] = novo_texto

# --- ENTÃO (THEN) ---
@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("a resposta deve mostrar o novo texto atualizado")
def verificar_atualizacao_texto(context):
    dados = context['response'].json()

    texto_retornado = dados['data']['text']
    
    assert texto_retornado == context['expected_text']