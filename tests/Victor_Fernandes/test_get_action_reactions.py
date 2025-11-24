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
@scenario('get_action_reactions.feature', 'Consultar detalhes de uma reação existente pelo ID')
def test_get_reaction():
    pass

# --- FIXTURE CONTEXTO ---
@pytest.fixture
def context():
    return {}

# --- DADO (GIVEN) ---
@given("que existe um comentário com uma reação criada")
def setup_comentario_com_reacao(context):
    # 1. Cria o comentário
    url_comment = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    r_comment = requests.post(url_comment, params={**AUTH, "text": "Setup para Teste de GET Reaction"})
    r_comment.raise_for_status()
    action_id = r_comment.json()["id"]
    context['action_id'] = action_id

    # 2. Cria a reação nesse comentário
    # Vamos usar o Foguete (🚀) código "1F680" para variar
    url_react = f"{BASE}/actions/{action_id}/reactions"
    payload = {"unified": "1F680"}
    
    r_react = requests.post(url_react, json=payload, params=AUTH)
    r_react.raise_for_status()
    
    # Guardamos o ID e o emoji esperado para validação posterior
    dados_reacao = r_react.json()
    context['reaction_id'] = dados_reacao["id"]
    context['expected_emoji'] = "1F680"

# --- QUANDO (WHEN) ---
@when("eu envio uma requisição GET para buscar essa reação pelo ID")
def consultar_reacao(context):
    action_id = context['action_id']
    reaction_id = context['reaction_id']
    
    # Endpoint específico: /actions/{idAction}/reactions/{id}
    url = f"{BASE}/actions/{action_id}/reactions/{reaction_id}"
    
    context['response'] = requests.get(url, params=AUTH)

# --- ENTÃO (THEN) ---
@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then("os dados da reação retornada devem corresponder à reação criada")
def verificar_conteudo_reacao(context):
    dados = context['response'].json()
    
    # Verifica se o ID retornado é o mesmo que pedimos
    assert dados['id'] == context['reaction_id']
    
    # Verifica se o emoji é o foguete (1F680)
    assert dados['emoji']['unified'] == context['expected_emoji']
    
    assert 'idMember' in dados