# Docker `version` and `info` Commands -- Explained

This document explains two important Docker commands used by DevOps
engineers:

-   `docker version`
-   `docker info`

These commands help inspect and troubleshoot Docker environments.

------------------------------------------------------------------------

# Example: `docker version` Output

Example command run on a Linux server:

``` bash
ubuntu@ip-172-31-6-26:~$ docker version
Client: Docker Engine - Community
 Version:           29.2.1
 API version:       1.53
 Go version:        go1.25.6
 Git commit:        a5c7197
 Built:             Mon Feb  2 17:17:26 2026
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          29.2.1
  API version:      1.53 (minimum version 1.44)
  Go version:       go1.25.6
  Git commit:       6bc6209
  Built:            Mon Feb  2 17:17:26 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v2.2.1
  GitCommit:        dea7da592f5d1d2b7755e3a161be07f43fad8f75
 runc:
  Version:          1.3.4
  GitCommit:        v1.3.4-0-gd6d73eb8
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

------------------------------------------------------------------------

# Line-by-Line Explanation

## Client Section

**Client: Docker Engine - Community**\
This indicates the Docker CLI version installed on the system.

**Version: 29.2.1**\
The installed Docker client version.

**API version: 1.53**\
Version of the Docker API used by the client to communicate with the
Docker daemon.

**Go version: go1.25.6**\
Docker is written in Go. This shows the Go language version used to
compile Docker.

**Git commit: a5c7197**\
The source code commit used to build this Docker release.

**Built: Mon Feb 2 17:17:26 2026**\
Date and time when this Docker binary was built.

**OS/Arch: linux/amd64**\
Operating system and CPU architecture.

**Context: default**\
Docker context currently being used. Context defines which Docker
environment the CLI connects to.

------------------------------------------------------------------------

# Server Section

This part shows information about the Docker daemon running on the
machine.

**Server: Docker Engine - Community**\
The Docker daemon running on the system.

### Engine Details

**Version: 29.2.1**\
Version of Docker Engine installed on the server.

**API version: 1.53 (minimum version 1.44)**\
Server API version and the minimum supported client version.

**Go version: go1.25.6**\
Go version used to compile the Docker engine.

**Git commit: 6bc6209**\
Source commit used to build the Docker server.

**Built: Mon Feb 2 17:17:26 2026**\
Build date of the Docker daemon.

**OS/Arch: linux/amd64**\
Operating system and architecture where Docker daemon is running.

**Experimental: false**\
Shows whether experimental Docker features are enabled.

------------------------------------------------------------------------

# Runtime Components

Docker internally uses several runtime tools.

### containerd

**Version: v2.2.1**\
containerd is responsible for managing container lifecycle.

**GitCommit**\
Exact build commit for containerd.

### runc

**Version: 1.3.4**\
runc is the low‑level container runtime used to start containers.

### docker-init

**Version: 0.19.0**\
Small init system used inside containers to properly manage processes.

------------------------------------------------------------------------

# Example: `docker info` Output

Example:

``` bash
ubuntu@ip-172-31-6-26:~$ docker info
Client: Docker Engine - Community
 Version:    29.2.1
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.31.1
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v5.1.0
    Path:     /usr/libexec/docker/cli-plugins/docker-compose
```

------------------------------------------------------------------------

# Client Info Explanation

**Version: 29.2.1**\
Docker CLI version.

**Context: default**\
The Docker environment the CLI is connected to.

**Debug Mode: false**\
Debug logging is disabled.

### Plugins

Docker CLI supports plugins.

**buildx**\
Advanced Docker build tool used for multi-platform builds.

**compose**\
Used to run multi-container applications using `docker compose`.

------------------------------------------------------------------------

# Server Section of `docker info`

    Containers: 5
     Running: 0
     Paused: 0
     Stopped: 5

**Containers**\
Total containers on the system.

**Running**\
Currently active containers.

**Paused**\
Containers paused using `docker pause`.

**Stopped**\
Containers that exist but are not running.

------------------------------------------------------------------------

    Images: 3

**Images**\
Number of Docker images stored locally.

------------------------------------------------------------------------

    Server Version: 29.2.1

Docker engine version installed on the server.

------------------------------------------------------------------------

# Storage Driver

    Storage Driver: overlayfs
    driver-type: io.containerd.snapshotter.v1

Storage drivers manage container image layers.

`overlayfs` is the most common driver used on modern Linux systems.

------------------------------------------------------------------------

# Logging Driver

    Logging Driver: json-file

Specifies how container logs are stored.

Default format: JSON files.

Logs can be viewed with:

``` bash
docker logs container_name
```

------------------------------------------------------------------------

# Cgroup Configuration

    Cgroup Driver: systemd
    Cgroup Version: 2

Controls how system resources like CPU and memory are managed for
containers.

------------------------------------------------------------------------

# Networking and Volume Plugins

    Volume: local
    Network: bridge host ipvlan macvlan null overlay

These are networking and volume drivers available in Docker.

------------------------------------------------------------------------

# System Information

    Kernel Version: 6.17.0-1007-aws
    Operating System: Ubuntu 24.04.3 LTS
    OSType: linux
    Architecture: x86_64

Shows the host system where Docker is running.

------------------------------------------------------------------------

# Hardware Resources

    CPUs: 2
    Total Memory: 911.5MiB

System resources available for running containers.

------------------------------------------------------------------------

# Docker Host Details

    Name: ip-172-31-6-26
    ID: c599fd1d-48d9-45e4-8f51-03814f8f39a5

Unique identifier and hostname of the Docker host.

------------------------------------------------------------------------

# Docker Storage Location

    Docker Root Dir: /var/lib/docker

Main directory where Docker stores:

-   images
-   containers
-   volumes
-   networks

------------------------------------------------------------------------

# Security and Network Settings

    Security Options:
     apparmor
     seccomp
     Profile: builtin
     cgroupns

Security features used by Docker containers.

------------------------------------------------------------------------

# Registry Configuration

    Insecure Registries:
     ::1/128
     127.0.0.0/8

Registries that allow HTTP connections without TLS.

------------------------------------------------------------------------

# Firewall Backend

    Firewall Backend: iptables

Linux firewall system used by Docker networking.

------------------------------------------------------------------------

# Summary

  Command          Purpose
  ---------------- ------------------------------------------
  docker version   Shows Docker client and server versions
  docker info      Displays full Docker environment details

These commands are extremely useful for:

-   DevOps troubleshooting
-   CI/CD debugging
-   Production server inspection
