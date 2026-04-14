# Dockerfile Masterclass - Complete Guide

A Dockerfile is a text file containing a series of instructions to build a Docker image. This guide explains all the major Dockerfile commands with examples and best practices.

---

## Table of Contents
1. [FROM](#from)
2. [RUN](#run)
3. [WORKDIR](#workdir)
4. [COPY](#copy)
5. [ADD](#add)
6. [USER](#user)
7. [ENV](#env)
8. [EXPOSE](#expose)
9. [LABEL](#label)
10. [CMD](#cmd)
11. [ENTRYPOINT](#entrypoint)
12. [VOLUME](#volume)
13. [ARG](#arg)
14. [HEALTHCHECK](#healthcheck)
15. [ONBUILD](#onbuild)
16. [Complete Example](#complete-example)
17. [Dockerfile Cheatsheet](#dockerfile-cheatsheet)

---

## FROM

**Purpose**: Specifies the base image for the Docker image. Must be the first instruction in a Dockerfile (except for ARG).

**Syntax**:
```dockerfile
FROM <image>:<tag>
FROM <image>@<digest>
```

**Examples**:
```dockerfile
# Using Ubuntu as base image
FROM ubuntu:22.04

# Using official Python image
FROM python:3.11-slim

# Using Alpine Linux (lightweight)
FROM alpine:latest

# Using Node.js image
FROM node:18-alpine

# Using specific digest for reproducibility
FROM ubuntu@sha256:6042500cf4b44c2e9c2cc1ef48b4dafb239e20322678e6bd35a337504e5f35d
```

**Best Practices**:
- Use specific version tags instead of `latest` for reproducibility
- Alpine images are smaller and faster to download
- Always specify a tag; if omitted, defaults to `latest`

---

## RUN

**Purpose**: Executes commands during image build. Used to install packages, create directories, or run any shell command.

**Syntax**:
```dockerfile
RUN <command>                    # Shell form
RUN ["executable", "param1", "param2"]  # Exec form
```

**Examples**:
```dockerfile
# Shell form - runs in /bin/sh -c
RUN apt-get update && apt-get install -y curl git

# Exec form - runs directly without shell
RUN ["apt-get", "install", "-y", "curl"]

# Multiple commands can be chained
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installing pip packages
RUN pip install --no-cache-dir django flask

# Creating directories
RUN mkdir -p /app/logs

# Setting up files
RUN useradd -m appuser
```

**Best Practices**:
- Chain multiple commands with `&&` to reduce layers
- Use `&&` to ensure previous command succeeded before next one
- Clean up package manager caches to reduce image size
- Each RUN creates a new layer; minimize them for efficiency

---

## WORKDIR

**Purpose**: Sets the working directory for all subsequent instructions (RUN, COPY, CMD, ENTRYPOINT, etc.). If the directory doesn't exist, it will be created.

**Syntax**:
```dockerfile
WORKDIR <path>
```

**Examples**:
```dockerfile
# Set working directory
WORKDIR /app

# Multiple WORKDIR commands - they are concatenated
WORKDIR /home
WORKDIR app
# Results in /home/app

# Using WORKDIR multiple times for different contexts
FROM node:18
WORKDIR /app
COPY package.json .
WORKDIR /app/src
COPY . .
```

**Best Practices**:
- Always set WORKDIR to a known directory
- Use absolute paths
- Avoids scattered files across the container filesystem

---

## COPY

**Purpose**: Copies files and directories from the host machine into the Docker image. Only copies from build context (cannot use URLs).

**Syntax**:
```dockerfile
COPY <src> <dest>
COPY ["<src>", "<dest>"]  # For paths with spaces
```

**Examples**:
```dockerfile
# Copy single file
COPY package.json /app/

# Copy entire directory
COPY src/ /app/src/

# Copy with pattern matching
COPY *.txt /app/

# Copy multiple files
COPY file1.js file2.js /app/

# Array syntax for paths with spaces
COPY ["my file.txt", "/app/my file.txt"]

# Copy with specific ownership
COPY --chown=user:group package.json /app/

# Full example with multiple COPY commands
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
```

**Best Practices**:
- Use specific paths rather than copying entire directory if possible
- Copy dependency files first (package.json, requirements.txt) for better layer caching
- Use `.dockerignore` to exclude unnecessary files
- Use `--chown` to set correct ownership

---

## ADD

**Purpose**: Similar to COPY but with additional features: can extract tar files and copy from URLs. Generally, COPY is preferred for clarity.

**Syntax**:
```dockerfile
ADD <src> <dest>
ADD ["<src>", "<dest>"]  # For paths with spaces
```

**Examples**:
```dockerfile
# Copy file (same as COPY)
ADD script.sh /app/

# Extract tar file automatically
ADD app.tar.gz /app/

# Copy from URL
ADD https://github.com/example/archive.tar.gz /tmp/

# Extract and place in specific directory
ADD https://golang.org/dl/go1.20.linux-amd64.tar.gz /usr/local/

# Difference between ADD and COPY
# ADD can extract archives
ADD configs.tar.gz /app/configs/

# COPY just copies files as-is
COPY configs.tar.gz /app/configs/
```

**Best Practices**:
- Prefer COPY for better clarity and predictability
- Use ADD only when you need URL download or tar extraction features
- If using ADD with URLs, consider using curl or wget in RUN instead for better control

---

## USER

**Purpose**: Sets the user context for running RUN, CMD, ENTRYPOINT, and COPY instructions. Improves security by avoiding running containers as root.

**Syntax**:
```dockerfile
USER <user>:<group>
USER <UID>:<GID>
```

**Examples**:
```dockerfile
# Using username
FROM ubuntu:22.04
RUN useradd -m appuser
USER appuser

# Using UID:GID
USER 1000:1000

# Creating user and switching
RUN useradd -m -u 1001 myapp
USER myapp

# Switching back to root for specific commands
FROM node:18
USER node
RUN npm install
USER root
RUN chown -R node:node /app
USER node

# Complete example with unprivileged user
FROM python:3.11
WORKDIR /app
RUN useradd -m appuser && chown -R appuser:appuser /app
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python", "app.py"]
```

**Best Practices**:
- Always run containers with non-root user for security
- Create the user before setting USER directive
- Use numeric UID:GID to avoid issues across different systems

---

## ENV

**Purpose**: Sets environment variables that are available during build time and at runtime in the container.

**Syntax**:
```dockerfile
ENV <key> <value>
ENV <key>=<value> <key2>=<value2>
```

**Examples**:
```dockerfile
# Single environment variable
ENV NODE_ENV production

# Multiple environment variables
ENV APP_HOME=/app \
    LOG_LEVEL=info \
    MAX_WORKERS=4

# Using environment variables in subsequent instructions
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Environment variables in configuration
ENV DATABASE_URL=postgres://localhost:5432/mydb
ENV REDIS_URL=redis://localhost:6379

# Using ARG with ENV (ARG is build-time only)
ARG VERSION=1.0
ENV APP_VERSION=$VERSION

# Application-specific example
FROM node:18
ENV NODE_ENV=production \
    NPM_CONFIG_LOGLEVEL=warn \
    PORT=3000
EXPOSE $PORT
CMD ["node", "server.js"]
```

**Best Practices**:
- Use ENV for runtime configuration
- Use ARG for build-time variables
- Document environment variables in your README
- Combine multiple ENV statements into one to reduce layers

---

## EXPOSE

**Purpose**: Documents which ports the application is listening on. Does NOT actually publish ports; it's metadata. Ports must be published using `-p` flag when running container.

**Syntax**:
```dockerfile
EXPOSE <port>
EXPOSE <port>/<protocol>
```

**Examples**:
```dockerfile
# Single port
EXPOSE 8080

# Multiple ports
EXPOSE 3000 5000 8000

# Specify protocol (TCP is default)
EXPOSE 80/tcp
EXPOSE 443/tcp

# UDP protocol
EXPOSE 53/udp

# Mixed protocols
EXPOSE 8080/tcp 8000/udp

# Web application example
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

# Database example
FROM postgres:15
EXPOSE 5432/tcp
```

**Best Practices**:
- Document all ports your app listens on
- Remember to use `-p` flag when running: `docker run -p 3000:3000 myimage`
- EXPOSE alone doesn't publish ports; it's for documentation and `-P` flag usage

---

## LABEL

**Purpose**: Adds metadata to the Docker image as key-value pairs. Useful for documentation, versioning, and automation.

**Syntax**:
```dockerfile
LABEL <key>=<value> <key2>=<value2>
LABEL <key>=<value>
```

**Examples**:
```dockerfile
# Single label
LABEL maintainer="admin@example.com"

# Multiple labels
LABEL version="1.0" \
      description="Node.js web application" \
      maintainer="team@company.com"

# Standard labels (OCI image spec)
LABEL org.opencontainers.image.title="MyApp" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.description="Production web server" \
      org.opencontainers.image.url="https://github.com/user/myapp" \
      org.opencontainers.image.vendor="MyCompany"

# Build-time labels
ARG BUILD_DATE
ARG VCS_REF
LABEL org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.revision=$VCS_REF

# Complete example
FROM ubuntu:22.04
LABEL maintainer="myteam@example.com" \
      version="2.0" \
      environment="production"
```

**Best Practices**:
- Use consistent label names (preferably OCI standards)
- Include maintainer contact and version
- Use labels for automation and organization
- View labels with: `docker inspect --format='{{json .Config.Labels}}' image_name`

---

## CMD

**Purpose**: Provides default command to run when container starts. Can be overridden by user when running the container.

**Syntax**:
```dockerfile
CMD ["executable", "param1", "param2"]     # Exec form (preferred)
CMD ["param1", "param2"]                    # Default parameters for ENTRYPOINT
CMD command param1 param2                   # Shell form
```

**Examples**:
```dockerfile
# Exec form (preferred - directly executes the binary)
CMD ["node", "server.js"]

# Shell form (runs in /bin/sh -c)
CMD npm start

# With parameters
CMD ["python", "app.py", "--debug"]

# Default parameters for ENTRYPOINT
ENTRYPOINT ["npm"]
CMD ["start"]

# Web server example
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

# Database example
FROM postgres:15
CMD ["postgres"]

# Can be overridden
# docker run myimage python3 script.py  (overrides CMD)
```

**Best Practices**:
- Use exec form for clarity and signal handling
- Only one CMD per Dockerfile; last one wins
- Use with ENTRYPOINT for flexibility
- CMD is intended to be overridden by users

---

## ENTRYPOINT

**Purpose**: Specifies the command that always runs when container starts. Unlike CMD, ENTRYPOINT is harder to override.

**Syntax**:
```dockerfile
ENTRYPOINT ["executable", "param1", "param2"]  # Exec form (preferred)
ENTRYPOINT command param1 param2               # Shell form
```

**Examples**:
```dockerfile
# Make container behave like an executable
ENTRYPOINT ["python", "app.py"]

# Accepting parameters passed to container
ENTRYPOINT ["node"]
# docker run myimage server.js  -> runs: node server.js

# Exec form is recommended
FROM python:3.11
ENTRYPOINT ["python", "-u", "app.py"]

# Combined with CMD
FROM node:18
ENTRYPOINT ["node"]
CMD ["server.js"]
# docker run myimage -> runs: node server.js
# docker run myimage app.js -> runs: node app.js

# Script as entrypoint
FROM ubuntu:22.04
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["default_arg"]

# Practical example - database backup tool
FROM postgres:15
ENTRYPOINT ["pg_dump"]
# Usage: docker run myimage -h localhost -U user mydatabase > backup.sql
```

**Best Practices**:
- Use exec form to handle signals correctly
- Combine ENTRYPOINT and CMD for flexibility
- Use shell scripts for complex startup logic
- ENTRYPOINT makes the container behave like an executable

---

## VOLUME

**Purpose**: Creates a mount point in the container. Marks directories to be stored outside the container's writable layer.

**Syntax**:
```dockerfile
VOLUME ["<path1>", "<path2>"]
VOLUME <path>
```

**Examples**:
```dockerfile
# Single volume
VOLUME /data

# Multiple volumes
VOLUME ["/var/log", "/data", "/config"]

# Database example
FROM postgres:15
VOLUME /var/lib/postgresql/data

# Application with multiple volumes
FROM ubuntu:22.04
VOLUME ["/app/uploads", "/app/logs", "/etc/config"]

# Web server with persistent data
FROM nginx:latest
VOLUME /usr/share/nginx/html
VOLUME /var/log/nginx
```

**Best Practices**:
- Use VOLUME to persist important data
- Mount volumes with `-v` flag: `docker run -v /host/path:/container/path image`
- Anonymous volumes are created for each VOLUME instruction
- Volumes persist even after container is deleted

---

## ARG

**Purpose**: Defines build-time variables that can be passed during image build. Not available at runtime.

**Syntax**:
```dockerfile
ARG <name>
ARG <name>=<default-value>
```

**Examples**:
```dockerfile
# Define without default value
ARG BUILD_DATE

# Define with default value
ARG VERSION=1.0.0

# Using ARG in build context
ARG APP_HOME=/app
WORKDIR $APP_HOME

# Multiple ARGs
ARG NODE_VERSION=18
ARG APP_ENV=production

FROM node:${NODE_VERSION}
ARG APP_ENV
ENV NODE_ENV=$APP_ENV

# Build-time arguments example
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential

# Using during build
# docker build --build-arg VERSION=2.0 .
# docker build --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') .

# Extended example with multiple args
FROM node:18
ARG NODE_ENV=production
ARG BUILD_DATE
ARG APP_VERSION=1.0

ENV NODE_ENV=$NODE_ENV
LABEL build.date=$BUILD_DATE app.version=$APP_VERSION
```

**Best Practices**:
- ARG is only available during build; not in running container
- Use for build-time configuration
- Can be overridden: `docker build --build-arg NAME=value .`
- Use ENV to make variables available at runtime

---

## HEALTHCHECK

**Purpose**: Tells Docker how to test if a container is still working. Periodically runs a command to check health.

**Syntax**:
```dockerfile
HEALTHCHECK [OPTIONS] CMD <command>
HEALTHCHECK NONE
```

**Examples**:
```dockerfile
# Basic healthcheck
HEALTHCHECK CMD curl -f http://localhost/ || exit 1

# With options
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Web application example
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1
CMD ["npm", "start"]

# Docker-compose with database
FROM mysql:8.0
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD mysqladmin ping -h 127.0.0.1 -u root -p$MYSQL_ROOT_PASSWORD

# Custom healthcheck script
FROM ubuntu:22.04
COPY healthcheck.sh /
RUN chmod +x /healthcheck.sh
HEALTHCHECK --interval=30s CMD /healthcheck.sh

# Disable healthcheck
HEALTHCHECK NONE
```

**Options**:
- `--interval=DURATION` (default: 30s): How often to check
- `--timeout=DURATION` (default: 30s): How long to wait for check
- `--start-period=DURATION` (default: 0s): Grace period before starting checks
- `--retries=N` (default: 3): Consecutive failures before unhealthy

**Best Practices**:
- Include specific endpoint or command to check
- Use appropriate intervals for your application
- Set start-period for applications that need time to start
- Exit code 0 = healthy, non-zero = unhealthy

---

## ONBUILD

**Purpose**: Registers a trigger instruction to run when this image is used as a base image for another Dockerfile.

**Syntax**:
```dockerfile
ONBUILD <INSTRUCTION>
```

**Examples**:
```dockerfile
# Base image with ONBUILD
FROM ubuntu:22.04
ONBUILD RUN apt-get update && apt-get install -y curl
ONBUILD WORKDIR /app
ONBUILD COPY . .

# When this is used as base in another Dockerfile:
# - The ONBUILD instructions execute after FROM
# - Useful for creating reusable base images

# Example: Node base image for applications
FROM node:18
ONBUILD WORKDIR /app
ONBUILD COPY package*.json ./
ONBUILD RUN npm install
ONBUILD COPY . .
EXPOSE 3000
ONBUILD CMD ["npm", "start"]

# Usage:
# FROM mybase:latest  (triggers all ONBUILD instructions)

# Python example
FROM python:3.11
ONBUILD RUN mkdir -p /app
ONBUILD WORKDIR /app
ONBUILD COPY requirements.txt .
ONBUILD RUN pip install -r requirements.txt
ONBUILD COPY . .
```

**Best Practices**:
- Use for creating reusable base images
- Document ONBUILD instructions clearly
- Can make debugging harder; use sparingly
- ONBUILD doesn't execute on the base image itself

---

## Complete Example

Here's a complete Dockerfile demonstrating best practices with multiple commands:

```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder

# Set metadata
LABEL maintainer="team@example.com" \
      version="1.0.0" \
      description="Production Node.js application"

# Build arguments
ARG BUILD_DATE
ARG VCS_REF

# Set environment variables
ENV NODE_ENV=production \
    NPM_CONFIG_LOGLEVEL=warn

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy application code
COPY . .

# Production stage
FROM node:18-alpine

# Set environment
ENV NODE_ENV=production \
    PORT=3000

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy from builder
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./
COPY --chown=nodejs:nodejs . .

# Create volumes for logs
VOLUME ["/app/logs"]

# Expose port
EXPOSE 3000

# Switch to non-root user
USER nodejs

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD node healthcheck.js || exit 1

# Default command
CMD ["node", "server.js"]
```

---

## Dockerfile Cheatsheet

### Image Building Instructions

| Command | Purpose | Format |
|---------|---------|--------|
| `FROM` | Base image | `FROM image:tag` |
| `RUN` | Execute command during build | `RUN command` |
| `COPY` | Copy files from host | `COPY src dest` |
| `ADD` | Copy files (with tar/URL support) | `ADD src dest` |
| `WORKDIR` | Set working directory | `WORKDIR path` |
| `ENV` | Set environment variables | `ENV KEY=value` |
| `ARG` | Build-time arguments | `ARG KEY=default` |
| `LABEL` | Add metadata | `LABEL key=value` |

### Runtime & Port Instructions

| Command | Purpose | Format |
|---------|---------|--------|
| `EXPOSE` | Document ports | `EXPOSE port` |
| `CMD` | Default command | `CMD ["cmd", "arg"]` |
| `ENTRYPOINT` | Configure container as executable | `ENTRYPOINT ["cmd"]` |
| `USER` | Set user context | `USER username` |
| `VOLUME` | Create mount point | `VOLUME /path` |

### Health & Advanced

| Command | Purpose | Format |
|---------|---------|--------|
| `HEALTHCHECK` | Health check command | `HEALTHCHECK CMD cmd` |
| `ONBUILD` | Trigger on child images | `ONBUILD INSTRUCTION` |

### Quick Reference by Task

#### Installing Packages
```dockerfile
RUN apt-get update && apt-get install -y package-name && rm -rf /var/lib/apt/lists/*
RUN apk add --no-cache package-name  # Alpine Linux
RUN yum install -y package-name && yum clean all  # CentOS/RHEL
```

#### Creating Users
```dockerfile
RUN useradd -m -u 1001 myuser
USER myuser
```

#### Setting Up Python
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

#### Setting Up Node.js
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

#### Multi-stage Build
```dockerfile
FROM golang:1.20 AS builder
WORKDIR /src
COPY . .
RUN go build -o app .

FROM alpine:latest
COPY --from=builder /src/app /app
CMD ["/app"]
```

#### Environment Configuration
```dockerfile
ENV APP_HOME=/app \
    LOG_LEVEL=info \
    NODE_ENV=production
ARG BUILD_DATE
RUN echo "Built on $BUILD_DATE"
```

### Best Practice Checklist

- [ ] Use specific base image tags (avoid `latest`)
- [ ] Combine RUN commands with `&&` to reduce layers
- [ ] Remove package manager caches to reduce image size
- [ ] Use WORKDIR instead of `cd` commands
- [ ] Copy files in correct order (dependencies first for better caching)
- [ ] Run containers as non-root user
- [ ] Use `.dockerignore` file
- [ ] Use exec form for CMD/ENTRYPOINT instead of shell form
- [ ] Add HEALTHCHECK for critical services
- [ ] Use LABEL for metadata and versioning
- [ ] Minimize the number of layers
- [ ] Use multi-stage builds for smaller final images

### Common Patterns

**Web Application Pattern:**
```dockerfile
FROM <language>:version
WORKDIR /app
COPY package.json .
RUN <install dependencies>
COPY . .
EXPOSE <port>
HEALTHCHECK --interval=30s CMD <health-check>
CMD ["<run-command>"]
```

**Microservice Pattern:**
```dockerfile
FROM <base>
RUN <system-packages>
RUN <create-user>
WORKDIR /app
COPY . .
RUN <install-dependencies>
USER <non-root>
EXPOSE <port>
HEALTHCHECK CMD <check>
ENTRYPOINT ["<service>"]
```

**Build Tool Pattern:**
```dockerfile
FROM <base> AS builder
WORKDIR /src
COPY . .
RUN <build-commands>

FROM <base>
COPY --from=builder <source> <dest>
CMD ["<run-command>"]
```

---

## Additional Resources

- [Official Docker Documentation](https://docs.docker.com/engine/reference/builder/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [OCI Image Spec](https://github.com/opencontainers/image-spec)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

---

**Last Updated**: April 2026
**Version**: 1.0