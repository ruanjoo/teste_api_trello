import requests
from pytest_bdd import scenario, given, when, then
import os
import shared # Importando a lista compartilhada

@scenario('trello.feature', '04. Upload de novo background (POST)')
def test_upload_background():
    pass

@given("eu tenho um arquivo de imagem valido")
def image_file(image_path):
    assert os.path.exists(image_path)

@when("eu faco o upload da imagem para backgrounds")
def request_upload_background(api_base_url, auth_params, member_id, image_path, context):
    url = f"{api_base_url}/members/{member_id}/customBoardBackgrounds"
    
    with open(image_path, 'rb') as f:
        response = requests.post(url, params=auth_params, files={'file': f})
    
    context['response'] = response
    
    if response.status_code in [200, 201]:
        data = response.json()
        if "id" in data:
            # Usando o arquivo shared para guardar o ID
            shared.background_id_container.append(data["id"])

@then("o status code da resposta deve ser 200 ou 201")
def check_status_upload(context):
    assert context['response'].status_code in [200, 201]

@then("a resposta deve conter um ID de background")
def check_id_exists(context):
    data = context['response'].json()
    assert "id" in data