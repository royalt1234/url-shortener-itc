# URL Shortener App - Presentation Content

Use these talking points to guide your presentation. Each section corresponds to a key phase in the application lifecycle, from design to production-grade orchestration. 

---

## 1. App Structure & Design
**Goal:** Explain *what* we built before explaining *how* we run it.

*   **Architecture Pattern**: Client-Server architecture with a clean separation of concerns.
*   **Frontend**: 
    *   Simple, lightweight Single Page Application (SPA).
    *   Vanilla HTML/JS designed for simplicity—avoiding complex build tools to keep the focus on infrastructure.
*   **Backend & API**: 
    *   Built with **FastAPI** (Python 3.11).
    *   Handles core logic: generating short codes, processing redirects, and tracking rich analytics (IP, User Agent).
*   **Database**: 
    *   Uses **SQLite** by default. Extremely portable and requires zero external setup for initial testing, but seamlessly swappable to PostgreSQL in production.

---

## 2. Local Testing/Development, Git Flow, Linux
**Goal:** Explain the foundational developer experience.

*   **Linux Foundations**: Emphasize how Linux is the bedrock throughout—from the local shell environment to the base OS of our containers in the cloud.
*   **Local Development Loop**:
    *   Running raw components locally on the host machine using standard tools.
    *   Backend testing via `uvicorn main:app --reload`.
    *   Frontend testing via a simple HTTP server (e.g., `python -m http.server`).
*   **Git Flow**:
    *   How we commit incremental changes.
    *   Standardizing code collaboration, branching, and maintaining a clean version history before anything gets built into heavily isolated formats.

---

## 3. Dockerfile, Containers, Webservers (HTTP, Nginx)
**Goal:** Introduce containerization and deployment fundamentals.

*   **The Containerization Shift**: Moving from "it works on my machine" to "it works everywhere" by packaging code + dependencies together.
*   **The Backend Dockerfile (Multi-Stage Build)**:
    *   **Optimization**: Highlight the recent shift to a *multi-stage Docker build*. 
    *   **Stage 1** builds heavyweight dependencies in a builder image, and **Stage 2** copies only the necessary compiled files into a minimal, lightweight python-slim image to reduce surface area and improve security.
*   **Webservers & Nginx**: 
    *   Why we use Nginx instead of a basic python HTTP server for the frontend.
    *   Nginx acts as a production-grade, highly concurrent web server designed specifically to serve static assets rapidly.

---

## 4. Docker Compose for Local Multi-Container Testing
**Goal:** How we orchestrate on a single developer machine.

*   **The Problem**: Running `docker build` and `docker run` for multiple connecting services (Frontend + Backend) is tedious and error-prone.
*   **The Solution - Docker Compose**:
    *   Infrastructure-as-Code for local environments.
    *   One command (`docker-compose up`) starts the entire stack simultaneously.
*   **Key Features Demonstrated**:
    *   **Port Mapping**: Routing isolated container ports (like 80) to the host (like 3000).
    *   **Networking**: Containers communicating automatically across the internal Docker bridge network without exposing databases/internal APIs to the world.
    *   **Volume Mounts**: Mapping local directories into the containers to allow hot-reloading code changes *without* needing to rebuild the Docker images every time.

---

## 5. Kubernetes & Helm
**Goal:** The final step to production scalability, high availability, and infrastructure management.

*   **Kubernetes Core Concepts**:
    *   **Deployments**: How we manage stateless applications (like our FastAPI backend and Nginx frontend). Deployments ensure our desired number of replica pods are constantly running and handle zero-downtime rolling updates.
    *   **StatefulSets**: Used for stateful applications (like a production database). Unlike Deployments, they provide stable, persistent network identities and storage for each pod.
*   **Networking & Services**:
    *   **ClusterIP**: The default, internal-only networking. Useful for allowing the frontend to securely talk to the backend within the cluster without exposing the backend to the public internet.
    *   **NodePort**: Exposes the service on a static port on each Node's IP. Often used for external access or local cluster testing.
*   **Reliability & Configuration**:
    *   **Health Probes (Liveness & Readiness)**: How Kubernetes knows if a pod is healthy. If our backend deadlocks, the Liveness probe fails and Kubernetes automatically restarts the pod. Readiness probes ensure no traffic is sent to a pod until the app is fully booted up.
    *   **Environment Variables & ConfigMaps**: Decoupling configuration from our container images. We inject variables (like `DATABASE_URL` or API keys) dynamically per environment without rebuilding the source code.
*   **Advanced Scheduling & Infrastructure**:
    *   **Node Selectors & Affinities**: Controlling *where* pods run. We can force backend pods to run on nodes with specific hardware (e.g., SSDs or specific instances) or ensure pods are spread across different availability zones (anti-affinity) for high availability.
    *   **Node Maintenance**: How Kubernetes handles infrastructure updates. We can gracefully **"drain"** a node—which safely moves all its running pods to other nodes in the cluster—so we can perform OS updates on the underlying machines without taking down the application.
*   **Helm (The Package Manager)**:
    *   Managing dozens of raw K8s YAML files gets messy fast. Helm packages them into a single logical unit.
    *   **Templating**: Reusing standard structural templates and injecting dynamic configurations (like replica counts or target ports).
    *   **Environment Parity**: Using the *exact same* Helm chart for Dev, Staging, and Production, just swapping out different `values.yaml` files.
    *   **Releases & Rollbacks**: Deploying complex architecture with a single `helm install` command, and supporting easy `helm rollback` if a bad deployment goes through.
