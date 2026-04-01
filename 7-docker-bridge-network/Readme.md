 # Docker Bridge Networks

This README documents Docker Bridge Networks, the default networking driver for Docker containers. Bridge networks enable container-to-container communication and provide network isolation.

------------------------------------------------------------------------

## Overview of Docker Bridge Network

The bridge network driver is the default Docker network driver with the following characteristics:

- Default CIDR block is assigned automatically
- Containers in the same bridge network can communicate with each other
- Containers can initiate outbound connections to the internet
- Bridge network does not accept inbound traffic from the internet by default
- Bridge network is configured as NAT (Network Address Translation)
- Bridge networks are private networks
- Containers in different bridge networks cannot communicate with each other
- Docker host can communicate with each container in the bridge network
- Provides application isolation through network segmentation

------------------------------------------------------------------------

## 1. View Default Bridge Network

List all available networks:

```bash
docker network ls
```

Inspect the default bridge network:

```bash
docker network inspect bridge
```

------------------------------------------------------------------------

## 2. Create a Custom Bridge Network

**Syntax:**

```bash
docker network create <network-name> --driver=bridge
```

**Example:**

Create a new bridge network named `newnet`:

```bash
docker network create newnet --driver=bridge
```

Verify the network was created:

```bash
docker network ls
```

------------------------------------------------------------------------

## 3. Run Containers on Custom Bridge Networks

First, pull a container image:

```bash
docker pull centos:8
```

Run a container on the default bridge network:

```bash
docker run -itd --name=app1 centos:8
```

Run a container on the custom bridge network:

```bash
docker run -itd --name=app2 --network=newnet centos:8
```

Inspect the network configuration of a container:

```bash
docker inspect app2 | grep -iA 10 network
```

------------------------------------------------------------------------

## 4. Test Container Communication

**Test #1: Containers on Different Networks**

Start a container on the custom network:

```bash
docker run -itd --name=app2 --network=newnet centos:8
```

Try to ping app1 from app2 (this will **fail** as they are on different networks):

```bash
docker exec -it app2 /bin/bash
ping app1
# Result: ping will not succeed - no communication between different networks
```

**Test #2: Containers on the Same Network**

Start another container on the same custom network:

```bash
docker run -itd --name=app3 --network=newnet centos:8
```

Try to ping app1 from app3 (this will **succeed** as they are on the same network):

```bash
docker exec -it app3 /bin/bash
ping app1
# Result: ping will succeed - communication is possible on the same network
```

------------------------------------------------------------------------

## Key Takeaways

**Important Notes:**

- Containers do not have their own Network Interface Card (NIC). They use the NIC of the Docker host.
- Network isolation is achieved through namespace and routing rules, not physical NICs.
- Only containers on the same bridge network can communicate with each other by default.
- Use different bridge networks to isolate application environments and microservices. 