def test_candidate_cannot_create_job(client):
    client.post(
        "/auth/register",
        json={
            "full_name": "Test Candidate",
            "email": "candidate@example.com",
            "password": "testpassword123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "candidate@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Python Developer",
            "description": "Backend Python developer",
            "location": "Remote",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to perform this action"
    )


def test_user_without_token_cannot_create_job(client):
    response = client.post(
        "/jobs",
        json={
            "title": "Python Developer",
            "description": "Backend Python developer",
            "location": "Remote",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 401


def test_recruiter_can_create_job(
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

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Senior Python Developer",
            "description": "Build scalable backend services.",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Senior Python Developer"
    assert data["location"] == "Bangalore"
    assert data["employment_type"] == "Full-time"
    assert data["recruiter_id"] == recruiter_user.id


def test_job_belongs_to_authenticated_recruiter(
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

    response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Backend Engineer",
            "description": "Develop REST APIs.",
            "location": "Hyderabad",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 201
    assert response.json()["recruiter_id"] == recruiter_user.id