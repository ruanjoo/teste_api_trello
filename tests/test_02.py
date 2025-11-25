import pytest
import requests
from pytest_bdd import scenario, given, when, then

@scenario('../features/labels.feature', '2. Update a label (PUT)')
def test_update_label():
    pass

@given('que existe uma label para atualização completa')
def setup_update(create_label_fixture, context):
    label = create_label_fixture(name="Label Original")
    context['id'] = label['id']

@when('eu atualizo a label com nome "Update Full" e cor "red"')
def perform_update(api_config, context):
    url = f"{api_config['base_url']}/labels/{context['id']}"
    
    # SOLUÇÃO DEFINITIVA:
    # 1. Usar params para tudo (igual ao Create que funcionou)
    # 2. Não fazer um GET depois (confiar na resposta do PUT)
    params = {
        **api_config['auth'],
        "name": "Update Full",
        "color": "red"
    }
    
    context['response'] = requests.put(url, params=params)

@then('o status code é 200')
def check_status(context):
    assert context['response'].status_code == 200

@then('o nome e a cor da label são atualizados')
def check_updated_data(context):
    # Validamos diretamente o JSON retornado pelo PUT
    data = context['response'].json()
    assert data['name'] == "Update Full"
    assert data['color'] == "red"