# 💬 P2P Chat App (Socket-based)

A multi-client terminal chat application built with **pure Python** — no third-party libraries required.

---

## 📁 Project Structure

```
p2p_chat/
├── server.py   # Central relay server
├── client.py   # Chat client
└── README.md
```

---

## 🚀 How to Run

### Step 1 — Start the server (one terminal)
```bash
python server.py
```

### Step 2 — Start client(s) (separate terminals)
```bash
python client.py
```
Each client will be prompted for a username. Open as many terminals as you like!

---

## 🧠 Core Concepts Used

| Concept          | Where Used                                  |
|------------------|---------------------------------------------|
| `socket`         | TCP connection between server and clients   |
| `threading`      | Each client runs on its own thread          |
| `Lock`           | Thread-safe access to the clients registry  |
| OOP & functions  | Modular design for broadcast/receive/send   |
| `daemon=True`    | Threads auto-exit when main program exits   |

---

## 💡 Features

- Multiple clients can chat simultaneously
- Server broadcasts join/leave notifications
- Graceful disconnection with `quit` or `exit`
- Thread-safe client registry using `threading.Lock`
- Works on LAN by changing `HOST` to the server's IP

---

## 📌 Resume Talking Points

- Designed a **multi-threaded TCP chat server** handling concurrent client connections
- Implemented **thread-safe state management** using `threading.Lock`
- Built a **non-blocking client** using a dedicated receiver thread alongside a sender thread
- Used Python's `socket` module for low-level **network programming**