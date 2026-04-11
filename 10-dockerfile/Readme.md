# Dockerfile Guide & Demos

> “Docker run is temporary… Dockerfile is permanent.”

**Quick Comparison:**

| `docker run` | `Dockerfile` |
| :--- | :--- |
| One command | Step-by-step process |
| Hard to repeat | Easy to version control |
| Manual | Automated |
| 🍜 Cooking instantly | 📖 A recipe |

---

## Part 1: Beginner Demo (No Code Needed)

If you don’t have any app code, you can still demonstrate `Dockerfile` vs `docker run` easily.

### 🚀 Example 1: Run NGINX

**🔹 Docker Run (The Quick Way)**
```bash
docker run -d -p 8080:80 nginx
```
👉 Open browser → `localhost:8080` (You’ll see the default NGINX page).

**🔹 Equivalent Dockerfile (The Structured Way)**
```dockerfile
FROM nginx:latest
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**🧠 Explain simply:**
* `FROM nginx:latest` → Ready-made web server
* `EXPOSE 80` → App runs on port 80
* `CMD` → Start nginx

**🔹 Build & Run**
```bash
docker build -t my-nginx .
docker run -d -p 8080:80 my-nginx
```

---

### 🚀 Example 2: Create Your Own HTML (No coding skills needed)

**🔹 Step 1: Create a simple file**
```bash
echo "<h1>Hello from Docker 🚀</h1>" > index.html
```

**🔹 Docker Run (The Temporary Way)**
```bash
docker run -d -p 8080:80 -v $(pwd):/usr/share/nginx/html nginx
```
**🧠 Explain:**
* `-v $(pwd):/usr/share/nginx/html` → Mounts your local folder into the container. Your HTML replaces the default page.

**🔹 Dockerfile (The Proper Way)**
```dockerfile
FROM nginx:latest

RUN rm -rf /usr/share/nginx/html/*

COPY index.html /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**🔹 Build & Run**
```bash
docker build -t my-html-site .
docker run -d -p 8080:80 my-html-site
```

---
## Common Dockerfile Instructions Explained

Here are the most frequently used instructions when writing a Dockerfile:

* **`FROM`**: Defines the base image for your container. It is always the starting point of any Dockerfile (e.g., `FROM node:18-alpine`, `FROM ubuntu:latest`). Think of it as the foundation of your building.
* **`WORKDIR`**: Sets the working directory inside the container for any subsequent `RUN`, `CMD`, `COPY`, or `ADD` instructions. It is exactly like running the `cd` command in a terminal. (e.g., `WORKDIR /app`)
* **`COPY`**: Copies files and directories from your local computer into the container's filesystem. (e.g., `COPY package.json .` or `COPY index.html /usr/share/nginx/html`).
* **`RUN`**: Executes commands inside the container *during the build process*. This is typically used to install dependencies or set up environments. (e.g., `RUN npm install` or `RUN apt-get update`).
