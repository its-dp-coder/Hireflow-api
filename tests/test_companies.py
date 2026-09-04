def test_recruiter_can_create_company(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "TechFlow Solutions",
            "description": "Software development company",
            "website": "https://techflow.example.com",
            "location": "Bangalore",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "TechFlow Solutions"
    assert data["location"] == "Bangalore"
    assert data["recruiter_id"] == recruiter_user.id


def test_candidate_cannot_create_company(client):
    client.post(
        "/auth/register",
        json={
            "full_name": "Company Candidate",
            "email": "company-candidate@example.com",
            "password": "testpassword123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "company-candidate@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Candidate Company",
            "description": "Should not be created",
            "website": None,
            "location": "Delhi",
        },
    )

    assert response.status_code == 403


def test_list_companies(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Alpha Technologies",
            "description": "Technology company",
            "website": "https://alpha.example.com",
            "location": "Bangalore",
        },
    )

    response = client.get("/companies")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Alpha Technologies"


def test_get_company_by_id(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Beta Technologies",
            "description": "Backend technology company",
            "website": None,
            "location": "Mumbai",
        },
    )

    company_id = create_response.json()["id"]

    response = client.get(
        f"/companies/{company_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == company_id
    assert data["name"] == "Beta Technologies"


def test_get_nonexistent_company(client):
    response = client.get("/companies/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"


def test_duplicate_company_not_allowed(
    client,
    recruiter_user,
):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    company_data = {
        "name": "Unique Technologies",
        "description": "Technology company",
        "website": None,
        "location": "Bangalore",
    }

    first_response = client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=company_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=company_data,
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Company already exists"


def test_recruiter_can_update_own_company(
    client,
    recruiter_user,
):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Old Company Name",
            "description": "Old description",
            "website": None,
            "location": "Delhi",
        },
    )

    company_id = create_response.json()["id"]

    response = client.put(
        f"/companies/{company_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Updated Company Name",
            "description": "Updated description",
            "website": "https://updated.example.com",
            "location": "Bangalore",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Company Name"
    assert data["description"] == "Updated description"
    assert data["location"] == "Bangalore"


def test_recruiter_can_delete_own_company(
    client,
    recruiter_user,
):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/companies",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Delete Company",
            "description": "Company to delete",
            "website": None,
            "location": "Delhi",
        },
    )

    company_id = create_response.json()["id"]

    response = client.delete(
        f"/companies/{company_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/companies/{company_id}",
    )

    assert get_response.status_code == 404