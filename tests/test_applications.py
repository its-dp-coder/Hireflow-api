def create_job(client, recruiter_user):
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
            "title": "Python Backend Developer",
            "description": "Build scalable backend APIs.",
            "location": "Bangalore",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_candidate(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test Candidate",
            "email": "application-candidate@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": "application-candidate@example.com",
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_candidate_can_apply_to_job(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "I am interested in this position.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["job_id"] == job_id
    assert data["status"] == "applied"
    assert data["cover_letter"] == (
        "I am interested in this position."
    )


def test_recruiter_cannot_apply_to_job(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

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
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "cover_letter": "Recruiter application",
        },
    )

    assert response.status_code == 403


def test_candidate_cannot_apply_to_nonexistent_job(client):
    candidate_token = create_candidate(client)

    response = client.post(
        "/applications/jobs/99999",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "Application",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_candidate_cannot_apply_twice(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    first_response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "First application",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "Second application",
        },
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "You have already applied to this job"
    )


def test_candidate_can_view_own_applications(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    apply_response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "Interested in the role.",
        },
    )

    assert apply_response.status_code == 201

    response = client.get(
        "/applications/my",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["job_id"] == job_id
    assert data[0]["status"] == "applied"


def test_recruiter_can_view_applications_for_own_job(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "Please consider my application.",
        },
    )

    assert response.status_code == 201

    recruiter_login = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert recruiter_login.status_code == 200

    recruiter_token = recruiter_login.json()["access_token"]

    response = client.get(
        f"/applications/job/{job_id}",
        headers={
            "Authorization": f"Bearer {recruiter_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["job_id"] == job_id
    assert data[0]["status"] == "applied"


def test_candidate_cannot_view_job_applications(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    response = client.get(
        f"/applications/job/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
    )

    assert response.status_code == 403


def test_recruiter_can_update_application_status(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    apply_response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "I would like to join your team.",
        },
    )

    assert apply_response.status_code == 201

    application_id = apply_response.json()["id"]

    recruiter_login = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert recruiter_login.status_code == 200

    recruiter_token = recruiter_login.json()["access_token"]

    response = client.put(
        f"/applications/{application_id}/status",
        headers={
            "Authorization": f"Bearer {recruiter_token}",
        },
        json={
            "status": "shortlisted",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["status"] == "shortlisted"


def test_invalid_application_status_is_rejected(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    apply_response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "Test application",
        },
    )

    assert apply_response.status_code == 201

    application_id = apply_response.json()["id"]

    recruiter_login = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert recruiter_login.status_code == 200

    recruiter_token = recruiter_login.json()["access_token"]

    response = client.put(
        f"/applications/{application_id}/status",
        headers={
            "Authorization": f"Bearer {recruiter_token}",
        },
        json={
            "status": "random-status",
        },
    )

    assert response.status_code == 422


def test_my_applications_pagination(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "Test application",
        },
    )

    assert response.status_code == 201

    response = client.get(
        "/applications/my?skip=0&limit=1",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_my_applications_limit_cannot_exceed_100(
    client,
):
    candidate_token = create_candidate(client)

    response = client.get(
        "/applications/my?limit=101",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
    )

    assert response.status_code == 422


def test_job_applications_pagination(
    client,
    recruiter_user,
):
    job_id = create_job(
        client,
        recruiter_user,
    )

    candidate_token = create_candidate(client)

    response = client.post(
        f"/applications/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {candidate_token}",
        },
        json={
            "cover_letter": "Test application",
        },
    )

    assert response.status_code == 201

    recruiter_login = client.post(
        "/auth/login",
        data={
            "username": "recruiter@example.com",
            "password": "testpassword123",
        },
    )

    assert recruiter_login.status_code == 200

    recruiter_token = recruiter_login.json()["access_token"]

    response = client.get(
        f"/applications/job/{job_id}?skip=0&limit=1",
        headers={
            "Authorization": f"Bearer {recruiter_token}",
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1