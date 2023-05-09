from werkzeug.exceptions import HTTPException
import pytest
from app.routes.planet import validate_model

# test get books with empty database
def test_get_all_crystals_with_no_records(client):
    # Act
    response = client.get('/crystals')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_read_cyrstal_by_id(client, two_saved_crystals):
    # Act 
    response = client.get('/crystals/2')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "color": "Red",
        "powers": "Awesomeness",
        "name": "Garnet"
    }

def test_post_crystal(client):
    # Act
    response = client.post("/crystals", json={
        'name': "Amethyst",
        'color': 'Purple',
        'powers': 'Knowledge',
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Crystal Amethyst successfully created."