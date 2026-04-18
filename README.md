# URL Shortener with Analytics

A powerful URL shortening service built with FastAPI and vanilla JavaScript. This project includes configurations for various deployment strategies, including local development, Docker environments, and Kubernetes orchestration.

## Features

- **URL Shortening**: Create short links from long URLs
- **Custom Codes**: Optional custom short codes
- **Analytics**: Track clicks with detailed metadata (IP, user agent, referrer)
- **Real-time Dashboard**: View all links with live statistics
- **RESTful API**: Well-documented endpoints for integration
- **Horizontally Scalable**: Designed to scale with Kubernetes
- **Infrastructure as Code**: Helm charts and Kubernetes manifests for repeatable deployments

## Deployment Options Comparison

| Method | Best For | Setup Time | Complexity |
|--------|----------|-----------|-----------|
| **Local Python** | Development | < 2 min | Low |
| **Docker Compose** | Local testing | 5 min | Low |
| **Kubernetes (kubectl) YAML** | Learning K8s | 10 min | Medium |
| **Kubernetes (Helm)** | Production | 5 min | Medium |

## Quick Start

### Local Development

#### Prerequisites
- Python 3.11+
- Node.js (for frontend optional tools, or use with any web server)

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

The Backend API will be available at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### Frontend Setup

Serve the frontend directory using any web server. For example:

```bash
cd frontend
python -m http.server 8080
# Or use npx: npx http-server
```

The Frontend will be available at `http://localhost:8080`

### Docker Deployment

#### Docker Compose

To build and run both the frontend and backend using Docker Compose:

```bash
docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

#### Standalone Docker Build

If you only want to build and run the backend container:

```bash
cd backend
docker build -t url-shortener:latest .
docker run -p 8000:8000 url-shortener:latest
```

### Kubernetes Deployment

#### Deploy with Helm (Recommended)

Helm is the recommended way to deploy the application in Kubernetes as it handles the deployment of all necessary components (Deployments, Services, ConfigMaps, HPA).

```bash
# Basic deployment
helm install url-shortener ./helm/url-shortener \
  --create-namespace --namespace url-shortener

# Check deployment status
kubectl get pods -n url-shortener -w
```

**Access the application:**
```bash
kubectl port-forward -n url-shortener svc/url-shortener-frontend 3000:80
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

#### Environment-Specific Helm Deployments

```bash
# Development
helm install url-shortener ./helm/url-shortener \
  -f helm/values-dev.yaml \
  --create-namespace --namespace url-shortener-dev

# Production
helm install url-shortener ./helm/url-shortener \
  -f helm/values-production.yaml \
  --create-namespace --namespace url-shortener
```

See [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md) for complete Helm options and customization.

#### Alternative: Direct YAML Deployment

If you prefer to apply raw Kubernetes manifests:

```bash
kubectl create namespace url-shortener
kubectl apply -f k8s/backend-deployment.yaml -n url-shortener
kubectl apply -f k8s/frontend-deployment.yaml -n url-shortener
kubectl get pods -n url-shortener
```

**Port Forward for Testing:**

```bash
# Backend
kubectl port-forward -n url-shortener svc/url-shortener-backend 8000:8000

# Frontend
kubectl port-forward -n url-shortener svc/url-shortener-frontend 3000:80
```

## API Endpoints

### Create Short Link
```bash
POST /shorten?original_url=<url>&custom_code=<code>&title=<title>
```

### Redirect
```bash
GET /<short_code>
# Redirects to original URL and logs analytics
```

### Get All Links
```bash
GET /api/links
```

### Get Analytics for Link
```bash
GET /api/analytics/<short_code>
```

### Get Overall Statistics
```bash
GET /api/stats
```

### Delete Link
```bash
DELETE /api/links/<short_code>
```

### Health Check
```bash
GET /health
```

## Architecture

```
┌─────────────────────────────────────────────┐
│         Browser / Client                    │
└─────────────────┬───────────────────────────┘
                  │
         ┌────────▼──────────┐
         │   Frontend (HTML) │
         │  (Nginx + CORS)   │
         └────────┬──────────┘
                  │
    ┌─────────────▼──────────────┐
    │   Backend API (FastAPI)    │
    │  ┌──────────────────────┐  │
    │  │    URL Shortening    │  │
    │  │    Analytics Logic   │  │
    │  └──────────┬───────────┘  │
    │             │              │
    │        ┌────▼─────┐        │
    │        │  SQLite  │        │
    │        │ Database │        │
    │        └──────────┘        │
    └────────────────────────────┘
```

## Project Structure

```
url-shortener/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database setup
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── .env.example         # Environment variables
├── frontend/
│   └── index.html           # Single-page application
├── k8s/
│   ├── backend-deployment.yaml
│   └── frontend-deployment.yaml
├── docker-compose.yml       # Local development setup
└── README.md               # This file
```

## Notes

- Database defaults to SQLite for simplicity out of the box. For a robust production K8s deployment, consider configuring a PostgreSQL database.
- The frontend is intentionally a simple HTML/JS architecture to minimize build-step complexity.

## License

MIT
