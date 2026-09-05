def login_recruiter(client):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


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
        data={
            "username": "candidate@example.com",
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
            "title": "Python Developer",
            "description": "Backend developer",
            "location": "Bangalore",
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
            "description": "Backend developer",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 401


def test_recruiter_can_create_job(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
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
        data={
            "username": "recruiter@example.com",
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
            "title": "Backend Engineer",
            "description": "Develop REST APIs.",
            "location": "Hyderabad",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 201
    assert response.json()["recruiter_id"] == recruiter_user.id


def test_list_jobs(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Python Backend Developer",
            "description": "Build FastAPI services.",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    response = client.get("/jobs")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Backend Developer"


def test_get_job_by_id(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Django Developer",
            "description": "Develop backend applications.",
            "location": "Delhi",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json()["id"] == job_id
    assert response.json()["title"] == "Django Developer"


def test_get_nonexistent_job(client):
    response = client.get("/jobs/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_search_jobs(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Senior Python Engineer",
            "description": "Python FastAPI backend role.",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Frontend Developer",
            "description": "React frontend role.",
            "location": "Mumbai",
            "employment_type": "Full-time",
        },
    )

    response = client.get(
        "/jobs",
        params={
            "search": "Python",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Senior Python Engineer"


def test_filter_jobs_by_location(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Python Developer",
            "description": "Backend development.",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Python Developer",
            "description": "Backend development.",
            "location": "Mumbai",
            "employment_type": "Full-time",
        },
    )

    response = client.get(
        "/jobs",
        params={
            "location": "Bangalore",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["location"] == "Bangalore"


def test_recruiter_can_update_own_job(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Python Developer",
            "description": "Old description",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    response = client.put(
        f"/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Senior Python Developer",
            "description": "Updated description",
            "location": "Remote",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Senior Python Developer"
    assert data["description"] == "Updated description"
    assert data["location"] == "Remote"
    assert data["recruiter_id"] == recruiter_user.id


def test_candidate_cannot_update_job(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    recruiter_token = login_response.json()["access_token"]

    create_response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {recruiter_token}",
        },
        json={
            "title": "Python Developer",
            "description": "Backend development",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    client.post(
        "/auth/register",
        json={
            "full_name": "Candidate User",
            "email": "candidate-update@example.com",
            "password": "testpassword123",
        },
    )

    candidate_login = client.post(
        "/auth/login",
        data={
            "username": "candidate-update@example.com",
            "password": "testpassword123",
        },
    )

    assert candidate_login.status_code == 200

    candidate_token = candidate_login.json()["access_token"]

    response = client.put(
        f"/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "title": "Hacked Job",
            "description": "Should not update",
            "location": "Mumbai",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 403


def test_recruiter_can_delete_own_job(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Temporary Developer",
            "description": "Temporary job",
            "location": "Delhi",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    response = client.delete(
        f"/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/jobs/{job_id}",
    )

    assert get_response.status_code == 404


def test_candidate_cannot_delete_job(client, recruiter_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    recruiter_token = login_response.json()["access_token"]

    create_response = client.post(
        "/jobs",
        headers={
            "Authorization": f"Bearer {recruiter_token}",
        },
        json={
            "title": "Python Developer",
            "description": "Backend development",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    client.post(
        "/auth/register",
        json={
            "full_name": "Delete Candidate",
            "email": "candidate-delete@example.com",
            "password": "testpassword123",
        },
    )

    candidate_login = client.post(
        "/auth/login",
        data={
            "username": "candidate-delete@example.com",
            "password": "testpassword123",
        },
    )

    assert candidate_login.status_code == 200

    candidate_token = candidate_login.json()["access_token"]

    response = client.delete(
        f"/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
    )

    assert response.status_code == 403


def test_list_jobs_pagination(client, recruiter_user):
    token = login_recruiter(client)

    for index in range(3):
        response = client.post(
            "/jobs",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "title": f"Backend Developer {index}",
                "description": "Build APIs.",
                "location": "Bangalore",
                "employment_type": "Full-time",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/jobs?skip=0&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2


def test_list_jobs_limit_cannot_exceed_100(client):
    response = client.get(
        "/jobs?limit=101"
    )

    assert response.status_code == 422


def test_list_jobs_skip_cannot_be_negative(client):
    response = client.get(
        "/jobs?skip=-1"
    )

    assert response.status_code == 422