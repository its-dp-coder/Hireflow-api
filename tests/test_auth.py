def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Automation Candidate",
            "email": "automation@example.com",
            "password": "testpassword123",
            "role": "candidate",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "Automation Candidate"
    assert data["email"] == "automation@example.com"
    assert data["role"] == "candidate"
    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_email(client):
    # First registration
    client.post(
        "/auth/register",
        json={
            "full_name": "Duplicate User",
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "role": "candidate",
        },
    )

    # Same email again
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Another User",
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "role": "candidate",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_user(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "full_name": "Login Candidate",
            "email": "login@example.com",
            "password": "testpassword123",
            "role": "candidate",
        },
    )

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "full_name": "Invalid Login User",
            "email": "invalid@example.com",
            "password": "correctpassword",
            "role": "candidate",
        },
    )

    # Wrong password
    response = client.post(
        "/auth/login",
        json={
            "email": "invalid@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_get_current_user(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "full_name": "Current User",
            "email": "current@example.com",
            "password": "testpassword123",
            "role": "candidate",
        },
    )

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "current@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "Current User"
    assert data["email"] == "current@example.com"
    assert data["role"] == "candidate"


def test_current_user_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401

def test_user_cannot_choose_admin_role(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Normal User",
            "email": "normal@example.com",
            "password": "testpassword123",
            "role": "admin",
        },
    )

    assert response.status_code == 201
    assert response.json()["role"] == "candidate"
