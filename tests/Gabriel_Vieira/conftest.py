# conftest.py
import pytest
import os
from dotenv import load_dotenv
from pytest_bdd import given, then, parsers

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# ===========================================================
# FIXTURES DE CONFIGURAÇÃO (O que estava faltando)
# ===========================================================

@pytest.fixture(scope="session")
def api_base_url():
    return "https://api.trello.com/1"

@pytest.fixture(scope="session")
def auth_params():
    """Lê a Key e o Token do .env"""
    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")
    
    if not key or not token:
        pytest.fail("ERRO: As variáveis TRELLO_API_KEY ou TRELLO_API_TOKEN não foram encontradas no .env")
        
    return {
        "key": key,
        "token": token
    }

@pytest.fixture(scope="session")
def member_id():
    return os.getenv("MEMBER_ID", "me")

@pytest.fixture(scope="session")
def image_path():
    """Verifica se a imagem existe na mesma pasta deste arquivo"""
    # Pega o diretório onde o conftest.py está salvo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Monta o caminho: pasta_atual + nome_da_imagem
    default_path = os.path.join(current_dir, "background_test.jpg")
    
    # Se quiser, ainda pode aceitar uma variável de ambiente, mas o default agora é inteligente
    path = os.getenv("TEST_BACKGROUND_IMAGE_PATH", default_path)
    
    if not os.path.exists(path):
        pytest.fail(f"ERRO: Arquivo de imagem não encontrado em: {path}")
    return path

@pytest.fixture
def context():
    """Dicionário para passar dados entre os passos do BDD"""
    return {}

# ===========================================================
# STEPS GENÉRICOS DO BDD (Compartilhados por todos os testes)
# ===========================================================

@given("que possuo credenciais validas")
def credenciais(auth_params):
    # Agora 'auth_params' existe (definido acima) e será injetado aqui
    return auth_params

@then(parsers.parse('o status code da resposta deve ser {status_code:d}'))
def check_status_code(context, status_code):
    assert context['response'].status_code == status_code, f"Status incorreto: {context['response'].status_code}"

@then(parsers.parse('a resposta deve conter o campo "{field}"'))
def check_field(context, field):
    data = context['response'].json()
    assert field in data