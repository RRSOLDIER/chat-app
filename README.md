# Realtime Chat App 💬

## 📌 Project Overview
Realtime private chat application built using **Django** and **Django Channels**.

The system supports live messaging, online/offline presence tracking, message persistence, and read receipts.

---

## 🚀 Tech Stack

- Python
- Django (MVT Architecture)
- Django Channels (WebSocket)
- SQLite
- HTML / CSS / JavaScript
- Bootstrap

---

## ⚙️ Setup Instructions

###  Clone Repository

```bash
git clone https://github.com/RRSOLDIER/chat-app.git
cd chat-app
```

---

###  Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

---

###  Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is missing:

```bash
pip install django channels daphne
```

---

###  Run Database Migrations

```bash
python manage.py migrate
```

---

###  Run Server (Daphne)

```bash
daphne chat_app.asgi:application
```

Open browser:

```
http://127.0.0.1:8000/
```

---

##  Features Implemented

✔ User Authentication (Register / Login / Logout)  
✔ Custom User Model  
✔ Real-time Online / Offline Status  
✔ Private Chat via WebSocket  
✔ Message Persistence (SQLite)  
✔ Chat History  
✔ Read Receipts (✓ / ✓✓)  
✔ Prevent Empty Messages  
✔ Authenticated WebSocket Connections  

---

##  Test Credentials

Admin
Username: admin
Password: admin123

User 1
Username: john
Password: john123

User 2
Username: emma
Password: emma123

---

##  Functional Flow

1. Register / Login  
2. View user list  
3. Online users shown with green indicator  
4. Click user to start private chat  
5. Exchange messages in real-time  
6. Messages stored in database  
7. Read receipts update automatically  

---

##  Notes

- Uses Django Channels for WebSocket communication
- SQLite used for database
- Only authenticated users can access chat
- Only authenticated users can connect WebSocket

---


