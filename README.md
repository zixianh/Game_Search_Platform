# Game Search Platform

A lightweight **game search and user preference system** built using **Flask** and **MySQL**.  
Supports **fuzzy search**, **user favorites**, and **multi-database redundancy**.

---

## Features

- Search games by **name**, **platform**, or **tag**
- Add / update / delete game records
- User **favorite / unfavorite** functionality
- Retrieve full favorite list for a user
- Two-database setup for reliability (GDB1 & GDB2)

---

## Tech Stack

| Component | Technology |
|---------|------------|
| Backend | Python, Flask, Flask-CORS |
| Database | MySQL (mysql-connector-python / pymysql) |
| Data Format | JSON, SQL |
| Optional UI | React (client folder) |

---

## Project Structure

```
Game_Search_Platform
│
├── client/                 # (Optional) React UI
│   ├── package.json
│   └── package-lock.json
│
├── docs/
│   └── report.pdf          # Project explanation/report
│
├── serve/                  # Backend
│   ├── app.py              # Flask API server
│   ├── matching.py         # Core DB + logic functions
│   ├── database1-v1.sql    # SQL schema + test data
│   └── database2-v2.sql
│
└── .gitignore              # Excludes venv & node_modules
```

---

## Setup & Run

### 1) Navigate to backend folder
```bash
cd serve
```

### 2) Create virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate     # Mac/Linux
# Windows: venv\Scripts\activate

pip install Flask flask-cors mysql-connector-python pymysql
```

### 3) Setup MySQL databases
```sql
CREATE DATABASE GDB1;
CREATE DATABASE GDB2;
```

Then import:
```
database1-v1.sql → GDB1
database2-v2.sql → GDB2
```

### 4) Run backend server
```bash
python app.py
```

Server starts at:
```
http://127.0.0.1:5000/
```

---

## API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/games/searchname/<name>` | GET | Search games by name |
| `/games/searchplatform/<platform>` | GET | Search games by platform |
| `/games/searchtag/<tag>` | GET | Search games by tag |
| `/favourite/<user_id>/<game_id>` | GET | Favorite a game |
| `/unfavourite/<user_id>/<game_id>` | GET | Remove favorite |
| `/allfavgames/<user_id>` | GET | Get all favorite games |
| `/insertgame/...` | GET | Insert a game |
| `/updategame/<id>?price=...` | GET | Update game fields |
| `/deletegame/<id>` | GET | Delete game |

---