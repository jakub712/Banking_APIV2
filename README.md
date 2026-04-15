[README(2).md](https://github.com/user-attachments/files/26748110/README.2.md)
# Banking API v2
A backend REST API simulating core banking operations: authentication, account management, and financial transactions. Built with FastAPI, PostgreSQL, SQLAlchemy, and Docker.

---

## What it does
Register users, create bank accounts, and move money between them. Every operation is authenticated via JWT, ownership is enforced server-side, and all monetary values are stored as integers to avoid floating-point arithmetic errors. An admin role provides system-wide visibility over users and transactions.

---

## How it's built

### Money as integers
All balances and transaction amounts are stored in pence as INTEGER columns, never FLOAT. Floating-point arithmetic is unreliable for financial data, 0.1 + 0.2 in Python is 0.30000000000000004. Storing in pence and dividing by 100 only at the display layer means the numbers stay exact throughout.

### Ownership enforced from the JWT
When a user makes a request, their account is looked up using the user ID extracted from the JWT payload not from anything the client sends in the request body. This closes a common vulnerability where a user could manipulate a request parameter to act on someone else's account. The client has no say in whose account is being accessed.

### Atomic transactions with rollback
Every deposit, withdrawal, and transfer is wrapped in a try/except block. If anything fails mid-operation for example: balance update, transaction record creation, commit. The database rolls back to its state before the request. This prevents partial writes where a balance gets debited but the transaction record never gets written, or a transfer deducts from the sender without crediting the receiver.

### RBAC and admin bootstrap
The role system has two levels: user and admin. The bootstrap flow allows the first registered user to self-promote to admin via /auth/create_admin. After that, the endpoint is locked and only existing admins can promote others via /auth/promote/{user_id}. This prevents the chicken-and-egg problem of needing an admin to create the first admin, while blocking any subsequent user from grabbing the role themselves.

### JWT authentication
Tokens are signed with HS256 and include the user's ID, username, and role in the payload. The secret key and algorithm are loaded from environment variables, never hardcoded. Tokens expire after 20 minutes.

---

## Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/create` | Register a new user |
| POST | `/auth/token` | Login, returns JWT |
| POST | `/auth/create_admin` | First user self-promotes to admin |
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
| POST | `/transactions/transfer/{account_id}` | Transfer to another account |
| GET | `/transactions/all` | Get own transaction history |

---

## Setup

### Requirements
- Docker + Docker Compose

### 1. Clone the repo

```bash
git clone https://github.com/jakub712/Banking_APIV2
cd Banking_APIV2
```

### 2. Create a `.env` file

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
DATABASE_URL=postgresql://postgres:password@db:5432/banking
```

Generate a secret key:

```bash
openssl rand -hex 32
```

### 3. Run with Docker

```bash
docker compose up --build
```

API available at `http://localhost:8000`. Postgres starts first. Docker Compose waits for the health check to pass before launching the API.

### 4. Interactive docs

```
http://localhost:8000/docs
```

---

## Running tests

Tests use SQLite in-memory so no database setup is needed.

```bash
pytest app/testing/
```

The test suite covers:
- User registration and login
- Account creation and retrieval
- Deposits, withdrawals, and transfers
- Admin role enforcement

---

## Stack

- **FastAPI** - web framework
- **PostgreSQL** - production database
- **SQLAlchemy** - ORM
- **Docker + Docker Compose** - containerised deployment
- **python-jose** - JWT
- **passlib / bcrypt** - password hashing
- **pytest** - test suite
- **python-dotenv** - environment config
