# Docker None Network

## Overview

The `none` network in Docker is a special network driver that completely isolates containers from any network connectivity. When a container is attached to the `none` network, it has no external network interfaces except for the loopback interface (localhost). This means the container cannot communicate with other containers, the host, or the internet.

## Use Cases

- **Security**: Running untrusted code or applications that should not have network access
- **Offline processing**: Tasks that don't require network connectivity
- **Testing**: Isolating components for testing purposes
- **Compliance**: Meeting security requirements that prohibit network access

## Demonstration

Let's demonstrate the `none` network by running an Alpine Linux container with no network access.

### Command

```bash
docker run -itd --network=none -v ${PWD}:/files alpine
```

### Explanation of Flags

- `-i`: Keep STDIN open even if not attached
- `-t`: Allocate a pseudo-TTY
- `-d`: Run container in background (detached mode)
- `--network=none`: Attach container to the none network (no network connectivity)
- `-v ${PWD}:/files`: Mount the current directory to `/files` inside the container
- `alpine`: Use the Alpine Linux image

### Steps to Run

1. Open a terminal in the current directory
2. Run the command above
3. Note the container ID that is returned

### Verification

Let's verify that the container has no network connectivity:

1. **Check container networks**:
   ```bash
   docker inspect <container_id> | grep -A 10 "Networks"
   ```
   You should see that the container is attached to the "none" network.

2. **Attach to the container**:
   ```bash
   docker attach <container_id>
   ```

3. **Test network isolation**:
   Inside the container, try these commands:
   ```bash
   # Check network interfaces
   ip addr show

   # Try to ping localhost (should work)
   ping -c 1 127.0.0.1

   # Try to ping external host (should fail)
   ping -c 1 google.com

   # Check if we can access files
   ls /files
   ```

   Expected results:
   - `ip addr show` will show only the loopback interface (lo)
   - `ping 127.0.0.1` should succeed
   - `ping google.com` should fail with "Network is unreachable"
   - `ls /files` should list the contents of your current directory

### Cleanup

To stop and remove the container:

```bash
docker stop <container_id>
docker rm <container_id>
```

## Key Points

- Containers on the `none` network have no IP address assigned
- No communication is possible with other containers or the host
- The loopback interface (127.0.0.1) still works for local communication
- Volume mounts still work, allowing file access
- This is the most isolated network mode in Docker