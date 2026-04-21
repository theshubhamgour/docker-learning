# 🚀 Docker Compose Tutorial

This repository teaches Docker Compose step-by-step using real-world examples.

---

## 📌 What You Will Learn

- Running containers using Docker
- Converting commands into Docker Compose
- Multi-container applications
- Networking in Docker Compose
- Volumes (data persistence)
- Environment variables
- Building custom apps using Dockerfile
- Health checks & dependencies

---

# 🧠 1. Single Container (Nginx)

## Manual Command
```bash
docker run -d -p 8080:80 nginx
```

## Docker Compose
```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

---

# 🧠 2. Multi-Container + Networking

## Manual Commands
```bash
docker network create mynet

docker run -d --name backend --network mynet hashicorp/http-echo -text="Hello from Backend"

docker run -d --name frontend --network mynet -p 8081:80 nginx
```

## Docker Compose
```yaml
services:
  backend:
    image: hashicorp/http-echo
    command: ["-text=Hello from Backend"]

  frontend:
    image: nginx
    ports:
      - "8081:80"
```

---

# 🧠 3. Volumes (MySQL)

## Manual Command
```bash
docker run -d \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=root \
  -v mysql-data:/var/lib/mysql \
  mysql
```

## Docker Compose
```yaml
services:
  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - mysql-data:/var/lib/mysql
    ports:
      - "3306:3306"

volumes:
  mysql-data:
```

---

# 🧠 4. Build + Environment Variables

## Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install flask

ENV ENV=prod

CMD ["python", "app.py"]
```

## Sample app.py
```python
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return f"Environment: {os.getenv('ENV')}"

app.run(host="0.0.0.0", port=5000)
```

## Manual Commands
```bash
docker build -t myapp .
docker run -d -p 5000:5000 -e ENV=prod myapp
```

## Docker Compose
```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      ENV: prod
```

---

# 🧠 5. Full Production Setup

## Docker Compose
```yaml
services:
  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 5

  backend:
    build: ./backend
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db

  frontend:
    image: nginx
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  mysql-data:
```

---

# ▶️ Run Everything

```bash
docker compose up -d
```

---

# 🎯 Key Takeaways

- Docker Compose simplifies multi-container apps
- One YAML file replaces multiple commands
- Built-in networking between services
- Volumes ensure data persistence
- Environment variables manage configs
- Health checks improve reliability

---


Happy Learning 🚀
