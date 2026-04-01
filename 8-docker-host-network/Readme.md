
# Docker Host Network Driver

## Overview

The host network driver removes network isolation between the Docker host and the Docker container. When you use the host network mode, the container shares the host's network namespace and does not get its own IP address. The container uses the host's network interfaces directly.

### Key Characteristics
- Container shares the host's network stack
- No IP address assigned to the container
- Container can bind to any port on the host
- No network isolation between host and container
- Direct access to host's network interfaces
- Container processes are visible on the host's network

---

# Practical Demonstration

## Step 1: Run Container with Host Network

Run an Apache HTTP server container using the host network driver:

```bash
docker run -itd --name=hostapp --network=host httpd
```

## Step 2: Inspect Container Network Configuration

Check the container's network settings - notice there is no IP address assigned:

```bash
docker inspect hostapp | grep -iA 4 ipaddress
```

**Expected Output:**
```json
"IPAddress": "",
```

## Step 3: Access Container and Modify Content

Execute into the running container:

```bash
docker exec -it hostapp /bin/bash
```

Create a simple HTML page:

```bash
echo "Hi" > /usr/local/apache2/htdocs/index.html
```

Exit the container shell.

## Step 4: Test Access via Localhost

Access the web server using localhost (since it shares the host's network):

```bash
curl localhost
```

**Expected Output:**
```
Hi
```

## Step 5: Test Access via Public IP

Open a web browser and navigate to your Docker host's public IP address. You should see the same "Hi" message, confirming that the container is using the host's network interfaces directly.

---

## Key Takeaways

- **No Network Isolation**: The container shares the host's network namespace completely
- **No IP Assignment**: Containers using host network mode don't receive their own IP addresses
- **Direct Port Binding**: Applications in the container can bind directly to host ports
- **Performance**: Slightly better network performance due to no network virtualization overhead
- **Security**: Reduced network isolation may pose security risks in multi-tenant environments
- **Use Cases**: Useful for applications that need direct access to host network interfaces or when maximum network performance is required