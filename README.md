<div align="center">

# 🌾 CropDrop — AI-Powered Smart Irrigation

<img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge&logo=vercel" />
<img src="https://img.shields.io/badge/Theme-Smart%20Agriculture-2E7D32?style=for-the-badge&logo=leaflet&logoColor=white" />
<img src="https://img.shields.io/badge/Goal-Water%20Conservation-0288D1?style=for-the-badge&logo=water&logoColor=white" />

<br/><br/>

> **When to irrigate. How much water. Why.**
>
> CropDrop is an AI-powered smart irrigation platform that helps farmers make data-driven decisions about water usage — reducing waste, saving resources, and growing smarter crops.

<br/>

```
🌱 Soil Moisture: 27%  ·  🌡️ Temp: 33°C  ·  🌧️ Rain: 15%
                    ↓
         🤖 CropDrop AI Engine
                    ↓
     🔴 IRRIGATE  ·  💧 420 L  ·  ⏰ 6:00 PM
```

<br/>

[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🔄 System Flow](#-system-flow)
- [🖥️ Screenshots & Pages](#️-screenshots--pages)
- [🧠 AI Decision Engine](#-ai-decision-engine)
- [🌿 Crop Profiles](#-crop-profiles)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [🐳 Docker Deployment](#-docker-deployment)
- [📡 API Reference](#-api-reference)
- [📂 Project Structure](#-project-structure)
- [🌍 Impact Measurement](#-impact-measurement)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Intelligence
- **Rule-Based Decision Engine** — Crop-specific thresholds with configurable parameters
- **Dynamic Recommendations** — IRRIGATE / WAIT_FOR_RAIN / MONITOR / NO_IRRIGATION
- **Water Volume Estimation** — Calculates exact liters based on field area, crop type, and growth stage
- **Explainable AI** — Every decision comes with human-readable reasoning

</td>
<td width="50%">

### 🖥️ Premium Dashboard
- **Real-time Monitoring** — Live sensor data visualization
- **Interactive Simulator** — What-if scenario analysis with instant results
- **Executive Analytics** — Water impact reports with beautiful charts
- **Responsive Design** — Works on desktop, tablet, and mobile

</td>
</tr>
<tr>
<td width="50%">

### 🌾 Smart Agriculture
- **Multi-Crop Support** — Tomato 🍅, Rice 🌾, Wheat 🌱
- **Growth Stage Awareness** — Different water needs at each stage
- **IoT-Ready Architecture** — Same API endpoints for real ESP32 sensors
- **Simulated Sensor Data** — 24-hour realistic telemetry curves

</td>
<td width="50%">

### 🏗️ Production Grade
- **Dockerized Stack** — One command to deploy everything
- **PostgreSQL** — Production database with SQLite fallback
- **Nginx** — High-performance static file serving
- **Environment Config** — Secure, cloud-ready deployment

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CropDrop Architecture                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐    │
│   │             │     │              │     │                 │    │
│   │   React     │────▶│   FastAPI    │────▶│   PostgreSQL    │    │
│   │   Frontend  │◀────│   Backend    │◀────│   Database      │    │
│   │   (Nginx)   │     │   (Uvicorn)  │     │                 │    │
│   │             │     │              │     │                 │    │
│   └─────────────┘     └──────┬───────┘     └─────────────────┘    │
│         :80                  │ :8000              :5432             │
│                              │                                     │
│                     ┌────────┴────────┐                            │
│                     │                 │                             │
│                     │  Rule Engine    │                             │
│                     │  + Crop         │                             │
│                     │    Profiles     │                             │
│                     │                 │                             │
│                     └─────────────────┘                            │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                    Docker Compose                            │  │
│   │   Orchestrates all 3 services with health checks            │  │
│   └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 System Flow

```
                    ┌──────────────────┐
                    │  Farmer adds     │
                    │  field + data    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Sensor data     │
                    │  received via    │
                    │  API endpoint    │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
       ┌────────────────┐      ┌──────────────────┐
       │  Rule Engine   │      │  Crop Profile    │
       │  evaluates     │◀─────│  lookup          │
       │  conditions    │      │  (Tomato/Rice/   │
       │                │      │   Wheat)         │
       └───────┬────────┘      └──────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │  Decision Matrix    │
    │                     │
    │  moisture < min?    │──── YES + no rain ──▶ 🔴 IRRIGATE
    │                     │──── YES + rain    ──▶ 🔵 WAIT_FOR_RAIN
    │  moisture < optimal?│──── YES + no rain ──▶ 🔴 IRRIGATE (half)
    │                     │──── YES + rain    ──▶ 🟡 MONITOR
    │  moisture >= optimal│────────────────────▶ 🟢 NO_IRRIGATION
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │  Output:            │
    │  ✓ Status           │
    │  ✓ Water (liters)   │
    │  ✓ Best time        │
    │  ✓ Reasoning list   │
    └─────────────────────┘
```

---

## 🖥️ Screenshots & Pages

| Page | Description |
|------|-------------|
| **Dashboard** `/` | Hero banner with live stats, animated counters, irrigation alerts, and field status overview |
| **My Fields** `/fields` | Filterable card grid with moisture bars, status badges, and quick stats per field |
| **Field Details** `/fields/:id` | Dark hero banner, large metric cards, interactive moisture trend chart with reference lines |
| **AI Advisor** `/advisor` | Dual-pane analysis — live telemetry on the left, rule engine verdict with reasoning on the right |
| **Simulator** `/simulator` | Interactive sliders + 4 demo scenario pills. Run what-if analyses through the live rule engine |
| **Analytics** `/analytics` | Executive KPI cards, water impact bar chart, and aggregate moisture area chart |

---

## 🧠 AI Decision Engine

CropDrop uses a **hybrid rule-based engine** — not a black-box model. Every decision is transparent and explainable.

### Decision Logic

```python
IF soil_moisture < crop_minimum:
    IF rain_probability >= 60%  →  🔵 WAIT_FOR_RAIN
    ELSE                        →  🔴 IRRIGATE (full dose)

ELIF soil_moisture < crop_optimal:
    IF rain_probability >= 60%  →  🔵 WAIT_FOR_RAIN
    ELIF rain_probability >= 30% → 🟡 MONITOR
    ELSE                        →  🔴 IRRIGATE (half dose)

ELSE:
    →  🟢 NO_IRRIGATION
```

### Water Calculation

```
water = base_requirement × growth_stage_factor × field_area
```

- **Full dose**: When moisture is critically below minimum
- **Half dose**: When moisture is sub-optimal but not critical

---

## 🌿 Crop Profiles

Each crop has scientifically-inspired (prototype) thresholds:

| Crop | Min Moisture | Optimal | Base Water (L/acre) | Stages |
|------|:-----------:|:-------:|:-------------------:|--------|
| 🍅 Tomato | 30% | 45% | 150 | Seedling (0.6×), Vegetative (1.0×), Flowering (1.5×), Fruiting (1.3×) |
| 🌾 Rice | 65% | 80% | 400 | Vegetative (1.0×), Reproductive (1.5×), Ripening (0.7×) |
| 🌱 Wheat | 35% | 55% | 120 | Tillering (0.8×), Stem Extension (1.2×), Heading (1.5×), Maturation (0.5×) |

> ⚠️ **Note:** These values are prototype assumptions for demonstration purposes. They have not been scientifically validated on real farms.

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:-----:|:----------:|:--------|
| 🎨 **Frontend** | React 18 + Vite | Single-page application |
| 🎨 **Styling** | Tailwind CSS | Utility-first CSS with custom animations |
| 📊 **Charts** | Recharts | Interactive data visualization |
| 🔌 **Icons** | Lucide React | Beautiful open-source icons |
| ⚡ **Backend** | FastAPI + Uvicorn | High-performance async API |
| 🧩 **ORM** | SQLAlchemy 2.0 | Database abstraction layer |
| ✅ **Validation** | Pydantic v2 | Request/response schema validation |
| 🗄️ **Database** | PostgreSQL 15 | Production database |
| 🗄️ **Dev DB** | SQLite | Local development fallback |
| 🐳 **Container** | Docker Compose | Multi-service orchestration |
| 🌐 **Web Server** | Nginx | Static file serving + reverse proxy |

</div>

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** ≥ 18
- **Python** ≥ 3.10
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Asmitpandey112/Crop-Drop-Smart-Irrigation.git
cd Crop-Drop-Smart-Irrigation
```

### 2. Start the Backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python generate_rich_db.py       # Seed the database
uvicorn app.main:app --reload    # Start on http://127.0.0.1:8000
```

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev    # Start on http://localhost:5173
```

### 4. Open in Browser

Navigate to **`http://localhost:5173`** and explore the dashboard!

---

## 🐳 Docker Deployment

Deploy the entire production stack with a single command:

```bash
docker-compose up --build -d
```

This spins up:
- 🗄️ **PostgreSQL** on port `5432`
- ⚡ **FastAPI** on port `8000`
- 🌐 **Nginx + React** on port `80`

Access the app at **`http://localhost`**

### Environment Variables

Copy the example and configure:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///./cropdrop.db` |
| `VITE_API_URL` | Frontend → Backend API URL | `http://127.0.0.1:8000/api` |
| `POSTGRES_USER` | DB username | `cropdrop_user` |
| `POSTGRES_PASSWORD` | DB password | `cropdrop_password` |
| `POSTGRES_DB` | DB name | `cropdrop_db` |

---

## 📡 API Reference

### Fields

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/fields/` | List all fields with latest status |
| `GET` | `/api/fields/{id}` | Get field details |
| `POST` | `/api/fields/` | Create a new field |
| `DELETE` | `/api/fields/{id}` | Delete a field |
| `GET` | `/api/fields/{id}/readings` | Get sensor history |
| `POST` | `/api/fields/{id}/readings` | Submit sensor reading (IoT-ready) |
| `GET` | `/api/fields/{id}/recommendation` | Get AI recommendation |

### Prediction

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/predict` | Run what-if simulation |

#### Example Request

```json
{
  "soilMoisture": 27,
  "temperature": 33,
  "humidity": 58,
  "rainProbability": 15,
  "crop": "Tomato",
  "growthStage": "Flowering",
  "fieldArea": 2.5
}
```

#### Example Response

```json
{
  "status": "IRRIGATE",
  "waterAmount": 562.5,
  "recommendedTime": "18:00",
  "reasons": [
    "Soil moisture (27.0%) is below Tomato minimum target (30.0%).",
    "Rain probability is currently low (15.0%).",
    "Crop is in Flowering stage, requiring calculated dose."
  ]
}
```

---

## 📂 Project Structure

```
Crop-Drop-Smart-Irrigation/
│
├── 🐳 docker-compose.yml          # Production orchestration
├── 📄 .env.example                 # Environment template
│
├── ⚡ backend/
│   ├── Dockerfile                  # Backend container
│   ├── requirements.txt            # Python dependencies
│   ├── generate_rich_db.py         # Database seeder
│   └── app/
│       ├── main.py                 # FastAPI application entry
│       ├── database/
│       │   └── database.py         # SQLAlchemy config (SQLite/PostgreSQL)
│       ├── models/
│       │   └── domain.py           # ORM models (User, Field, Sensor, etc.)
│       ├── schemas/
│       │   ├── field.py            # Pydantic field schemas
│       │   └── prediction.py       # Pydantic prediction schemas
│       ├── routers/
│       │   ├── fields.py           # CRUD + recommendation endpoints
│       │   └── predictions.py      # Simulation endpoint
│       └── services/
│           ├── crop_profiles.py    # Configurable crop thresholds
│           └── rule_engine.py      # Decision logic engine
│
└── 🎨 frontend/
    ├── Dockerfile                  # Multi-stage build + Nginx
    ├── nginx.conf                  # Production web server config
    ├── package.json                # Node dependencies
    └── src/
        ├── components/
        │   └── Sidebar.jsx         # Collapsible nav with live status
        ├── layouts/
        │   └── AppLayout.jsx       # Main layout wrapper
        ├── pages/
        │   ├── Dashboard.jsx       # Hero banner + stats + alerts
        │   ├── FieldsList.jsx      # Filterable field cards
        │   ├── FieldDetails.jsx    # Field deep-dive + charts
        │   ├── AIAdvisor.jsx       # AI recommendation panel
        │   ├── Simulator.jsx       # What-if scenario tool
        │   └── Analytics.jsx       # Executive reports
        ├── services/
        │   └── api.js              # Backend API client
        └── data/
            └── mockData.js         # Fallback mock data
```

---

## 🌍 Impact Measurement

> 📄 **Full report:** [`IMPACT_MEASUREMENT.md`](IMPACT_MEASUREMENT.md)

CropDrop aligns with **UN SDG 6 (Clean Water)** and **SDG 2 (Zero Hunger)**. Here are the key projected impact numbers:

<div align="center">

| Metric | Per Field / Week | Per Farm / Year (5 fields) |
|:------:|:---------------:|:--------------------------:|
| 💧 **Water Saved** | ~2,000 L | **520,000 L** |
| 💰 **Cost Saved** (India) | — | **₹2,600 – ₹7,800** |
| 🌍 **CO₂ Avoided** | — | **~95 kg** |
| ⏱️ **Farmer Time Saved** | ~14 hrs | **~730 hrs** |

</div>

### Scalability

| Scale | Fields | Annual Water Saved | Equivalent |
|-------|:------:|:-----------------:|:----------:|
| 1 Farm | 5 | 520,000 L | 1 family's water for 208 days |
| 50 Farms (Village) | 250 | 26 million L | Fills 10 Olympic pools |
| 500 Farms (District) | 2,500 | 260 million L | **104 Olympic pools** |

### How We Measure

```
┌──────────────────┐        ┌──────────────────┐
│ Traditional Mode │        │  CropDrop Mode   │
│ (Fixed Schedule) │        │ (Rule Engine)    │
│                  │        │                  │
│ Irrigate every   │        │ Only irrigate    │
│ 2 days: 500 L    │   vs   │ when needed:     │
│                  │        │ 0 – 562 L        │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
         └───────────┬───────────────┘
                     ▼
         ┌───────────────────────┐
         │  Δ = Water Avoided   │
         │  Logged per decision │
         └───────────────────────┘
```

### UN SDG Alignment

| SDG | Contribution |
|:---:|-------------|
| **SDG 2** Zero Hunger | Optimizes crop water for better yields |
| **SDG 6** Clean Water | Reduces agricultural water waste by 40–60% |
| **SDG 12** Responsible Consumption | Data-driven resource allocation |
| **SDG 13** Climate Action | Reduces pump energy & CO₂ emissions |

> ⚠️ All metrics are projected estimates from prototype simulation data. Real-world validation is planned.

---

## 🗺️ Roadmap

- [x] Phase 1 — React Frontend with Tailwind CSS
- [x] Phase 2 — FastAPI Backend with REST endpoints
- [x] Phase 3 — SQLAlchemy + SQLite Database
- [x] Phase 4 — Frontend ↔ Backend Integration
- [x] Phase 5 — Rule-Based Irrigation Engine + Crop Profiles
- [x] Production — Docker, Nginx, PostgreSQL, Environment Config
- [ ] Phase 6 — ML Model (scikit-learn RandomForestRegressor)
- [ ] Phase 7 — Real Weather API Integration
- [ ] Phase 8 — User Authentication (JWT)
- [ ] Phase 9 — Real IoT Sensor Integration (ESP32/MQTT)
- [ ] Phase 10 — Mobile-First PWA

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">

### 🌍 Built for Smart Agriculture Hackathon

**Theme:** Smart Agriculture 🌾 — Technology to make farming more resource-efficient

**SDG Goal:** Reduce unnecessary water usage through data-driven irrigation

<br/>

Made with 💚 by [Asmit kumar](https://github.com/Asmitpandey112)

<br/>

<img src="https://img.shields.io/badge/Save_Water-Save_Life-0288D1?style=for-the-badge&logo=water&logoColor=white" />

</div>
