import requests
from pytest_bdd import scenario, when, then

@scenario('trello.feature', '03. Buscar backgrounds customizados (GET)')
def test_get_backgrounds():
    pass

@when("eu busco a lista de custom board backgrounds")
def request_get_backgrounds(api_base_url, auth_params, member_id, context):
    url = f"{api_base_url}/members/{member_id}/customBoardBackgrounds"
    context['response'] = requests.get(url, params=auth_params)

@then("a resposta deve ser uma lista")
def check_response_is_list(context):
    data = context['response'].json()
    assert isinstance(data, list)