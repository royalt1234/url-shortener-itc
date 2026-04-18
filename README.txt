# URL Shortener with Analytics

A simple but powerful URL shortening service built with FastAPI and vanilla JavaScript. Perfect for demonstrating Docker containerization and Kubernetes orchestration in presentations.

## 🎯 Quick Access

- **New to the project?** → Start with [Local Development](#local-development)
- **Want to present?** → Jump to [Kubernetes with Helm (Demo)](#deploy-with-helm-recommended)
- **Need full details?** → See [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md)

## Features

- **URL Shortening**: Create short links from long URLs
- **Custom Codes**: Optional custom short codes
- **Analytics**: Track clicks with detailed metadata (IP, user agent, referrer)
- **Real-time Dashboard**: View all links with live statistics
- **RESTful API**: Well-documented endpoints for integration
- **Horizontally Scalable**: Designed to scale with Kubernetes
- **Infrastructure as Code**: Helm charts for repeatable deployments

## Deployment Options Comparison

| Method | Best For | Setup Time | Complexity | Demo-Ready |
|--------|----------|-----------|-----------|-----------|
| **Local Python** | Development | < 2 min | Low | ❌ No |
| **Docker Compose** | Local testing | 5 min | Low | ✅ Yes |
| **Kubernetes (kubectl) YAML** | Learning K8s | 10 min | Medium | ✅ Yes |
| **Kubernetes (Helm)** | Production + Demo | 5 min | Medium | ✅ Yes |

## Quick Start

### Local Development

#### Prerequisites
- Python 3.11+
- Node.js (for frontend, or use with any web server)

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

#### Frontend Setup

Simply open `frontend/index.html` in a browser or serve with a web server:

```bash
cd frontend
python -m http.server 8080
# Or use any web server: npx http-server, etc.
```

Frontend will be available at `http://localhost:8080`

### Docker

#### Build and Run with Docker Compose

```bash
docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

#### Build Docker Image

```bash
cd backend
docker build -t url-shortener:latest .
docker run -p 8000:8000 url-shortener:latest
```

### Kubernetes

#### Deploy with Helm (Recommended)

The simplest way to deploy the entire application:

```bash
# Demo/Presentation setup (optimized for HPA scaling demo)
helm install url-shortener ./helm/url-shortener \
  -f helm/values-demo.yaml \
  --create-namespace --namespace url-shortener

# Watch it deploy
kubectl get pods -n url-shortener -w
```

**What gets deployed:**
- ✅ 2 backend replicas with health checks
- ✅ 2 frontend replicas (auto-scales to 5)
- ✅ Services for both frontend and backend
- ✅ ConfigMaps for configuration
- ✅ Horizontal Pod Autoscaler (HPA)

**Access the application:**
```bash
kubectl port-forward -n url-shortener svc/url-shortener-frontend 3000:80
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

#### Other Helm Deployment Options

```bash
# Development (minimal resources)
helm install url-shortener ./helm/url-shortener \
  -f helm/values-dev.yaml \
  --create-namespace --namespace url-shortener-dev

# Production (high availability)
helm install url-shortener ./helm/url-shortener \
  -f helm/values-production.yaml \
  --create-namespace --namespace url-shortener
```

See [HELM_DEPLOYMENT.md](HELM_DEPLOYMENT.md) for complete Helm options and customization.

#### Alternative: Direct YAML Deployment

If you prefer direct Kubernetes manifests:

```bash
kubectl create namespace url-shortener
kubectl apply -f k8s/backend-deployment.yaml -n url-shortener
kubectl apply -f k8s/frontend-deployment.yaml -n url-shortener
kubectl get pods -n url-shortener
```

#### Port Forward for Local Testing

```bash
# Backend
kubectl port-forward -n url-shortener svc/url-shortener-backend 8000:8000

# Frontend
kubectl port-forward -n url-shortener svc/url-shortener-frontend 3000:80
```

## Helm at a Glance

**Helm** is the "package manager for Kubernetes." It lets you:
- ✅ Define complex applications declaratively
- ✅ Reuse templates across environments (dev/staging/prod)
- ✅ Override values without editing YAML files
- ✅ Track versions and rollback easily
- ✅ Share applications with others

**Key Helm commands for this project:**

```bash
# Install
helm install url-shortener ./helm/url-shortener

# Check status
helm status url-shortener -n url-shortener

# Update
helm upgrade url-shortener ./helm/url-shortener -f values-production.yaml

# Uninstall
helm uninstall url-shortener -n url-shortener

# Rollback
helm rollback url-shortener -n url-shortener
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

## Presentation Talking Points

### 🐳 Docker Concepts to Demonstrate

1. **Containerization**: Show `Dockerfile` and explain layers
2. **Image Caching**: Demonstrate layer reuse (`docker build` twice)
3. **Volume Mounting**: Hot-reload code changes with `-v`
4. **Port Mapping**: Explain container:host port mapping
5. **CORS**: Show how containers communicate across networks

### ☸️ Kubernetes Concepts to Demonstrate

1. **Deployments**: Show 2 backend replicas running simultaneously
2. **Services**: Internal (ClusterIP) vs External (LoadBalancer) networking
3. **ConfigMaps**: Environment-specific configuration without rebuilding images
4. **Horizontal Pod Autoscaler (HPA)**: Watch pods scale based on CPU
5. **Health Checks**: Liveness and readiness probes keeping pods healthy
6. **Resource Management**: CPU/memory requests and limits
7. **Load Balancing**: Service automatically routes traffic across pods

### 📦 Helm Benefits to Showcase

1. **Infrastructure as Code**: Define entire application in YAML templates
2. **Environment Management**: Same chart, different `values-*.yaml` files
3. **Templating**: Show how Helm reduces YAML duplication
4. **Package Management**: Install/upgrade/rollback entire applications
5. **Reusability**: Share charts across teams and organizations

## Live Demo: Kubernetes Autoscaling with Helm

This is the **centerpiece demo** for your Kubernetes presentation.

### Pre-Demo Checklist

```bash
# 1. Build the Docker image
cd backend
docker build -t url-shortener:latest .
cd ..

# 2. Deploy with Helm
helm install url-shortener ./helm/url-shortener \
  -f helm/values-demo.yaml \
  --create-namespace --namespace url-shortener

# 3. Wait for pods to be ready
kubectl get pods -n url-shortener -w
# (Press Ctrl+C when all pods show "Running" and "1/1")
```

### Demo Flow (10 minutes)

**Setup (2 minutes)**

```bash
# Terminal 1: Show the Helm deployment
helm status url-shortener -n url-shortener
helm get values url-shortener -n url-shortener

# Terminal 2: Watch pods and HPA in real-time
kubectl get hpa,pods -n url-shortener -w

# Terminal 3: Port forward
kubectl port-forward -n url-shortener svc/url-shortener-frontend 3000:80 &
```

**The Demo (8 minutes)**

```bash
# Terminal 4: Start the load test
hey -z 30s -c 100 http://localhost:3000/

# Watch Terminal 2 - pods scale from 2 → 3 → 4 → 5
# Explain what's happening as it scales
```

### What Your Audience Sees

1. **Baseline**: 2 frontend pods running
   ```
   NAME                                    READY   STATUS    REPLICAS
   pod/url-shortener-frontend-xxx          1/1     Running   ✓
   pod/url-shortener-frontend-yyy          1/1     Running   ✓
   hpa/url-shortener-frontend-hpa          0%/70%              2
   ```

2. **Under Load**: CPU hits 70%, new pods appear instantly
   ```
   pod/url-shortener-frontend-xxx          1/1     Running   ✓
   pod/url-shortener-frontend-yyy          1/1     Running   ✓
   pod/url-shortener-frontend-zzz          0/1     Pending   ✗ (NEW!)
   pod/url-shortener-frontend-www          0/1     Pending   ✗ (NEW!)
   hpa/url-shortener-frontend-hpa          85%/70%             4
   ```

3. **Scaled Up**: All new pods become ready
   ```
   NAME                                    READY   STATUS    REPLICAS
   pod/url-shortener-frontend-xxx          1/1     Running   ✓
   pod/url-shortener-frontend-yyy          1/1     Running   ✓
   pod/url-shortener-frontend-zzz          1/1     Running   ✓
   pod/url-shortener-frontend-www          1/1     Running   ✓
   hpa/url-shortener-frontend-hpa          45%/70%             4
   ```

4. **Cool Down**: After load stops, pods scale back down
   ```
   (After ~1 minute of idle)
   NAME                                    READY   STATUS    REPLICAS
   pod/url-shortener-frontend-xxx          1/1     Running   ✓
   pod/url-shortener-frontend-yyy          1/1     Running   ✓
   hpa/url-shortener-frontend-hpa          5%/70%              2
   ```

### Demo Talking Points

```
"I've deployed this application using Helm - a Kubernetes package manager.
Notice how we went from raw YAML files to a single: 'helm install' command.

Right now we have 2 frontend replicas. Let me simulate traffic..."

[Run load test in Terminal 4]

"See what's happening? The HPA (Horizontal Pod Autoscaler) is watching the CPU.
When it exceeded 70%, Kubernetes automatically spun up 2 more pods.

Now we have 4 replicas sharing the load. This is *true* autoscaling - no manual 
intervention, no ops team needed. It happened automatically based on demand.

Let's wait for the load to stop..."

[Wait 1-2 minutes]

"And there it goes - back down to 2 pods. Kubernetes is saving resources by 
removing pods we don't need. This is efficiency at scale."
```

### Load Testing Options

**Option 1: Using `hey` (Recommended)**

```bash
# Install hey
# Windows: choco install hey
# Mac: brew install hey
# Linux: go install github.com/rakyll/hey@latest

# Light load
hey -n 1000 -c 10 http://localhost:3000/

# Heavy load (triggers scaling)
hey -n 10000 -c 100 http://localhost:3000/

# Sustained load (best for presentations - 30 seconds)
hey -z 30s -c 100 http://localhost:3000/
```

**Option 2: In-Cluster Load Testing**

```bash
# Deploy load generator pod
kubectl run -n url-shortener load-generator --image=busybox --restart=Never -- \
  /bin/sh -c "while true; do wget -q -O- http://url-shortener-frontend; done"

# Watch scaling in Terminal 2
# Clean up when done
kubectl delete pod -n url-shortener load-generator
```

**Option 3: Python (No Installation Required)**

```bash
python -c "
import urllib.request
import threading

def hammer():
    for i in range(500):
        try:
            urllib.request.urlopen('http://localhost:3000/', timeout=5)
        except:
            pass

threads = [threading.Thread(target=hammer) for _ in range(20)]
for t in threads:
    t.start()
for t in threads:
    t.join()
"
```

### FAQ During Demo

**Q: Can the pods really talk to each other?**
A: Yes! Services provide a stable internal network (ClusterIP). Each pod can reach others by service name.

**Q: What if a pod crashes?**
A: The Deployment controller immediately replaces it. Show with `kubectl delete pod <name>` - a new one appears instantly.

**Q: Why only scale to 5 pods?**
A: It's configured in `values-demo.yaml`. We can change it, but 5 is good for a demo. Production might be 10+.

**Q: Would I need to restart the app?**
A: Nope! Kubernetes handles new pod startup. Traffic is seamlessly routed to new replicas via the Service.

## Cleanup

After your presentation:

```bash
# Remove the Helm deployment
helm uninstall url-shortener -n url-shortener

# Delete the namespace
kubectl delete namespace url-shortener
```

## Load Testing Troubleshooting

- **Pods won't scale?** → Check resource requests are set (`kubectl describe node`)
- **Load test too fast?** → Use `hey -z 60s -c 50` for longer, gentler load
- **Some pods not starting?** → Check logs: `kubectl logs -n url-shortener <pod-name>`

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

- Database defaults to SQLite for simplicity. For production K8s, upgrade to PostgreSQL
- Frontend is intentionally simple HTML/JS to avoid build step complexity
- CORS is wide open for presentation purposes; tighten in production
- Consider adding Redis for caching in advanced demos

## License

MIT
