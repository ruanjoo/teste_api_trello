import pytest
import requests
from pytest_bdd import scenario, given, when, then

# Liga este arquivo especificamente ao Cenário 1 do arquivo feature
@scenario('../features/labels.feature', '1. Get a Label (GET)')
def test_get_label():
    pass

@given('que existe uma label para leitura')
def setup_get(create_label_fixture, context):
    # Cria uma label temporária antes do teste
    label = create_label_fixture(name="Label Test Get")
    context['id'] = label['id']
    context['name'] = label['name']

@when('eu busco essa label pelo ID')
def perform_get(api_config, context):
    url = f"{api_config['base_url']}/labels/{context['id']}"
    # Realiza o GET
    context['response'] = requests.get(url, params=api_config['auth'])

@then('o status code é 200')
def check_status(context):
    assert context['response'].status_code == 200

@then('os dados da label retornam corretamente')
def check_data(context):
    data = context['response'].json()
    assert data['id'] == context['id']
    assert data['name'] == context['name']