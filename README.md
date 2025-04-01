# 🌤️ Weather Sensor API

A lightweight FastAPI backend for ingesting weather sensor data and querying statistics like average, min, and max for temperature, humidity, and windspeed — built using Python, SQLite, and Pydantic.

---

## 📦 Features

- ✅ Add new sensor data via `POST /data`
- ✅ Query sensor metrics via `GET /query`
- ✅ Support for statistics like min, max, average, sum
- ✅ Date-based filtering (last N days, default = latest)
- ✅ Custom error handling and validation
- ✅ Unit and integration test coverage (84%+)
- ✅ Fully interactive Swagger UI at `/docs`

---

## ⚙️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pytest](https://docs.pytest.org/)
- [httpx](https://www.python-httpx.org/) (for integration tests)

---

## 🚀 Setup Instructions

### 📁 Clone the repo

```bash
git clone https://github.com/your-username/weather-sensor-api.git
cd weather-sensor-api
```

### 🐍 Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

### 🏃‍♂️ Run the API
```bash
uvicorn app.main:app --reload
```

### 🧪 Run tests + coverage
```bash
pytest --cov=app
pytest --cov-report=term-missing
```

