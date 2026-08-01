# Simple FastAPI Demo with Docker Compose + CI/CD

## Project structure
```
fastapi-docker-demo/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI app
├── tests/
│   └── test_main.py         # Pytest tests
├── .github/workflows/
│   └── ci-cd.yml            # GitHub Actions pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── .dockerignore
```

## Run locally without Docker
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```
Visit http://localhost:8000/docs for the interactive Swagger UI.

## Run with Docker Compose
```bash
docker compose up --build
```
Then open http://localhost:8000/docs

Stop it with:
```bash
docker compose down
```

## Run tests
```bash
pytest -v
```

---

## How the CI/CD pipeline works (`.github/workflows/ci-cd.yml`)

The pipeline has three jobs that run in sequence:

1. **test** — runs on every push and pull request to `main`.
   - Checks out the code, sets up Python, installs dependencies, runs `pytest`.
   - If tests fail, the pipeline stops here — nothing gets built or deployed.

2. **build-and-push** — runs only on pushes to `main` (not PRs), and only if `test` passed.
   - Logs into GitHub Container Registry (GHCR) using the automatically provided `GITHUB_TOKEN` — no extra secret needed.
   - Builds the Docker image from the `Dockerfile` and pushes it tagged both `:latest` and `:<git-sha>` (so you can always trace an image back to the exact commit).

3. **deploy** — runs only after the image is pushed successfully.
   - SSHes into your server (or VM) and re-pulls/restarts the containers with `docker compose`.
   - This step needs three GitHub Actions **secrets** configured in your repo (Settings → Secrets and variables → Actions):
     - `DEPLOY_HOST` — server IP or hostname
     - `DEPLOY_USER` — SSH username
     - `DEPLOY_SSH_KEY` — private SSH key with access to that server

### Setting it up on your own repo
1. Push this project to a GitHub repository.
2. If you want automatic deployment, add the three secrets above. If not, just delete the `deploy` job — you'll still get automated testing and image publishing.
3. On your server, create `/opt/fastapi-docker-demo/docker-compose.yml` pointing at the `ghcr.io/<you>/<repo>:latest` image instead of building locally, e.g.:
   ```yaml
   services:
     api:
       image: ghcr.io/<you>/<repo>:latest
       ports:
         - "8000:8000"
       restart: unless-stopped
   ```
4. Make sure the server can pull from GHCR (`docker login ghcr.io` once with a personal access token if the package is private).
5. Push to `main` — the pipeline will test → build → deploy automatically.

### Alternatives worth knowing
- **Docker Hub** instead of GHCR: swap the `docker/login-action` registry/credentials and change the image tag prefix to `docker.io/<username>/...`.
- **Other CI systems**: the same three-stage idea (test → build/push image → deploy) maps directly onto GitLab CI (`.gitlab-ci.yml`), Jenkins, or CircleCI — only the YAML syntax changes.
- **Kubernetes deploy** instead of SSH+compose: replace the `deploy` job with a step that runs `kubectl set image ...` or applies a Helm chart, using a `KUBE_CONFIG` secret.
