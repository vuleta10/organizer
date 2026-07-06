def test_register_user(client):

    response = client.post(
        "/users/register",
        json={
            "username": "pera",
            "password": "123"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["username"] == "pera"
    
def test_login_user(client):

    client.post(
    "/users/register",
    json={
        "username": "testuser",
        "password": "123"
    }
    )

    response = client.post(
    "/users/login",
    json={
        "username": "testuser",
        "password": "123"
    }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "testuser"  
def test_login_wrong_password(client):

    client.post(
        "/users/register",
        json={
            "username": "marko",
            "password": "123"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "username": "marko",
            "password": "999"
        }
    )

    assert response.status_code == 401

def test_change_password(client):

    client.post(
        "/users/register",
        json={
            "username": "pera",
            "password": "123"
        }
    )

    response = client.put(
        "/users/change-password",
        json={
            "username": "pera",
            "old_password": "123",
            "new_password": "456"
        }
    )

    assert response.status_code == 200