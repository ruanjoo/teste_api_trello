import pytest
import requests
from pytest_bdd import scenario, given, when, then

@scenario('../features/labels.feature', '5. Create a Label (POST)')
def test_create_label():
    pass

@given('que tenho dados válidos para nova label')
def prepare_payload(api_config, context):
    # Prepara o payload
    context['payload'] = {
        **api_config['auth'],
        "name": "Label Criada POST",
        "color": "yellow",
        "idBoard": api_config['board_id']
    }

@when('eu envio o comando de create')
def perform_create(api_config, context):
    url = f"{api_config['base_url']}/labels"
    context['response'] = requests.post(url, params=context['payload'])

@then('o status code é 200')
def check_status(context):
    assert context['response'].status_code == 200

@then('a API retorna o ID da nova label')
def check_id_returned(context):
    data = context['response'].json()
    assert 'id' in data
    assert data['name'] == "Label Criada POST"