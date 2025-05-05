from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

@pytest.fixture
def setup_database():
    # Подготовка тестовой базы данных, если необходимо
    yield
    # Очистка базы данных после тестов

# Тестирование получения всех картин
def test_get_all_paintings(setup_database):
    response = client.get("/paintings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "title" in response.json()[0]
    assert "artist" in response.json()[0]
    assert "price" in response.json()[0]

# Тестирование получения списка картин и их оценок (score)
def test_get_paintings_scores(setup_database):
    response = client.get("/paintings/scores")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "title" in response.json()[0]
    assert "score" in response.json()[0]

# Тестирование авторизации пользователя
def test_user_login(setup_database):
    response = client.post("/login", params={"username": "Henri"})
    assert response.status_code == 200
    assert "token" in response.json()


