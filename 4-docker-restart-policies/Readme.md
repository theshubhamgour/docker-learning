
# Docker Restart Policy – Default (no / none)

## Overview
Docker restart policies define how containers behave when they stop running or when the Docker service restarts.

---

# 1. Restart Policy: `no` (Default)

Here we are demonstrating the **default restart policy**, which is **`no` (none)**.

This means Docker will **not automatically restart the container** if:
- The container stops
- Docker service restarts
- The system reboots

The container will remain in the **Exited state** unless it is manually started.


### Key Behaviour
- This is the **default policy** if no restart policy is specified.
- Docker **will not restart the container automatically**.
- The container moves to **Exited state** in the following situations:
  - Docker service restart
  - System reboot
  - Manual stop
  - Application error or failure inside the container

---

# Practical Demonstration

## Step 1: Pull the Nginx Image

```bash
docker pull nginx
```

## Step 2: Verify Image

```bash
docker images
```

## Step 3: Run the Container

```bash
docker run -itd --name=demo nginx
```

## Step 4: Verify Container Status

```bash
docker ps -a
```

### Expected Output

```
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS     NAMES
e0dfc4e2ed99   nginx     "/docker-entrypoint.…"   33 seconds ago   Up 32 seconds   80/tcp    demo
```

**Status:** `Up`

---

# Validate Restart Policy

We can inspect the container configuration to check which restart policy is applied.

```bash
docker inspect demo | grep -A 4 RestartPolicy
```

OR

```bash
docker inspect demo | grep -iA 4 RestartPolicy
```

Explanation:
- `-i` → Case insensitive search
- `-A` → Show lines **after the matched result**

### Output

```
"RestartPolicy": {
    "Name": "no",
    "MaximumRetryCount": 0
},
```

This confirms that the container is using the **default restart policy (`no`)**.

---

# Restart Docker Service

Now restart the Docker service to verify container behaviour.

```bash
systemctl restart docker
```

## Check Container Status

```bash
docker ps -a
```

### Output

```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS                      PORTS     NAMES
e0dfc4e2ed99   nginx     "/docker-entrypoint.…"   3 minutes ago   Exited (0) 18 seconds ago             demo
```

**Observation:**  
After restarting the Docker service, the container moved to **Exited state**.

This proves that containers using the **default restart policy are not automatically restarted**.

---

# Start the Container Manually

```bash
docker start demo
```

Verify again:

```bash
docker ps -a
```

**Status:** `Up`

---

# Reboot the System

Now reboot the system and check the container status again.

```bash
docker ps -a
```

### Result

```
STATUS: Exited
```

**Observation:**  
After system reboot, the container remains in **Exited state**.

---

# Conclusion

The **`no` restart policy (default)** means Docker will **not attempt to restart the container automatically** under any circumstances.

Containers must be **manually started** if they stop due to:
- Docker daemon restart
- System reboot
- Manual stop
- Application failure

This policy is typically used for:
- Testing environments
- Temporary containers
- Debugging scenarios


------------------------------------------------------------------------

# 2. Restart Policy: `always`

The **Always policy** ensures that Docker will always attempt to start
the container whenever it stops, when Docker restarts, or when the host
machine reboots.

This behaviour is similar to what is commonly seen in **Kubernetes**,
where containers are automatically restarted to maintain availability.

## Key Behaviour

When a container is started with the **always restart policy**, Docker
will try to keep the container running at all times.

Behaviour of this policy:

-   The container will be **started automatically if the Docker engine
    restarts**
-   The container will be **started automatically if the host machine
    reboots**
-   Docker will **attempt to restart the container if it crashes or
    fails**
-   The restart policy is applied using the **`--restart` option**

------------------------------------------------------------------------

# Syntax

``` bash
docker run <options> --restart=always <image>:<tag>
```

Example:

``` bash
docker run -itd --name=app --restart=always httpd
```

------------------------------------------------------------------------

# Practical Demonstration

## Step 1: Pull the HTTPD Image

``` bash
docker pull httpd
```

## Step 2: Verify Images

``` bash
docker images
```

## Step 3: Run the Container with Restart Policy

``` bash
docker run -itd --name=app --restart=always httpd
```

## Step 4: Check Container Status

``` bash
docker ps -a
```

### Expected Output

    -----------(The Status is UP)-------------

This shows the container is running.

------------------------------------------------------------------------

# Validate Restart Policy

We can verify the restart policy using the **docker inspect command**.

``` bash
docker inspect app | grep -iA 3 restartpolicy
```

### Output

    "RestartPolicy": {
        "Name": "always",
        "MaximumRetryCount": 0
    },

This confirms that the container is configured with the **always restart
policy**.

------------------------------------------------------------------------

# Restart Docker Engine

Now restart the Docker service to verify behaviour.

``` bash
sudo systemctl restart docker
```

Check container status again:

``` bash
docker ps -a
```

### Result

    -----------(The Status is Still UP)-------------

    CONTAINER ID   IMAGE     COMMAND             CREATED        STATUS          PORTS     NAMES
    7aefbc85038c   httpd     "httpd-foreground"  2 minutes ago  Up 11 seconds   80/tcp    app

### Observation

Even after restarting Docker, the container **automatically starts
again**.

------------------------------------------------------------------------

# Stop the Container Manually

``` bash
docker stop app
```

Check status:

``` bash
docker ps -a
```

### Result

    -----------(The Status is Exited)-------------

Note: This exited state is **temporary during runtime**.

------------------------------------------------------------------------

# Restart Docker Again

``` bash
sudo systemctl restart docker
```

Now check the container status again:

``` bash
docker ps -a
```

### Output

    CONTAINER ID   IMAGE     COMMAND             CREATED        STATUS        PORTS     NAMES
    7aefbc85038c   httpd     "httpd-foreground"  5 minutes ago  Up 3 seconds  80/tcp    app

### Observation

The container automatically starts again even though it was stopped
earlier.

------------------------------------------------------------------------

# Reboot the Machine

Now reboot the host machine and verify the container status.

After reboot:

``` bash
docker ps -a
```

### Result

The container will be:

    UP and Running

------------------------------------------------------------------------

# Conclusion

The **`always` restart policy** ensures that Docker keeps the container
running under almost all circumstances.

Docker will automatically restart the container if:

-   Docker daemon restarts
-   The host machine reboots
-   The container crashes or fails

This policy is commonly used in **production environments** where
applications must stay available.

It is also conceptually similar to container restart behaviour seen in
**Kubernetes**.




------------------------------------------------------------------------

# 3.  Restart Policy: `unless-stopped`

## Key Behaviour

-   If the container is **running**, it will automatically start after:
    -   Docker daemon restart
    -   Host machine reboot
-   If the container is **manually stopped**, it will **remain stopped**
    even if:
    -   Docker daemon restarts
    -   The host machine reboots

This behaviour gives administrators **manual control** over containers
that should stay stopped.

------------------------------------------------------------------------

# Syntax

``` bash
docker run <options> --restart=unless-stopped <image>:<tag>
```

Example:

``` bash
docker run -itd --name=prod --restart=unless-stopped httpd
```

------------------------------------------------------------------------

# Practical Demonstration

## Step 1: Pull HTTPD Image

``` bash
docker pull httpd
```

## Step 2: Run Container with Restart Policy

``` bash
docker run -itd --name=prod --restart=unless-stopped httpd
```

------------------------------------------------------------------------

# Validate Restart Policy

Check the restart policy using:

``` bash
docker inspect prod | grep -iA 3 restartpolicy
```

### Output

    "RestartPolicy": {
        "Name": "unless-stopped",
        "MaximumRetryCount": 0
    },

This confirms that the container is running with the **unless-stopped
restart policy**.

------------------------------------------------------------------------

# Check Container Status

``` bash
docker ps -a
```

    -----------(The Status is UP)-------------

------------------------------------------------------------------------

# Restart Docker Engine

``` bash
sudo systemctl restart docker
```

Check again:

    -----------(The Status is UP)-------------

Observation:\
Since the container was running before Docker restarted, Docker
**automatically started the container again**.

------------------------------------------------------------------------

# Reboot the Machine

After rebooting the host machine:

``` bash
docker ps -a
```

    -----------(The Status is UP)-------------

Observation:\
The container starts automatically because it was previously running.

------------------------------------------------------------------------

# Important Test -- Manual Stop

Now manually stop the container.

``` bash
docker stop prod
```

Restart Docker:

``` bash
systemctl restart docker
```

Check container status:

``` bash
docker ps -a
```

### Result

    -----------(The Status is Exited)-------------

    CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS                      PORTS     NAMES
    5b35466ee2c5   httpd     "httpd-foreground"       4 minutes ago    Exited (0) 20 seconds ago             prod

------------------------------------------------------------------------

# Conclusion

The **`unless-stopped` restart policy** behaves similarly to the
**always restart policy**, with one key difference.

Docker will automatically restart the container after: - Docker daemon
restart - System reboot

**But only if the container was running before the restart.**

If the container is **manually stopped**, Docker will respect that
decision and **will not restart it automatically**.

This policy is commonly used in **production systems** where services
should stay running unless an administrator intentionally stops them.


------------------------------------------------------------------------

# Restart Policy: `on-failure`

Here we demonstrate the **`on-failure` restart policy**.

With this policy, Docker will **restart the container only if it exits
with a non‑zero exit code**, which usually indicates an **error or
failure in the application**.

If the container exits normally with exit code **0**, Docker **will not
restart it**.

## Key Behaviour

-   Docker restarts the container **only when the container exits with
    an error (non‑zero exit code)**.
-   If the container exits normally (`exit code 0`), Docker **does not
    restart it**.
-   We can also **limit the number of restart attempts**.

------------------------------------------------------------------------

# Syntax

``` bash
docker run <options> --restart=on-failure <image>:<tag>
```

Example:

``` bash
docker run -itd --name=test --restart=on-failure nginx
```

------------------------------------------------------------------------

# Practical Demonstration

## Step 1: Pull Nginx Image

``` bash
docker pull nginx
```

## Step 2: Verify Images

``` bash
docker images
```

## Step 3: Run Container with Restart Policy

``` bash
docker run -itd --name=test --restart=on-failure nginx
```

Check container:

``` bash
docker ps -a
```

------------------------------------------------------------------------

# Validate Restart Policy

``` bash
docker inspect test | grep -iA 3 restartpolicy
```

Output:

    "RestartPolicy": {
        "Name": "on-failure",
        "MaximumRetryCount": 0
    }

This means Docker will **restart the container if it fails**, with
**unlimited retry attempts**.

------------------------------------------------------------------------

# Using Retry Limit

You can specify how many times Docker should try restarting the
container.

Example:

``` bash
docker run -itd --name=tester --restart=on-failure:3 nginx
```

Verify:

``` bash
docker inspect tester | grep -iA 3 restartpolicy
```

Output:

    "RestartPolicy": {
        "Name": "on-failure",
        "MaximumRetryCount": 3
    }

Docker will attempt to restart the container **maximum 3 times** if it
fails.

------------------------------------------------------------------------

# Restart Docker Service

``` bash
systemctl restart docker
docker ps -a
```

Result:

    -----------(The Status is Exited)-------------

Observation:

`on-failure` does **not restart containers just because Docker
restarted**.

------------------------------------------------------------------------

# Simulating a Failure

Run a container that intentionally exits with an error.

``` bash
docker run --name failure-demo --restart on-failure:5 alpine sh -c "sleep 5 && exit 1"
```

Check container:

``` bash
docker ps -a
```

Example output:

    CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS                          PORTS     NAMES
    570d75815c58   alpine    "sh -c 'sleep 5 && e…"   11 seconds ago       Up Less than a second                     failure-demo

After failure:

    CONTAINER ID   IMAGE     COMMAND                  CREATED             STATUS                         PORTS     NAMES
    570d75815c58   alpine    "sh -c 'sleep 5 && e…"   47 seconds ago      Exited (1) 12 seconds ago                failure-demo

Docker will **retry restarting the container up to 5 times**.

------------------------------------------------------------------------

# Testing with Application Failure

Run another container:

``` bash
docker run -itd --name=testers --restart=on-failure:10 nginx
```

Verify policy:

``` bash
docker inspect testers | grep -iA 4 restartpolicy
```

Output:

    "RestartPolicy": {
        "Name": "on-failure",
        "MaximumRetryCount": 10
    },

Now enter the container and break the configuration:

``` bash
docker exec -it testers /bin/bash
echo "Helloworld" > /etc/nginx/nginx.conf
/sbin/nginx
```

Restart Docker:

``` bash
systemctl restart docker
```

Check status:

``` bash
docker ps -a
```

Container will fail and enter restarting state.

Example:

    CONTAINER ID   IMAGE     COMMAND                  CREATED             STATUS                         PORTS     NAMES
    f3a5b70db96b   nginx     "/docker-entrypoint.…"   6 minutes ago       Restarting (1) 2 seconds ago             testers

To monitor restarts continuously:

``` bash
watch docker ps -a
```

------------------------------------------------------------------------

# Changing Restart Policy of Running Container

Create container:

``` bash
docker run -itd --name=app1 httpd
```

Update restart policy:

``` bash
docker update --restart=always app1
```

Verify:

``` bash
docker inspect app1 | grep -iA 3 restartpolicy
```

Output:

    "RestartPolicy": {
        "Name": "always",
        "MaximumRetryCount": 0
    },

------------------------------------------------------------------------

# Conclusion

The **`on-failure` restart policy** is useful when you want Docker to
restart containers **only when the application crashes**.

Docker will restart the container when:

-   The container exits with a **non-zero exit code**
-   The application inside the container fails

Docker will **not restart the container** if:

-   The container stops normally
-   Docker daemon restarts
-   The system reboots

This policy is commonly used for **batch jobs, workers, and
error‑recovery scenarios**.


# Docker `--rm` Option (Not a Restart Policy)

## Overview

The `--rm` option in Docker is **not a restart policy**.

It is used to **automatically remove the container when it stops or
exits**.\
This helps keep the system clean by preventing unused stopped containers
from accumulating.

------------------------------------------------------------------------

## Key Behaviour

-   The container is **automatically deleted when it stops**
-   It **does not restart the container**
-   It is commonly used for **temporary or testing containers**
-   Once the container exits, it **cannot be started again because it is
    removed**

------------------------------------------------------------------------

## Syntax

``` bash
docker run <options> --rm <image>:<tag>
```

Example:

``` bash
docker run -itd --rm --name=demoapp nginx
```

------------------------------------------------------------------------

## Practical Demonstration

### Pull Image

``` bash
docker pull nginx
```

### Verify Images

``` bash
docker images
```

### Run Container with `--rm`

``` bash
docker run -itd --rm --name=demoapp nginx
```

### Verify Restart Policy

``` bash
docker inspect demoapp | grep -iA 3 restartpolicy
```

Output:

    "RestartPolicy": {
        "Name": "no",
        "MaximumRetryCount": 0
    }

This confirms that `--rm` **does not set a restart policy**.

------------------------------------------------------------------------

## Check Container Status

``` bash
docker ps -a
```

    -----------(The Status is UP)-------------

------------------------------------------------------------------------

## Restart Docker

``` bash
systemctl restart docker
```

Check again:

    -----------(The Status is Exited)-------------

Since the container stops, Docker **automatically removes it** because
of the `--rm` option.

------------------------------------------------------------------------

## Conclusion

`--rm` is **not a restart policy**.

It is simply a **cleanup option** that automatically removes the
container after it stops.\
This is useful for **temporary containers, testing, and short-lived
tasks**.
