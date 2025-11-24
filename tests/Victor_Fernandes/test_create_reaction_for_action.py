import requests
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv
from pytest_bdd import scenario, given, when, then

# --- CONFIGURAÇÃO (Mantendo seu padrão) ---
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
@scenario('create_reaction_for_action.feature', 'Adicionar uma reação (Joinha) a um comentário com sucesso')
def test_create_reaction():
    pass

# --- FIXTURE CONTEXTO ---
@pytest.fixture
def context():
    return {}

# --- DADO (GIVEN) ---
@given("que existe um comentário criado no cartão")
def setup_comentario(context):
    """Cria um comentário novo para garantir que temos onde reagir"""
    url = f"{BASE}/cards/{STABLE_CARD_ID}/actions/comments"
    r = requests.post(url, params={**AUTH, "text": "Comentário para teste de CREATE Reaction"})
    r.raise_for_status()
    context['action_id'] = r.json()["id"]

# --- QUANDO (WHEN) ---
@when('eu envio uma requisição POST para adicionar a reação "1F44D" neste comentário')
def criar_reacao(context):
    action_id = context['action_id']
    url = f"{BASE}/actions/{action_id}/reactions"
    
    # O Trello exige o payload com o código 'unified' do emoji.
    # 1F44D é o código hexadecimal para o emoji de "Polegar para cima" (👍)
    payload = {
        "unified": "1F44D"
    }
    
    # Importante: passamos 'json=payload' para o requests formatar corretamente
    context['response'] = requests.post(url, json=payload, params=AUTH)

# --- ENTÃO (THEN) ---
@then("o código de status da resposta deve ser 200")
def verificar_status_200(context):
    assert context['response'].status_code == 200

@then('a resposta deve conter o código do emoji "1F44D" e o ID correto')
def verificar_dados_reacao(context):
    dados = context['response'].json()
    
    # Valida se o emoji criado é realmente o que pedimos
    assert dados['emoji']['unified'] == "1F44D"
    
    # Valida se a API retornou um ID para essa nova reação
    assert "id" in dados
    
    # Opcional: Salva o ID da reação caso queira usar num passo de limpeza (teardown) futuro
    context['reaction_id'] = dados['id']