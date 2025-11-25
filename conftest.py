import pytest
import requests

# conftest.py
# ... imports ...

# MANTENHA ASSIM PARA ENVIAR AO GITHUB
AUTH = {
    'key': 'SUA_KEY_AQUI',
    'token': 'SEU_TOKEN_AQUI'
}
BOARD_ID = 'SEU_BOARD_ID_AQUI'

# ... resto do código ...

# Fixture que guarda o contexto compartilhado entre os passos
@pytest.fixture
def context():
    return {}

# Fixture de configuração da API (usada no teste 5)
@pytest.fixture
def api_config():
    return {'base_url': BASE_URL, 'auth': AUTH, 'board_id': BOARD_ID}

# Fixture que cria labels (usada nos testes 1, 2, 3 e 4)
@pytest.fixture
def create_label_fixture(api_config):
    def _create(name="Label Setup", color="green"):
        url = f"{api_config['base_url']}/labels"
        params = {
            **api_config['auth'],
            "name": name,
            "color": color,
            "idBoard": api_config['board_id']
        }
        # Cria a label e retorna o JSON
        resp = requests.post(url, params=params)
        return resp.json()
    return _create