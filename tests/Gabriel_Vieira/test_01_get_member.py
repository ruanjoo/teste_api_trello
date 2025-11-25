import requests
from pytest_bdd import scenario, when, parsers

@scenario('trello.feature', '01. Buscar um membro (GET)')
def test_get_member():
    pass

# Note que removemos toda a configuração de .env aqui. 
# O pytest injeta 'api_base_url' e 'auth_params' automaticamente do conftest.py

@when(parsers.parse('eu busco os dados do membro "{member_id}"'))
def request_get_member(api_base_url, auth_params, member_id, context):
    # Se member_id for "me", a URL funciona, se for um ID específico também
    url = f"{api_base_url}/members/{member_id}"
    context['response'] = requests.get(url, params=auth_params)