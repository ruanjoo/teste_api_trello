import requests
import pytest
from pytest_bdd import scenario, given, when, then
import shared

@scenario('trello.feature', '05. Deletar background customizado (DELETE)')
def test_delete_background():
    pass

@given("que um background foi criado no cenario anterior")
def check_created_id():
    # Verifica se a lista compartilhada tem dados
    if not shared.background_id_container:
        pytest.skip("Pular teste: Nenhum ID foi criado no teste anterior (Test 04 falhou ou não rodou).")

@when("eu envio uma requisicao para deletar esse background")
def request_delete_background(api_base_url, auth_params, member_id, context):
    # Recupera o último ID adicionado
    bg_id = shared.background_id_container.pop()
    
    url = f"{api_base_url}/members/{member_id}/customBoardBackgrounds/{bg_id}"
    context['response'] = requests.delete(url, params=auth_params)

@then("o status code da resposta deve ser 200")
def check_status_200(context):
    assert context['response'].status_code == 200