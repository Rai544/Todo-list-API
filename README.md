# Todo API – DevOps & Cloud Internship Task

A simple RESTful Todo API built with **Python and FastAPI** using in-memory storage.

The project demonstrates basic REST API development, containerization with Docker, and CI automation using GitHub Actions.

---

## 1. Project Overview

This project provides a simple Todo API that allows users to:

* Check whether the API is running
* Create new tasks
* List all tasks
* Mark a task as completed

The application stores tasks in a Python list in memory.

### Important

Because the application uses in-memory storage, all tasks are lost whenever the application restarts.

This approach was intentionally chosen because the internship task does not require a persistent database.

---

## 2. Technology Stack

* **Python 3**
* **FastAPI**
* **Uvicorn**
* **Pydantic** — used by FastAPI for request/data validation
* **Docker**
* **GitHub Actions**

---

## 3. Project Structure

```text
Todo-list-API/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
└── .github/
    └── workflows/
        └── main.yml
```

---

## 4. How the Application Works

The application maintains tasks using an in-memory Python list:

```python
tasks = []
```

Each task contains:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": false
}
```

The application also maintains an ID counter:

```python
next_id = 1
```

When a new task is created:

1. The API receives the task title.
2. The request body is validated.
3. A unique ID is assigned.
4. `completed` is initially set to `false`.
5. The task is added to the in-memory list.
6. The newly created task is returned to the client.

---

# 5. API Endpoints

| Method | Endpoint                | Purpose                  |
| ------ | ----------------------- | ------------------------ |
| GET    | `/`                     | Check API status         |
| POST   | `/tasks`                | Create a new task        |
| GET    | `/tasks`                | List all tasks           |
| PATCH  | `/tasks/{task_id}/done` | Mark a task as completed |

---

# 6. Endpoint 1 – API Status

## Request

```http
GET /
```

## Example

```bash
curl http://127.0.0.1:8000/
```

## Response

```json
{
  "message": "Todo API is running"
}
```

## How It Works

This endpoint provides a simple way to verify that the FastAPI application is running and responding to HTTP requests.

It is a basic status endpoint rather than a full production health/readiness check.

---

# 7. Endpoint 2 – Create a Task

## Request

```http
POST /tasks
```

## Request Body

The API expects a JSON object containing a task title.

Example:

```json
{
  "title": "Learn Docker"
}
```

## Example Using cURL

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker"}'
```

## Response

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": false
}
```

## How It Works

When this endpoint is called:

1. FastAPI receives the HTTP request.
2. The request body is validated.
3. The application reads the task title.
4. A unique ID is generated.
5. The task is created with `completed: false`.
6. The task is stored in the in-memory list.
7. The newly created task is returned.

Flow:

```text
Request
   |
   v
POST /tasks
   |
   v
Validate Request
   |
   v
Generate ID
   |
   v
Create Task
   |
   v
Store in Memory
   |
   v
Return Task
```

---

# 8. Endpoint 3 – List All Tasks

## Request

```http
GET /tasks
```

## Example

```bash
curl http://127.0.0.1:8000/tasks
```

## Example Response

```json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "completed": false
  },
  {
    "id": 2,
    "title": "Build CI/CD Pipeline",
    "completed": false
  },
  {
    "id": 3,
    "title": "Deploy Application to AWS",
    "completed": false
  }
]
```

## How It Works

The endpoint reads the current contents of the in-memory `tasks` list and returns all stored tasks.

No database query is performed because the application does not use a persistent database.

---

# 9. Endpoint 4 – Mark a Task as Completed

## Request

```http
PATCH /tasks/{task_id}/done
```

The `{task_id}` represents the ID of the task that should be completed.

## Example

To mark task `1` as completed:

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1/done
```

## Response

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": true
}
```

## How It Works

The application:

1. Receives the task ID.
2. Searches the in-memory task list.
3. Finds the task with the matching ID.
4. Changes `completed` from `false` to `true`.
5. Returns the updated task.

If no task matches the ID, the API returns HTTP 404 with `{"detail": "Task not found"}`.

Flow:

```text
PATCH /tasks/1/done
          |
          v
   Search Task ID 1
          |
          v
      Task Found?
       /       \
     Yes        No
      |          |
      v          v
completed     HTTP 404
= true        Task not found
      |
      v
Return Updated Task
```

---

# 10. Task Not Found

If the requested task ID does not exist, the API returns **HTTP 404**.

For example:

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/999/done
```

Response:

```json
{
  "detail": "Task not found"
}
```

---

# 11. Running the Application Locally

## Prerequisites

Make sure the following are installed:

* Python 3
* pip
* Git

---

## Step 1 – Clone the Repository

```bash
git clone https://github.com/Rai544/Todo-list-API.git
```

Move into the project directory:

```bash
cd Todo-list-API
```

---

## Step 2 – Create a Virtual Environment

### Linux/macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## Step 3 – Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
fastapi
uvicorn
```

FastAPI uses Pydantic internally for data validation, so it does not necessarily need to be listed separately in this simple project.

---

## Step 4 – Start the Application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

# 12. FastAPI Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

From the Swagger UI, you can:

* View all endpoints
* View request and response schemas
* Send POST requests
* Create tasks
* List tasks
* Mark tasks as completed

Swagger provides a convenient way to manually test the API.

---

# 13. Complete API Test

The following sequence demonstrates the complete application flow.

## Step 1 – Check API

```bash
curl http://127.0.0.1:8000/
```

Expected:

```json
{
  "message": "Todo API is running"
}
```

---

## Step 2 – Create Task 1

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker"}'
```

Expected:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": false
}
```

---

## Step 3 – Create Task 2

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Content-Type: application/json" \
-d '{"title":"Build CI/CD Pipeline"}'
```

Expected:

```json
{
  "id": 2,
  "title": "Build CI/CD Pipeline",
  "completed": false
}
```

---

## Step 4 – Create Task 3

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Content-Type: application/json" \
-d '{"title":"Deploy Application to AWS"}'
```

Expected:

```json
{
  "id": 3,
  "title": "Deploy Application to AWS",
  "completed": false
}
```

---

## Step 5 – List Tasks

```bash
curl http://127.0.0.1:8000/tasks
```

Expected:

```json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "completed": false
  },
  {
    "id": 2,
    "title": "Build CI/CD Pipeline",
    "completed": false
  },
  {
    "id": 3,
    "title": "Deploy Application to AWS",
    "completed": false
  }
]
```

---

## Step 6 – Complete Task 1

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1/done
```

Expected:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": true
}
```

---

## Step 7 – Verify the Updated List

```bash
curl http://127.0.0.1:8000/tasks
```

Expected:

```json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "completed": true
  },
  {
    "id": 2,
    "title": "Build CI/CD Pipeline",
    "completed": false
  },
  {
    "id": 3,
    "title": "Deploy Application to AWS",
    "completed": false
  }
]
```

This confirms that the PATCH operation successfully updated the task stored in memory.

---

# 14. Running with Docker

## Build the Docker Image

```bash
docker build -t todo-api .
```

## Run the Container

```bash
docker run -p 8000:8000 todo-api
```

The API will then be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 15. Docker Port Mapping

The command:

```bash
docker run -p 8000:8000 todo-api
```

maps the host port to the container port:

```text
Host Port 8000
      |
      v
Container Port 8000
      |
      v
FastAPI Application
```

The first `8000` is the **host port**.

The second `8000` is the **container port**.

For the application to be accessible through the Docker port mapping, Uvicorn should listen on `0.0.0.0` inside the container.

For example:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

This is normally configured in the Dockerfile's `CMD` or `ENTRYPOINT`.

---

# 16. GitHub Actions CI

The project includes a GitHub Actions workflow that automatically builds the Docker image whenever code is pushed to the `main` branch.

Example workflow:

```yaml
name: Docker Build

on:
  push:
    branches:
      - main

jobs:
  docker-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t todo-api .
```

## CI Flow

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    v
Checkout Code
    |
    v
Build Docker Image
    |
    v
Build Successful
```

The workflow currently verifies that the application can be successfully containerized after code changes.

It does **not** currently run automated API tests or deploy the application.

---

# 17. In-Memory Storage

This project intentionally uses an in-memory Python data structure instead of MySQL, PostgreSQL, MongoDB, or another persistent database.

Example:

```python
tasks = []
```

When the application starts:

```text
tasks = []
```

After creating three tasks:

```text
tasks = [
    {
        "id": 1,
        "title": "Learn Docker",
        "completed": False
    },
    {
        "id": 2,
        "title": "Build CI/CD Pipeline",
        "completed": False
    },
    {
        "id": 3,
        "title": "Deploy Application to AWS",
        "completed": False
    }
]
```

If the application restarts:

```text
tasks = []
```

All previously created tasks are lost.

This is the main limitation of the current implementation and is acceptable for the scope of this assignment.

---

# 18. API Architecture

```text
                    +----------------+
                    |     Client     |
                    +-------+--------+
                            |
                            |
                       HTTP Requests
                            |
                            v
                    +---------------+
                    |    FastAPI    |
                    +-------+-------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
       POST /tasks     GET /tasks    PATCH /tasks/{id}/done
              |             |             |
              +-------------+-------------+
                            |
                            v
                    +---------------+
                    | In-Memory     |
                    | Storage       |
                    |   tasks=[]    |
                    +---------------+
```

---

# 19. Endpoint Quick Reference

### Check API Status

```http
GET /
```

Returns:

```json
{
  "message": "Todo API is running"
}
```

### Create Task

```http
POST /tasks
```

Body:

```json
{
  "title": "Learn Docker"
}
```

### List Tasks

```http
GET /tasks
```

### Complete Task

```http
PATCH /tasks/{task_id}/done
```

---

# 20. Reflection

## What was the trickiest part?

The trickiest part was connecting the FastAPI application with Docker and GitHub Actions correctly.

I needed to understand how the FastAPI application should listen on `0.0.0.0` inside the Docker container so that the application could be accessed through the published Docker port.

I also needed to understand how GitHub Actions checks out the repository and uses the Dockerfile to build the application image automatically after a push to the `main` branch.

## Why did you make these choices?

I chose **FastAPI** because it provides a straightforward way to build REST APIs and automatically generates interactive Swagger documentation.

I used **in-memory storage** instead of a persistent database because the task does not require a database. This keeps the implementation simple and allows the focus to remain on API development, Docker, and CI.

I used **Docker** to package the application and its runtime environment consistently.

I used **GitHub Actions** to automatically verify that the Docker image can be successfully built whenever changes are pushed to the `main` branch.

## What would you improve with another day?

If I had another day, I would first add automated unit and API tests and execute them in GitHub Actions before the Docker build stage.

I would also improve error handling and validation, add structured logging, and scan the Docker image for known security vulnerabilities.

For a production-oriented version, I would replace the in-memory storage with PostgreSQL and add a deployment stage to the CI/CD pipeline.

---

# 21. Limitations

This project is intentionally kept simple for the internship task.

* Tasks are stored only in memory.
* Tasks are lost when the application restarts.
* There is no authentication or authorization.
* There is no persistent database.
* Automated tests are not currently included.
* The GitHub Actions workflow currently builds the Docker image but does not deploy it.

These limitations are acceptable for the scope of the assignment.

---

# 22. Future Improvements

If this project were extended beyond the internship task, possible improvements would include:

* PostgreSQL database
* Automated unit and integration tests
* Authentication and authorization
* Improved request validation
* Structured application logging
* Dedicated health and readiness endpoints
* Docker image optimization
* Container security scanning
* CI/CD deployment
* Cloud deployment using AWS ECS
* Infrastructure as Code using Terraform

---

# 23. Author

**Muhammad Shehbaz**

DevOps / Cloud Engineering

GitHub: `https://github.com/Rai544/`
