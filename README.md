# Banking API v2 (FastAPI)

A backend REST API simulating core banking operations — authentication, account management, and financial transactions. Built with FastAPI and SQLAlchemy.

---

## Features

- JWT authentication with bcrypt password hashing
- Role-based access control (user / admin)
- One account per user with server-side ownership enforcement
- Deposits, withdrawals, and transfers between accounts
- Atomic transaction handling with rollback on failure
- Admin endpoints for user and transaction management
- Integer (pence) storage for all monetary values — no floating-point errors
- Secrets managed via environment variables

---

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **SQLite** — database
- **python-jose** — JWT
- **passlib / bcrypt** — password hashing
- **python-dotenv** — environment config
- **Uvicorn** — ASGI server

---

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/jakub712/Banking_APIV2
cd Banking_APIV2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

Generate a secret key:

```bash
openssl rand -hex 32
```

### Run

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/create` | Register a new user |
| POST | `/auth/token` | Login, returns JWT |
| POST | `/auth/create_admin` | Promote first user to admin |
| POST | `/auth/promote/{user_id}` | Admin: promote another user to admin |
| GET | `/auth/all_users` | Admin: list all users |
| GET | `/auth/all_transactions` | Admin: list all transactions |
| GET | `/auth/{user_name}` | Admin: get user details |

### Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts/create` | Create a bank account |
| GET | `/accounts/get_user` | Get own account details |

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions/deposit` | Deposit funds |
| POST | `/transactions/withdraw` | Withdraw funds |
| POST | `/transactions/transfer/{user_id}` | Transfer to another user |
| GET | `/transactions/all` | Get own transaction history |

---

## Security

- All routes except `/auth/create` and `/auth/token` require a valid JWT
- Ownership is enforced server-side from the JWT — not from request parameters
- Admin role required for system-wide data access
- No credentials or database files committed to version control
