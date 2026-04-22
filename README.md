# 🚀 NotifyX

NotifyX is a full-stack job notification system that tracks job postings (India + global) and sends alerts to users based on their preferences.

It consists of:

- 🌐 **Frontend** — Web UI
- ⚙️ **Backend** — FastAPI
- 🔄 **Worker** — Background job processor
- 🗄️ **Database** — PostgreSQL

All services are prebuilt, containerized, and ready to run using Docker.

---

## 🐳 Run in 1 Command

**1. Clone the repository**

```bash
git clone https://github.com/arpitrajawat62/NotifyX-.git
cd NotifyX-
```

**2. Create a `.env` file** in the root directory:

```env
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=notifyx_db

# Optional — for email alerts
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email
EMAIL_PASS=your_password
```

**3. Start everything**

```bash
docker-compose up
```

> ⚡ Docker will automatically pull the latest images from Docker Hub.

---

## 🌍 Access the App

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

---

## 📦 Services Overview

| Service | Description |
|---|---|
| `frontend` | UI served via Nginx |
| `backend` | FastAPI REST API |
| `worker` | Background job processor |
| `postgres` | PostgreSQL database |

---

## 🔄 Prebuilt Docker Images

NotifyX uses prebuilt images hosted on Docker Hub — no build step needed:

- `arpitsingh09/notifyx:frontend`
- `arpitsingh09/notifyx:backend`
- `arpitsingh09/notifyx:worker`

---

## 🧠 How It Works

1. User registers and logs in
2. Creates job alerts (keyword, location, etc.)
3. Backend fetches job data from sources
4. Worker processes and filters matching jobs
5. Matching jobs → email notification sent

---

## 🔧 Useful Commands

```bash
# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# Pull latest images
docker-compose pull
```

---

## 📁 Project Structure

```
NotifyX-/
├── backend/
├── frontend/
├── worker/
├── docker-compose.yml
├── docker-compose.dev.yml
└── .env
```

---

## 📌 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (Nginx) |
| Backend | FastAPI (Python) |
| Worker | Async Python |
| Database | PostgreSQL |
| Infra | Docker & Docker Compose |

---

## ⚠️ Notes

- Make sure Docker is installed and running before starting
- Default ports: `3000` (frontend), `8000` (backend), `5432` (database)
- If a port is already in use, update it in `docker-compose.yml`

---

## 🚧 Roadmap

- [ ] More job sources (LinkedIn, Indeed)
- [ ] Push notifications
- [ ] Mobile app
- [ ] AI-based job recommendations

---

## 👨‍💻 Author

**Arpit Rajawat** · [github.com/arpitrajawat62](https://github.com/arpitrajawat62)

---

> ⭐ NotifyX automates job discovery and delivers relevant opportunities — so you never miss a match.
