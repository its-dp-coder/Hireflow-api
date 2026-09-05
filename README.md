# HireFlow API

A production-style Job Recruitment REST API built with FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication, Alembic, Docker, GitHub Actions, and Render.

HireFlow is a backend system for managing candidates, recruiters, companies, jobs, and job applications with authentication, role-based access control, resource ownership authorization, pagination, database constraints, automated testing, CI, and cloud deployment.

## 🚀 Live Demo

### Production API

https://hireflow-api-nso3.onrender.com

### Health Check

https://hireflow-api-nso3.onrender.com/health

### Swagger API Documentation

https://hireflow-api-nso3.onrender.com/docs

---

## ✨ Features

- User registration and authentication
- JWT-based authentication
- Secure password hashing with bcrypt
- Candidate and recruiter roles
- Role-Based Access Control (RBAC)
- Resource ownership authorization
- Company management
- Job management
- Job search
- Location-based job filtering
- Pagination
- Job applications
- Duplicate application prevention
- Application status workflow
- Recruiter application management
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Automated API testing with pytest
- Dedicated PostgreSQL test database
- Docker containerization
- GitHub Actions CI
- Production deployment on Render
- Environment-based configuration
- Health check endpoint
- Swagger/OpenAPI documentation

---

## 🛠️ Tech Stack

| Technology       | Purpose                |
| ---------------- | ---------------------- |
| Python 3.13      | Programming Language   |
| FastAPI          | REST API Framework     |
| PostgreSQL       | Relational Database    |
| SQLAlchemy       | ORM                    |
| Alembic          | Database Migrations    |
| Pydantic         | Data Validation        |
| PyJWT            | JWT Authentication     |
| Passlib + bcrypt | Password Hashing       |
| pytest           | Automated Testing      |
| Docker           | Containerization       |
| GitHub Actions   | Continuous Integration |
| Render           | Cloud Deployment       |

---

## 🏗️ Architecture

```text
                    Client
                      |
                      v
              ┌───────────────┐
              │    FastAPI    │
              │   Application │
              └───────┬───────┘
                      |
          ┌───────────┼───────────┐
          |           |           |
          v           v           v
       Auth         Jobs      Companies
          |           |           |
          |           v           |
          |     Applications      |
          |           |           |
          └───────────┼───────────┘
                      |
                      v
              Authentication &
              Authorization
                      |
                      v
                SQLAlchemy ORM
                      |
                      v
                 PostgreSQL
```

---

## 📁 Project Structure

```text
Hireflow-api/
│
├── app/
│   ├── api/
│   │   ├── applications.py
│   │   ├── auth.py
│   │   ├── companies.py
│   │   └── jobs.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── security.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── application.py
│   │   ├── company.py
│   │   ├── job.py
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── application.py
│   │   ├── company.py
│   │   ├── job.py
│   │   └── user.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── conftest.py
│   ├── test_applications.py
│   ├── test_auth.py
│   ├── test_companies.py
│   ├── test_jobs.py
│   └── test_main.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🔐 Authentication

HireFlow uses JWT Bearer Authentication.

Authentication flow:

```text
User Registration
       |
       v
Password Hashing
       |
       v
User Stored in PostgreSQL
       |
       v
Login
       |
       v
Credentials Verified
       |
       v
JWT Access Token Generated
       |
       v
Client sends Bearer Token
       |
       v
JWT Validation
       |
       v
Current User Identified
       |
       v
Role + Ownership Authorization
```

Passwords are never stored in plain text.

---

# 👥 User Roles

HireFlow supports two primary roles.

## Candidate

Candidates can:

- Register
- Login
- View their profile
- Browse jobs
- Search jobs
- Filter jobs by location
- Apply to jobs
- View their own applications

## Recruiter

Recruiters can:

- Login
- Create companies
- Update their own companies
- Delete their own companies
- Create jobs
- Update their own jobs
- Delete their own jobs
- View applications for their own jobs
- Update application status

---

# 🛡️ Role-Based Access Control

Protected endpoints use FastAPI dependencies to enforce user roles.

Example:

```python
current_user: User = Depends(require_role("recruiter"))
```

This ensures recruiter-only endpoints cannot be accessed by candidates.

HireFlow also performs resource ownership checks.

For example:

```text
Recruiter A
    |
    +---- Job A
    |
    +---- Applications for Job A

Recruiter B
    |
    +---- Job B
    |
    +---- Applications for Job B
```

Recruiter A cannot modify Recruiter B's jobs, companies, or applications.

The authorization model is:

```text
Role Authorization
        +
Resource Ownership
        |
        v
Secure API Access
```

---

# 💼 Job Management

Recruiters can create and manage jobs.

Each job contains:

- Title
- Description
- Location
- Employment type
- Recruiter
- Created timestamp
- Updated timestamp

Public users can:

- View jobs
- Search jobs
- Filter jobs by location
- Paginate job results

Example:

```text
GET /jobs?search=python&location=remote&skip=0&limit=10
```

---

# 🏢 Company Management

Recruiters can create and manage companies they own.

Each company contains:

- Company name
- Description
- Website
- Location
- Recruiter
- Created timestamp
- Updated timestamp

Company names are protected with a database-level uniqueness constraint.

Example:

```text
GET /companies?skip=0&limit=10
```

---

# 📩 Job Applications

Candidates can apply to jobs.

An application contains:

- Job ID
- Candidate ID
- Cover letter
- Status
- Created timestamp
- Updated timestamp

The API prevents duplicate applications.

A candidate can apply to the same job only once.

This is enforced using a database-level unique constraint:

```text
(job_id, candidate_id)
```

---

# 🔄 Application Status Workflow

Applications use the following status values:

```text
APPLIED
   |
   v
SHORTLISTED
   |
   v
INTERVIEW
   |
   +--------> REJECTED
   |
   v
HIRED
```

Available statuses:

```text
applied
shortlisted
interview
rejected
hired
```

Recruiters can update application status only for applications belonging to their own jobs.

---

# 🗄️ Database Design

Main entities:

```text
                 ┌──────────────┐
                 │    Users     │
                 └──────┬───────┘
                        |
             ┌──────────┴──────────┐
             |                     |
             v                     v
      ┌─────────────┐       ┌─────────────┐
      │  Companies  │       │    Jobs     │
      └─────────────┘       └──────┬──────┘
                                   |
                                   v
                            ┌──────────────┐
                            │ Applications │
                            └──────┬───────┘
                                   |
                                   v
                                 Users
```

## Users

Stores:

- ID
- Full name
- Email
- Password hash
- Role
- Created timestamp
- Updated timestamp

## Companies

Stores:

- ID
- Name
- Description
- Website
- Location
- Recruiter ID
- Created timestamp
- Updated timestamp

## Jobs

Stores:

- ID
- Title
- Description
- Location
- Employment type
- Recruiter ID
- Created timestamp
- Updated timestamp

## Applications

Stores:

- ID
- Job ID
- Candidate ID
- Cover letter
- Status
- Created timestamp
- Updated timestamp

---

# 📊 Pagination

List endpoints support offset-based pagination.

Parameters:

```text
skip
limit
```

Example:

```text
GET /jobs?skip=20&limit=10
```

This returns a maximum of 10 jobs starting from offset 20.

Pagination limits prevent excessively large API responses.

Pagination is implemented for:

- Jobs
- Companies
- Candidate applications
- Job applications

---

# 🔎 Job Search and Filtering

The job listing endpoint supports search and location filtering.

Search jobs:

```text
GET /jobs?search=python
```

Search with location:

```text
GET /jobs?search=python&location=remote
```

Search with pagination:

```text
GET /jobs?search=backend&location=delhi&skip=0&limit=10
```

---

# 🌐 API Endpoints

## Authentication

| Method | Endpoint         | Access        | Description           |
| ------ | ---------------- | ------------- | --------------------- |
| POST   | `/auth/register` | Public        | Register candidate    |
| POST   | `/auth/login`    | Public        | Login and receive JWT |
| GET    | `/auth/me`       | Authenticated | Get current user      |

## Jobs

| Method | Endpoint         | Access    | Description      |
| ------ | ---------------- | --------- | ---------------- |
| POST   | `/jobs`          | Recruiter | Create job       |
| GET    | `/jobs`          | Public    | List/search jobs |
| GET    | `/jobs/{job_id}` | Public    | Get job          |
| PUT    | `/jobs/{job_id}` | Job Owner | Update job       |
| DELETE | `/jobs/{job_id}` | Job Owner | Delete job       |

## Companies

| Method | Endpoint                  | Access        | Description    |
| ------ | ------------------------- | ------------- | -------------- |
| POST   | `/companies`              | Recruiter     | Create company |
| GET    | `/companies`              | Public        | List companies |
| GET    | `/companies/{company_id}` | Public        | Get company    |
| PUT    | `/companies/{company_id}` | Company Owner | Update company |
| DELETE | `/companies/{company_id}` | Company Owner | Delete company |

## Applications

| Method | Endpoint                                | Access    | Description               |
| ------ | --------------------------------------- | --------- | ------------------------- |
| POST   | `/applications/jobs/{job_id}`           | Candidate | Apply to job              |
| GET    | `/applications/my`                      | Candidate | View own applications     |
| GET    | `/applications/job/{job_id}`            | Job Owner | View job applications     |
| PUT    | `/applications/{application_id}/status` | Job Owner | Update application status |

## Health

| Method | Endpoint  | Access | Description     |
| ------ | --------- | ------ | --------------- |
| GET    | `/`       | Public | API information |
| GET    | `/health` | Public | Health check    |

---

# 📚 API Documentation

FastAPI automatically generates OpenAPI documentation.

## Swagger UI

```text
/docs
```

Production:

https://hireflow-api-nso3.onrender.com/docs

## OpenAPI Schema

```text
/openapi.json
```

---

# ⚠️ Error Handling

The API uses standard HTTP status codes.

Common responses:

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Validation Error
```

Examples of handled errors:

- Invalid request body
- Invalid email
- Invalid credentials
- Missing authentication
- Invalid JWT
- Expired JWT
- Unauthorized role
- Resource not found
- Duplicate email
- Duplicate application
- Unauthorized ownership access
- Invalid pagination parameters

---

# 🔄 Database Migrations

HireFlow uses Alembic for database schema migrations.

Create a migration:

```bash
alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback the latest migration:

```bash
alembic downgrade -1
```

Migration files are stored in:

```text
alembic/versions/
```

---

# ⚙️ Environment Variables

Create a `.env` file locally.

Example:

```env
APP_ENV=development
APP_NAME=HireFlow API
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/hireflow_db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The repository contains:

```text
.env.example
```

for configuration reference.

## Security

Never commit `.env` or production secrets to Git.

---

# 💻 Local Development

## 1. Clone Repository

```bash
git clone https://github.com/its-dp-coder/Hireflow-api.git
cd Hireflow-api
```

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create:

```text
.env
```

Use `.env.example` as a template.

Make sure PostgreSQL is running and the required database exists.

## 5. Run Database Migrations

```bash
alembic upgrade head
```

## 6. Start the API

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Running Tests

HireFlow uses pytest for automated API testing.

Run the complete test suite:

```bash
pytest
```

Current test suite:

```text
48 tests
```

The tests cover:

- Root endpoint
- Health endpoint
- User registration
- Duplicate registration
- Login
- JWT authentication
- Current user endpoint
- Role-based authorization
- Job CRUD
- Job ownership
- Job search
- Job location filtering
- Job pagination
- Company CRUD
- Company ownership
- Company pagination
- Job applications
- Duplicate application prevention
- Application ownership
- Application status updates
- Application pagination

Tests run against a dedicated PostgreSQL test database.

---

# 🐳 Docker

HireFlow is fully containerized using Docker.

## Build Docker Image

```bash
docker build -t hireflow-api .
```

## Run Container

```bash
docker run --name hireflow-api-container --env-file .env -p 8000:8000 hireflow-api
```

The Docker container supports the `PORT` environment variable for cloud deployments and falls back to port `8000` locally.

Health check:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 🔁 Continuous Integration

GitHub Actions is configured to run automatically on:

- Push to `main`
- Pull requests targeting `main`

Workflow:

```text
Git Push / Pull Request
          |
          v
   Checkout Repository
          |
          v
      Setup Python
          |
          v
   Install Dependencies
          |
          v
      Run pytest
          |
          v
   Build Docker Image
          |
          v
        Success
```

The CI pipeline uses PostgreSQL as a service container so automated tests run against PostgreSQL.

Workflow file:

```text
.github/workflows/ci.yml
```

---

# ☁️ Deployment

HireFlow is deployed as a Docker Web Service on Render.

Production URL:

https://hireflow-api-nso3.onrender.com

Deployment architecture:

```text
                 GitHub
                   |
                   | Push to main
                   v
            GitHub Actions
              /         \
             v           v
          pytest      Docker Build
             \           /
              \         /
               v       v
                  Render
                    |
          ┌─────────┴─────────┐
          |                   |
          v                   v
     Web Service          PostgreSQL
          |                   |
          └─────────┬─────────┘
                    |
                    v
              Production API
```

Production configuration is provided through Render environment variables.

Secrets are not stored in the Git repository.

---

# 🔒 Security

Security practices implemented in the project include:

- JWT authentication
- Bearer token authorization
- bcrypt password hashing
- Passwords never stored in plain text
- Role-Based Access Control
- Resource ownership validation
- Database foreign keys
- Database unique constraints
- Input validation using Pydantic
- Environment-based secrets
- `.env` excluded from Git
- Pagination limits
- Authentication on protected resources

---

# 🧪 Testing Strategy

The project follows an automated testing approach instead of relying only on manual Swagger testing.

The test suite uses:

```text
FastAPI TestClient
        +
pytest
        +
PostgreSQL Test Database
        |
        v
Automated API Verification
```

Test fixtures provide database isolation so test data does not affect development data.

---

# 📋 Production Readiness Checklist

- [x] REST API
- [x] FastAPI
- [x] PostgreSQL
- [x] SQLAlchemy ORM
- [x] JWT Authentication
- [x] Password Hashing
- [x] Role-Based Access Control
- [x] Resource Ownership Authorization
- [x] Input Validation
- [x] Database Constraints
- [x] Pagination
- [x] Search and Filtering
- [x] Job Application Workflow
- [x] Automated Tests
- [x] Docker
- [x] Alembic Migrations
- [x] GitHub Actions CI
- [x] Environment Variables
- [x] Health Check
- [x] Swagger/OpenAPI Documentation
- [x] Render Deployment

---

# 🚀 Future Improvements

Possible future enhancements:

- Refresh token support
- Email verification
- Password reset
- Candidate profile management
- Recruiter profile management
- Resume upload
- Cloud object storage
- Job categories
- Skills and technology tags
- Advanced job filtering
- Application history/timeline
- Email notifications
- Background jobs
- Redis caching
- Rate limiting
- Structured logging
- Centralized exception handling
- API versioning
- Monitoring and observability
- Automated production deployment
- Search optimization
- Job recommendation system

---

# 🎯 Learning Outcomes

This project demonstrates practical backend development skills including:

- REST API design
- FastAPI
- Dependency Injection
- JWT Authentication
- Authorization
- Role-Based Access Control
- Password Security
- SQLAlchemy ORM
- PostgreSQL
- Relational Database Design
- Foreign Keys
- Unique Constraints
- Database Migrations
- Automated Testing
- Docker
- GitHub Actions
- CI pipelines
- Environment Configuration
- Cloud Deployment
- API Documentation
- Backend Security

---

# 👨‍💻 Author

**Dependra Pratap Singh**

GitHub:

https://github.com/its-dp-coder

---

# 📄 License

This project was created for learning, portfolio, and interview demonstration purposes.
