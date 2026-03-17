# 🐳 Docker Commit - Complete Practical Guide

![Docker](https://img.shields.io/badge/Docker-Commit-blue)
![Level](https://img.shields.io/badge/Level-Beginner-green)
![Type](https://img.shields.io/badge/Hands--On-Practical-orange)

---

## 📑 Table of Contents
- [What is Docker Commit?](#-what-is-docker-commit)
- [Why Use It?](#-why-use-it)
- [Syntax](#-syntax)
- [Hands-On Demo](#-hands-on-demo)
- [Visual Flow](#-visual-flow)
- [Storage Path (Layers)](#-storage-path-layers)
- [Real-World Use Cases](#-real-world-use-cases)
- [Interview Questions](#-interview-questions)
- [Summary](#-summary)

---

## 📌 What is Docker Commit?

Docker commit creates a **new image from a running container’s current state**.

👉 Think of it like:
> Taking a snapshot of your container after making changes.

---

## 🎯 Why Use It?

✅ Save manual changes  
✅ Quick prototyping  
✅ Learning & debugging  

⚠️ Not recommended for production → use Dockerfile instead

---

## 🧾 Syntax

```
docker commit <container-id/name> <image>:<tag>
```

---

##  Hands-On Demo

### 1️⃣ Create Image from Container
```
docker commit new-ubuntu mynginx:v1
docker images
```

---

### 2️⃣ Run Container
```
docker run -itd --name=newapp -p 80:80 mynginx:v1
docker ps -a
```

---

### 3️⃣ Modify Inside Container
```
docker exec -it newapp /bin/bash
echo "Hello World" > /var/www/html/index.html
```

---

### 4️⃣ Verify Output
```
docker inspect newapp | grep -iA 4 ipaddress
curl <ip-address>
```

---

### 5️⃣ Commit Changes
```
docker commit newapp webapp:v2
docker images
```

---

### 6️⃣ Remove Old Container
```
docker rm -f newapp
```

---

### 7️⃣ Run Final Image
```
docker run -itd --name=server -p 8080:80 webapp:v2
```

---

## 🎬 Visual Flow 

```
Base Container → Modify → Commit → New Image → Run → Final App
```

---

## 📂 Storage Path (Layers)

```
/var/lib/containerd/io.containerd.content.v1.content/blobs/sha256
```

👉 Stores image & container layers (content-addressable)

---

## 🌍 Real-World Use Cases

🔹 Debugging production issue snapshot  
🔹 Saving temporary fixes quickly  
🔹 Creating demo environments  
🔹 Experimenting before writing Dockerfile  
🔹 Backup of container state  

---

## 🎤 Interview Questions

**Q1: What is docker commit?**  
👉 Creates image from container state  

**Q2: Is docker commit recommended?**  
👉 No, use Dockerfile for production  

**Q3: Difference between Dockerfile & commit?**  
👉 Dockerfile = reproducible  
👉 commit = manual snapshot  

**Q4: Where are layers stored?**  
👉 containerd storage path 
~~~
 (/var/lib/containerd/io.containerd.content.v1.content/blobs/sha256)
~~~

---

## 🔁 Summary

- Snapshot of container → image  
- Fast but not reproducible  
- Good for learning & debugging  
- Avoid in CI/CD pipelines  

---

## 💡 Pro Tip

Always prefer:
✔ Dockerfile  
✔ Version control  
✔ CI/CD pipelines  

---

⭐ If this helped, star your repo & share! 🚀
