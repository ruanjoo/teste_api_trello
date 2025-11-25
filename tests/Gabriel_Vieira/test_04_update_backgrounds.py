import requests
import os
from pytest_bdd import scenario, given, when, then
import shared # Certifique-se que shared.py está na mesma pasta

@scenario('trello.feature', '04. Upload de novo background (POST)')
def test_upload_background():
    pass

# A fixture 'image_path' já vem do conftest.py, então removemos a lógica duplicada
@given("eu tenho um arquivo de imagem valido")
def check_image_exists(image_path):
    assert os.path.exists(image_path), f"Imagem não encontrada: {image_path}"

@when("eu faco o upload da imagem para backgrounds")
def request_upload_background(api_base_url, auth_params, member_id, image_path, context):
    url = f"{api_base_url}/members/{member_id}/customBoardBackgrounds"
    
    # Abrindo o arquivo binário
    with open(image_path, 'rb') as f:
        # Nota: 'files' é separado de 'params' no requests
        response = requests.post(url, params=auth_params, files={'file': f})
    
    context['response'] = response
    
    # Lógica de compartilhamento de ID
    if response.status_code in [200, 201]:
        data = response.json()
        if "id" in data:
            print(f"DEBUG: ID gerado: {data['id']}") # Útil para debug
            shared.background_id_container.append(data["id"])

@then("o status code da resposta deve ser 200 ou 201")
def check_status_upload(context):
    assert context['response'].status_code in [200, 201]

@then("a resposta deve conter um ID de background")
def check_id_exists(context):
    data = context['response'].json()
    assert "id" in data