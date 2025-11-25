# TrelloTests/tests/Marcos/conftest.py

import pytest
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env do projeto raiz
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)

BASE = os.getenv("TRELLO_BASE_URL")
AUTH = {
    "key": os.getenv("TRELLO_KEY"),
    "token": os.getenv("TRELLO_TOKEN")
}


@pytest.fixture
def context():
    return {}


@pytest.fixture
def temp_board():
    # Criar board
    url = f"{BASE}/boards/"
    payload = {"name": "Board Temp Tests"}

    resp = requests.post(url, params=AUTH, json=payload)
    if resp.status_code != 200:
        raise Exception(f"Erro ao criar board: {resp.text}")

    board_id = resp.json()["id"]

    yield board_id  # entrega o ID ao teste

    # Deletar board no final
    requests.delete(f"{BASE}/boards/{board_id}", params=AUTH)


@pytest.fixture
def create_label(temp_board):
    def creator(name="Label Test Auto", color="green"):
        url = f"{BASE}/labels"
        payload = {
            "name": name,
            "color": color,
            "idBoard": temp_board
        }

        resp = requests.post(url, params=AUTH, json=payload)
        if resp.status_code != 200:
            raise Exception(
                f"Erro ao criar label:\nPayload={payload}\nResp={resp.text}"
            )

        return resp.json()

    return creator
