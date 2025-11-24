import requests
from pytest_bdd import scenario, when, then
import uuid

@scenario('trello.feature', '02. Atualizar um membro (PUT)')
def test_update_member():
    pass

@when("eu atualizo a Bio do membro para um valor aleatorio")
def request_update_bio(api_base_url, auth_params, member_id, context):
    url = f"{api_base_url}/members/{member_id}"
    unique_bio = f"Test BDD {uuid.uuid4().hex[:8]}"
    
    update_payload = {"bio": unique_bio}
    params_with_payload = auth_params.copy()
    params_with_payload.update(update_payload)
    
    context['response'] = requests.put(url, params=params_with_payload)

@then("o status code da resposta deve ser 200 ou 401")
def check_status_200_or_401(context):
    code = context['response'].status_code
    assert code in [200, 401]