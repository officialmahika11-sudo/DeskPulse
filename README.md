# 🖥️ DeskPulse — Personal Desktop Assistant

DeskPulse is a personal AI workflow built with **n8n** and **Python** that lets you monitor your desktop activity using simple text commands.

## ✨ Features

- ⏱️ **Screen Time Tracking** — tracks how many hours you've actively used your PC today
- 🔔 **Notifications Checker** — shows your recent app notifications
- ⏰ **Break Reminder** — plays a sound and shows a popup if you've been working for 10+ minutes continuously

## 🛠️ Built With

- [n8n](https://n8n.io) — workflow automation
- Python 3 — local data fetching and server
- Flask — lightweight local API server
- HTML/CSS/JS — chat interface

## 📁 Project Structure
DeskPulse/
├── server.py           # Flask API server
├── assistant.py        # Command handler script
├── monitor.py          # Background activity monitor
├── chat.html           # Browser chat interface
└── n8n assistant.json  # n8n workflow (importable)
## 🚀 How to Run

**1. Install dependencies**
```bash
pip install flask psutil plyer requests
```

**2. Start the Flask server**
```bash
python server.py
```

**3. Start the activity monitor**
```bash
python monitor.py
```

**4. Start n8n**
```bash
n8n start
```

**5. Import the workflow**
- Go to `localhost:5678`
- Click `...` → `Import from file`
- Select `n8n assistant.json`

**6. Open the chat interface**
- Open `chat.html` in your browser
- Type `screen time` or `notifications`

## 💬 Commands

| Command | Response |
|---------|----------|
| `screen time` | Shows today's active PC usage |
| `notifications` | Shows recent app notifications |


**7.How it works**
You type a command in chat.html (browser)
↓
n8n Webhook receives the POST request
↓
n8n HTTP Request node forwards it to Flask server (port 5000)
↓
Flask server runs the logic (screen time / notifications)
↓
Response sent back through n8n → displayed in browser

monitor.py runs in background every 60 seconds
↓
Detects active CPU usage → pings Flask /track endpoint
↓
Saves active minutes to screen_time.json
↓
Triggers popup + beep after 10 continuous minutes

---

## 🔄 n8n Workflow Detail

The workflow consists of **3 nodes** connected in sequence:

| Node | Type | Role |
|------|------|------|
| **Webhook** | Trigger | Listens for POST requests at `/assistant` path. Acts as the entry point — receives your text command from `chat.html` |
| **HTTP Request** | Action | Forwards the command as a JSON POST to the local Flask server at `http://127.0.0.1:5000/assistant` |
| **Respond to Webhook** | Output | Takes the Flask server's response and sends it back to the browser as plain text |

The workflow is fully local — no data leaves your machine at any point.

---

## 🛠️ Tech Stack

| Technology | Version | Purpose | Why This? |
|-----------|---------|---------|-----------|
| **n8n** | Latest | Workflow automation engine | Visual no-code tool to connect inputs and outputs without writing complex routing logic |
| **Python** | 3.11+ | Core logic and scripting | Best language for system-level tasks on Windows (reading processes, system stats) |
| **Flask** | 3.x | Local HTTP server | Lightweight micro-framework — runs a local API server in under 10 lines of code. Perfect for bridging n8n with Python scripts |
| **psutil** | Latest | System monitoring | Cross-platform library to read CPU usage, boot time, and process info |
| **plyer** | Latest | Desktop notifications | Simple cross-platform library to trigger native Windows popup notifications |
| **HTML/CSS/JS** | Vanilla | Chat interface | No framework needed — a single HTML file is enough for a local chat UI |

---

## 🖥️ Why Flask as the Local Server?

n8n is a workflow tool — it's great at connecting services but it can't directly run Python scripts or read your system data. Flask bridges this gap by:

- Running a **lightweight HTTP server on port 5000** on your local machine
- Exposing **API endpoints** (`/assistant`, `/track`) that n8n can call via HTTP Request node
- Executing **Python logic** (psutil, PowerShell commands) when those endpoints are hit
- Returning **JSON responses** that n8n can process and send back to you

Flask was chosen over alternatives because:
- ✅ Minimal setup — no configuration files needed
- ✅ Runs with a single `python server.py` command
- ✅ Perfect for local-only use cases like this
- ✅ Handles JSON natively with `jsonify()`
## 👤 Author

Made by [@officialmahika11-sudo](https://github.com/officialmahika11-sudo)


