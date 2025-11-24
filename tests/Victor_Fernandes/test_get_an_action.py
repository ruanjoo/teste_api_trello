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
@scenario('get_an_action.feature', 'Consultar um comentário existente pelo ID')
def test_get_action():
    pass

# --- FIXTURE CONTEXTO ---
@pytest.fixture
def context():
    return {}

# --- DADO (GIVEN) ---
@given("que acabei de criar um comentário no cartão")
def setup_comentario_para_busca(context):
    """Cria um comentário para termos um ID válido para buscar"""
    url = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    texto_original = "Teste de GET Action ID"
    
    r = requests.post(url, params={**AUTH, "text": texto_original})
    r.raise_for_status()
    
    # Guardamos o ID e o Texto para validar depois
    dados = r.json()
    context['action_id'] = dados["id"]
    context['original_text'] = texto_original

# --- QUANDO (WHEN) ---
@when("eu envio uma requisição GET para buscar essa ação pelo ID")
def get_action_by_id(context):
    action_id = context['action_id']
    
    # Endpoint: /actions/{id}
    url = f"{BASE}/actions/{action_id}"
    
    context['response'] = requests.get(url, params=AUTH)

# --- ENTÃO (THEN) ---
@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("o texto da ação retornada deve ser igual ao texto criado")
def verificar_conteudo_acao(context):
    dados_retornados = context['response'].json()
    

    assert dados_retornados['id'] == context['action_id']
    
    texto_retornado = dados_retornados['data']['text']
    
    assert texto_retornado == context['original_text']