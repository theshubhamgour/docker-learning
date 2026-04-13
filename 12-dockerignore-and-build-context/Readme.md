# Docker .dockerignore and Build Context

## Overview

When building Docker images, understanding the **build context** and using **.dockerignore** files are crucial for efficient, secure, and clean image builds.

## Docker Build Context

The build context is the set of files that Docker sends to the Docker daemon for building an image. It's everything in the directory where you run the `docker build` command.

### How Build Context Works

```bash
docker build -t myapp .
```

The `.` at the end specifies the current directory as the build context. Docker will:

1. Package all files in the current directory (and subdirectories)
2. Send them to the Docker daemon
3. Use the Dockerfile to build the image

### Build Context Size Matters

- **Large contexts** = slower builds and more network traffic
- **Unnecessary files** in context can bloat your image
- **Sensitive files** might be accidentally included

## .dockerignore File

The `.dockerignore` file works like `.gitignore` but for Docker builds. It tells Docker which files and directories to **exclude** from the build context.

### Creating a .dockerignore File

Create a file named `.dockerignore` in the same directory as your Dockerfile:

```bash
# .dockerignore
node_modules
*.log
.git
.env
README.md
```

### .dockerignore Syntax

The `.dockerignore` file supports:

- **Exact matches**: `node_modules`
- **Wildcards**: `*.log`, `temp*`
- **Directory patterns**: `logs/`
- **Comments**: Lines starting with `#`
- **Negation**: `!important.txt` (include despite other rules)

### Common .dockerignore Patterns

```bash
# Dependencies
node_modules/
__pycache__/
*.pyc
.pytest_cache/

# Version control
.git/
.gitignore

# Documentation
README.md
docs/

# Environment files
.env
.env.local

# Logs
*.log
logs/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Build artifacts
dist/
build/
target/

# Temporary files
tmp/
temp/
```

## Best Practices

### 1. Always Use .dockerignore

```bash
# Good practice
echo "node_modules" > .dockerignore
docker build -t myapp .
```

### 2. Minimize Build Context

Only include files needed for building your application:

```dockerfile
# Copy only necessary files
COPY package.json package-lock.json ./
RUN npm ci --only=production
COPY src/ ./src/
```

### 3. Use Multi-Stage Builds

For languages with large build dependencies:

```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

### 4. Exclude Sensitive Files

Never include:
- API keys
- Passwords
- Private keys
- Database credentials

### 5. Test Your Build Context

Check what's being sent to Docker:

```bash
# See build context size
docker build --no-cache -t test .

# Or use buildkit for progress
DOCKER_BUILDKIT=1 docker build -t myapp .
```

## Examples

### Node.js Application

```bash
# .dockerignore
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity

# Build output
dist/
build/

# Environment
.env
.env.local
```

```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Python Application

```bash
# .dockerignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
```

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

## Troubleshooting

### Build Context Too Large

**Problem**: `docker build` takes too long or fails with "context too large"

**Solution**:
1. Check `.dockerignore` is working: `docker build --no-cache -t test .`
2. Verify excluded files: `ls -la` in build directory
3. Use smaller base images

### Files Not Excluded

**Problem**: Files in `.dockerignore` still appear in build context

**Solution**:
1. Check file syntax (no spaces around `=`)
2. Ensure `.dockerignore` is in the build context root
3. Use absolute paths if needed

### Case Sensitivity

`.dockerignore` patterns are case-sensitive on Linux but case-insensitive on Windows/Mac.

## Summary

- **Build context** = files sent to Docker daemon
- **.dockerignore** = excludes unnecessary files
- **Benefits**: faster builds, smaller images, better security
- **Best practice**: always create a `.dockerignore` file

Remember: A clean build context leads to efficient, secure Docker images!
