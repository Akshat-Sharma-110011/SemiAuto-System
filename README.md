# SemiAuto-System

**SemiAuto-System** is a unified automation framework that integrates Regression, Classification, and Clustering pipelines under one orchestrated platform. Designed for **ML engineers**, **MLOps practitioners**, and **software developers**, it offers an API-driven and user-guided approach to automate the **entire machine learning lifecycle** while maintaining modularity and control.

---

## 🚀 Key Features

- ⚙️ Unified interface to access Regression, Classification, and Clustering pipelines
- 🌐 API-first with interactive web-based dashboard
- 📦 Modular microservices architecture
- 🔁 Seamless pipeline switching via user selection
- 🐳 Docker support for scalable deployment

---

## 🧱 System Architecture

```
SemiAuto-System/
├── app.py               # FastAPI Orchestrator (Main Gateway)
├── templates/           # Jinja2 HTML templates for UI
├── static/              # Static files (CSS/JS) placeholder
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
└── README.md            # Documentation
```

### 🧩 Microservices

- `semiauto-regression` (port 8030)
- `semiauto-classification` (port 8020)
- `semiauto-clustering` (port 8010)

### 🌐 Flow

1. User visits `/` and selects a pipeline.
2. Orchestrator sets the active microservice.
3. All API/static requests are proxied to the selected microservice.
4. Results are returned as if from a single unified system.

---

## 🛠️ Installation

### 🔧 Local Setup (Python)

```bash
git clone https://github.com/Akshat-Sharma-110011/SemiAuto-System.git
cd SemiAuto-System
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### 🐳 Docker Setup

```bash
docker build -t semiauto-system .
docker run -p 8000:8000 semiauto-system
```

> Ensure microservices (`semiauto-regression`, `semiauto-classification`, `semiauto-clustering`) are running and accessible at ports `8030`, `8020`, and `8010` respectively.

---

## 🚀 Usage Guide

### 🔘 Web Dashboard

Visit:

```
http://localhost:8000/
```

Select the pipeline (Regression / Classification / Clustering) → You’ll be redirected to that service's interface or instructions.

### 🔁 API Routing

Once a pipeline is selected:

- `POST /train` → forwarded to selected service’s `/train`
- `POST /predict` → forwarded to selected service’s `/predict`
- `GET /metrics` → forwarded to selected service’s `/metrics`
- Static assets (`/clustering-static/style.css`) are proxied accordingly

### 📋 Example: Select Classification Pipeline

```bash
curl -X POST -F "service_type=classification" http://localhost:8000/select-service
```

Then use:

```bash
curl -X POST http://localhost:8000/train -F file=@your_data.csv
```

---

## ⚙️ Configuration

Edit `app.py`:

```python
MICROSERVICES = {
    "regression": "http://semiauto-regression:8030",
    "classification": "http://semiauto-classification:8020",
    "clustering": "http://semiauto-clustering:8010"
}
```

Adjust hostnames/ports as per your deployment (e.g. Docker Compose or Kubernetes).

---

## 🚧 Limitations

- Microservices must be run separately
- No experiment tracking or database integration
- Minimal error handling / no retry logic
- No authentication or authorization
- Limited to tabular supervised/unsupervised pipelines

---

## 📈 Roadmap

- [ ] Support for additional ML pipeline types (NLP, Time Series)
- [ ] AutoML integration for parameter search
- [ ] Full MLOps lifecycle support (logging, versioning, monitoring)
- [ ] User authentication and access control
- [ ] Docker Compose or Helm chart for full orchestration
- [ ] Enhanced dashboard with drag-drop data and pipeline visualization

---

## 📚 Inspiration

This project is influenced by:

- **[H2O AutoML](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html)** – For streamlined, user-controllable automation.
- **Modular MLOps tools** – Emphasizing pipeline separation, extensibility, and runtime orchestration.

---

## 🪪 License

[MIT License](LICENSE)

---

## 🤝 Contributing

Feel free to fork, raise issues, or submit pull requests. Help expand the system with more pipelines, visualization tools, or deployment recipes!

