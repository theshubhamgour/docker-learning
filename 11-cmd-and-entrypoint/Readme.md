# 🐳 CMD vs ENTRYPOINT in Docker (Beginner Friendly)

---

## 📌 1. What is CMD?

CMD is used to provide a **default command** for a container.

- It runs when the container starts
- It can be **overridden** at runtime

### 🔷 Diagram:
```
Dockerfile CMD  --->  docker run (no input)  --->  CMD executes

Dockerfile CMD  --->  docker run new command  --->  CMD replaced
```

### Example:
```dockerfile
FROM ubuntu
CMD ["echo", "Hello from CMD"]
```

---

## 📌 2. What is ENTRYPOINT?

ENTRYPOINT is used to define a **fixed command**.

- It always runs
- It **cannot be easily overridden**
- Extra input is passed as arguments

### 🔷 Diagram:
```
ENTRYPOINT (fixed) ---> docker run ---> always runs

ENTRYPOINT ---> docker run extra args ---> appended
```

### Example:
```dockerfile
FROM ubuntu
ENTRYPOINT ["echo", "Hello from ENTRYPOINT"]
```

---

## 📌 3. CMD vs ENTRYPOINT (Together)

Best practice is to use both together.

- ENTRYPOINT = main command
- CMD = default arguments

### 🔷 Diagram:
```
ENTRYPOINT (command) + CMD (args)

        ↓

docker run

        ↓

Final Execution:
command + arguments
```

### Example:
```dockerfile
FROM ubuntu
ENTRYPOINT ["echo"]
CMD ["Hello from CMD"]
```

---

## 🎯 Visual Comparison

```
CMD:
[Default Command] ---> can be REPLACED

ENTRYPOINT:
[Fixed Command] ---> cannot be replaced
                    only arguments added
```

---

## 🎯 Final Difference

| Feature        | CMD                    | ENTRYPOINT              |
|---------------|------------------------|------------------------|
| Purpose       | Default command        | Fixed command          |
| Override      | Yes                    | No (only args allowed) |
| Behavior      | Replaced               | Appended               |

---

## 💡 Simple Rule

👉 CMD = changeable  
👉 ENTRYPOINT = fixed  

👉 Together:
```
ENTRYPOINT + CMD = command + arguments
```

---

## 🧠 Real-life Analogy

```
ENTRYPOINT = Machine (fixed)
CMD = Input (changeable)

Machine + Input = Result
```

Example:
- Machine = calculator  
- Input = numbers  

---

## 🚀 When to Use?

- Use **CMD** when flexibility is needed
- Use **ENTRYPOINT** when you want fixed behavior

---

Happy Learning! 🎯
