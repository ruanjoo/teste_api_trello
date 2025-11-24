import requests
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv
from pytest_bdd import scenario, given, when, then, parsers

# --- CONFIGURAÇÃO DE AMBIENTE ---
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

# --- CENÁRIO ---
@scenario('delete_action_reaction.feature', 'Deletar uma reação existente com sucesso')
def test_delete_reaction_scenario():
    pass

# --- FIXTURE DE CONTEXTO ---
@pytest.fixture
def context():
    return {}

# --- DADO (GIVEN) ---
@given("que existe um comentário criado no cartão alvo")
def setup_comentario(context):
    """Cria um comentário (Action) para receber a reação"""
    url = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    # Criamos um comentário simples
    r = requests.post(url, params={**AUTH, "text": "Comentário para teste de Reação"})
    r.raise_for_status()
    context['action_id'] = r.json()["id"]

@given("que eu adicionei uma reação a este comentário")
def setup_reacao(context):
    """Adiciona uma reação (emoji) ao comentário criado anteriormente"""
    action_id = context['action_id']
    url = f"{BASE}/actions/{action_id}/reactions"
    
    # Payload para adicionar um 'Thumbs Up' (👍). O código unificado é 1F44D.
    payload = {
        "unified": "1F44D"
    }
    
    # Nota: POST reactions geralmente requer body JSON
    r = requests.post(url, json=payload, params=AUTH)
    r.raise_for_status()
    
    # Guardamos o ID da reação para deletar depois
    context['reaction_id'] = r.json()["id"]

# --- QUANDO (WHEN) ---
@when("eu envio uma requisição DELETE para remover essa reação")
def requisitar_delecao_reacao(context):
    """Executa o DELETE no endpoint alvo"""
    action_id = context['action_id']
    reaction_id = context['reaction_id']
    
    # Montagem da URL conforme documentação: /actions/{idAction}/reactions/{id}
    url = f"{BASE}/actions/{action_id}/reactions/{reaction_id}"
    
    context['response'] = requests.delete(url, params=AUTH)

# --- ENTÃO (THEN) ---
@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

