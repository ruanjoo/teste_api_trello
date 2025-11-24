import requests
from pytest_bdd import scenario, when, parsers

@scenario('trello.feature', '01. Buscar um membro (GET)')
def test_get_member():
    pass

@when(parsers.parse('eu busco os dados do membro "{member_id}"'))
def request_get_member(api_base_url, auth_params, member_id, context):
    url = f"{api_base_url}/members/{member_id}"
    context['response'] = requests.get(url, params=auth_params)