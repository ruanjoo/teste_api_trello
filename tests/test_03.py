import pytest
import requests
from pytest_bdd import scenario, given, when, then

@scenario('../features/labels.feature', '3. Delete a Label (DEL)')
def test_delete_label():
    pass

@given('que existe uma label para deleção')
def setup_delete(create_label_fixture, context):
    label = create_label_fixture(name="Label Delete")
    context['id'] = label['id']

@when('eu envio o comando de delete')
def perform_delete(api_config, context):
    url = f"{api_config['base_url']}/labels/{context['id']}"
    context['response'] = requests.delete(url, params=api_config['auth'])

@then('o status code é 200')
def check_status(context):
    assert context['response'].status_code == 200

@then('a label não é mais encontrada (404)')
def check_not_found(api_config, context):
    url = f"{api_config['base_url']}/labels/{context['id']}"
    resp = requests.get(url, params=api_config['auth'])
    assert resp.status_code == 404