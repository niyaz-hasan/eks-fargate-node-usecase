# 🐍 Employee Directory – Flask API

A minimal REST API that powers the internal **Employee Directory**.  
Built with **Flask + SQLAlchemy** and protected with **JWT access-tokens**.

| Stack piece | Why we use it |
|-------------|---------------|
| **Flask** | Fast, lightweight HTTP framework |
| **Flask-SQLAlchemy** | Integrates SQLAlchemy ORM with Flask lifecycle |
| **Flask-JWT-Extended** | Issues & validates JSON Web Tokens |
| **Flask-CORS** | Adds CORS headers so the React SPA (different origin) can call the API |
| **PyMySQL** | Pure-Python MySQL driver (SQLAlchemy talks to RDS through this) |
| **Gunicorn** | Production WSGI process manager (multi-worker) |

## 📂 Repo Structure

```
backend/
├── app.py              # ⇐ application factory + startup retries
├── config.py           # env-driven settings (DB URI, JWT secret, …)
├── models.py           # SQLAlchemy models: Employee, User
├── routes.py           # /api/* blueprints (CRUD + auth)
├── requirements.txt    # pip packages
└── README.md           # ← you are here
```

## ⚙️ Configuration (env vars)

| Variable | Example | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `mysql+pymysql://user:pass@host:3306/employees` | RDS connection string |
| `JWT_SECRET_KEY` | `super-secret-string` | Symmetric key used to sign tokens |
| `DB_CONN_RETRIES` | `10` | How many times to retry RDS during start-up |
| `DB_CONN_DELAY` | `3`  | Seconds to wait between retries |

## ▶️ Running locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="sqlite:///local.db"
export JWT_SECRET_KEY="dev-secret"
python app.py
```

## 🆔 Auth flow

1. `POST /api/login` – user sends JSON `{"username":"alice","password":"p@ss"}`  
2. Receives:
```json
{
  "access_token": "<JWT>",
  "expires_in": 3600
}
```
3. Use it in header: `Authorization: Bearer <JWT>`

## 📚 Main API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/login` | Get JWT token |
| `GET`  | `/api/employees` | List/search (`?search=<term>`) |
| `POST` | `/api/employees` | Create new employee |
| `PUT`  | `/api/employees/<id>` | Update employee |
| `DELETE` | `/api/employees/<id>` | Delete employee |
| `GET`  | `/api/healthz` | K8s probe |

## 🐳 Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## ☸️ Kubernetes

* **Namespace**: backend
* **Ingress**: `/api/* → backend Service`
* **IRSA role**: reads secrets from AWS Secrets Manager
* **Deployment**: nodeSelector → EC2 only

## 🚀 GitHub Actions (CI/CD)

* Build image from `backend/`
* Push to ECR: `support-portal-backend`
* Patch EKS Deployment with new tag

---

>  Secure with bcrypt, token refresh, and HTTPS headers. Use AWS Secrets Manager for secrets.