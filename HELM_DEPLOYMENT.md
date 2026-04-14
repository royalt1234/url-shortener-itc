# Helm Deployment Guide for URL Shortener

This guide covers deploying the URL Shortener application using Helm, the Kubernetes package manager.

## Prerequisites

- Kubernetes cluster running (minikube, Docker Desktop K8s, or cloud K8s)
- Helm 3.x installed ([installation guide](https://helm.sh/docs/intro/install/))
- `kubectl` configured and pointing to your cluster
- Docker image built: `docker build -t url-shortener:latest ./backend`

## Quick Start

### 1. Add the Helm Chart (if using repo, or deploy locally)

For local deployment:

```bash
helm install url-shortener ./helm/url-shortener \
  --create-namespace --namespace url-shortener
```

### 2. Check Deployment Status

```bash
# Watch the deployment
kubectl get pods -n url-shortener -w

# Check services
kubectl get svc -n url-shortener

# View the release
helm list -n url-shortener

# Get release details
helm status url-shortener -n url-shortener
```

### 3. Access the Application

```bash
# Port forward
kubectl port-forward -n url-shortener svc/url-shortener-frontend 3000:80 &
kubectl port-forward -n url-shortener svc/url-shortener-backend 8000:8000 &

# Open in browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

## Deployment Scenarios

### Development Deployment

```bash
helm install url-shortener ./helm/url-shortener \
  -f helm/values-dev.yaml \
  --create-namespace --namespace url-shortener-dev
```

**What it does:**
- 1 backend replica (saves resources)
- 1 frontend replica
- HPA disabled (no scaling)
- Minimal resource requests

### Demo/Presentation Deployment

```bash
helm install url-shortener ./helm/url-shortener \
  -f helm/values-demo.yaml \
  --create-namespace --namespace url-shortener
```

**What it does:**
- 2 backend replicas
- 2 frontend replicas (scales to 5)
- HPA enabled with 70% CPU threshold
- Perfect for load testing demo

### Production Deployment

```bash
helm install url-shortener ./helm/url-shortener \
  -f helm/values-production.yaml \
  --create-namespace --namespace url-shortener
```

**What it does:**
- 5 backend replicas (high availability)
- 3 frontend replicas (scales to 10)
- HPA enabled with 75% CPU threshold
- Higher resource limits

## Customizing Deployment

### Override Individual Values

```bash
helm install url-shortener ./helm/url-shortener \
  --set backend.replicaCount=5 \
  --set frontend.replicaCount=3 \
  --set frontend.autoscaling.maxReplicas=10 \
  --create-namespace --namespace url-shortener
```

### Using a Custom Values File

```bash
helm install url-shortener ./helm/url-shortener \
  -f custom-values.yaml \
  --create-namespace --namespace url-shortener
```

### Create Your Own Values File

```yaml
# my-values.yaml
backend:
  replicaCount: 4
  image:
    tag: v1.0.0

frontend:
  replicaCount: 3
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 8

config:
  databaseUrl: "postgresql://db-host:5432/urlshortener"
```

## Common Helm Commands

### View Chart Details

```bash
# Dry run - see what will be deployed
helm install url-shortener ./helm/url-shortener \
  --dry-run --debug

# Template - see rendered YAML files
helm template url-shortener ./helm/url-shortener

# Get chart values
helm show values ./helm/url-shortener
```

### Update Release

```bash
# Update with new values
helm upgrade url-shortener ./helm/url-shortener \
  -f helm/values-production.yaml \
  -n url-shortener

# Rollback to previous release
helm rollback url-shortener -n url-shortener

# View release history
helm history url-shortener -n url-shortener
```

### Uninstall Release

```bash
helm uninstall url-shortener -n url-shortener

# Also delete namespace
kubectl delete namespace url-shortener
```

## Helm Chart Structure

```
helm/url-shortener/
├── Chart.yaml                    # Chart metadata
├── values.yaml                   # Default values
├── templates/
│   ├── _helpers.tpl             # Template helpers
│   ├── namespace.yaml           # Namespace creation
│   ├── configmap.yaml           # Config and frontend files
│   ├── backend-deployment.yaml  # Backend deployment
│   ├── backend-service.yaml     # Backend service
│   ├── frontend-deployment.yaml # Frontend deployment
│   ├── frontend-service.yaml    # Frontend service
│   ├── frontend-hpa.yaml        # Horizontal Pod Autoscaler
│   └── frontend-configmap.yaml  # Frontend files
```

## Troubleshooting

### Check Helm Release

```bash
helm status url-shortener -n url-shortener
helm get values url-shortener -n url-shortener
helm get manifest url-shortener -n url-shortener
```

### View Detailed Logs

```bash
kubectl logs -n url-shortener -l app=url-shortener-backend
kubectl logs -n url-shortener -l app=url-shortener-frontend
```

### Describe Pods

```bash
kubectl describe pod -n url-shortener <pod-name>
```

### Check Events

```bash
kubectl get events -n url-shortener --sort-by='.lastTimestamp'
```

## Load Testing with Helm Deployment

### Set Up Port Forwarding

```bash
kubectl port-forward -n url-shortener svc/url-shortener-frontend 3000:80 &
kubectl get hpa -n url-shortener -w &
```

### Run Load Test

```bash
# Using hey (recommended)
hey -z 30s -c 100 http://localhost:3000/

# Or Python
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

You should see pods scaling up as CPU usage increases!

## Tips for Presentations

1. **Pre-pull images** to avoid download delays:
   ```bash
   docker pull nginx:alpine
   docker pull url-shortener:latest
   ```

2. **Use demo values** for consistent HPA behavior:
   ```bash
   helm install url-shortener ./helm/url-shortener \
     -f helm/values-demo.yaml \
     --create-namespace --namespace url-shortener
   ```

3. **Show Helm commands for IaC narrative**:
   ```bash
   # Show dry-run first
   helm install url-shortener ./helm/url-shortener --dry-run --debug | head -50
   
   # Then deploy
   helm install url-shortener ./helm/url-shortener ...
   ```

4. **Use watches for live visualization**:
   ```bash
   watch -n 1 'kubectl get pods,hpa -n url-shortener'
   ```

## Next Steps

- Explore [Helm Charts Hub](https://artifacthub.io/) for production charts
- Learn about [Helm Hooks](https://helm.sh/docs/topics/hooks/) for advanced deployments
- Explore [Chart Testing](https://helm.sh/docs/topics/chart_tests/) for chart validation
- Create a Helm chart repository for version control
