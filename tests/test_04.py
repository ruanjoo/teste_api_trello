import pytest
import requests
from pytest_bdd import scenario, given, when, then

@scenario('../features/labels.feature', '4. Update a field on a label (PUT)')
def test_update_field():
    pass

@given('que existe uma label para atualização de campo')
def setup_field(create_label_fixture, context):
    label = create_label_fixture(name="Label Campo Fixo", color="green")
    context['id'] = label['id']
    context['original_name'] = label['name']

@when('eu atualizo apenas a cor para "blue"')
def perform_field_update(api_config, context):
    url = f"{api_config['base_url']}/labels/{context['id']}"
    
    # Envia tudo via params e confia na resposta imediata
    params = {
        **api_config['auth'],
        "color": "blue"
    }
    
    context['response'] = requests.put(url, params=params)

@then('o status code é 200')
def check_status(context):
    assert context['response'].status_code == 200

@then('a cor muda para "blue" mas o nome original é mantido')
def check_partial_update(context):
    data = context['response'].json()
    assert data['color'] == "blue"
    assert data['name'] == context['original_name']