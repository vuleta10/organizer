def test_register_user(client):

    response = client.post(
        "/users/register",
        json={
            "username": "utest1",
            "password": "test123"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["username"] == "utest1"

def test_login_user(client):

    response = client.post(
        "/users/login",
        json={
            "username": "utest2",
            "password": "test123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "utest2"

def test_login_wrong_password(client):

    response = client.post(
        "/users/login",
        json={
            "username": "utest3",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401

def test_change_password(client):

    response = client.put(
        "/users/change-password",
        json={
            "username": "utest4",
            "old_password": "test123",
            "new_password": "test456"
        }
    )

    assert response.status_code == 200
