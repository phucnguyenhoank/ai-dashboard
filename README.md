# 🚀 AI Dashboard
This is a FastAPI-based web application managed with [`uv`](https://docs.astral.sh/uv/) for fast and reproducible dependency management.

## 📦 Prerequisites

* **Python**: Version 3.8 or higher (see `.python-version`)
* **uv**: Modern Python package manager — install from [uv documentation](https://docs.astral.sh/uv/)

## 🛠️ Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/phucnguyenhoank/ai-dashboard.git
   cd ai-dashboard
   ```

2. **Install dependencies with `uv`:**

   ```bash
   uv sync
   ```

   This will create a virtual environment and install all dependencies from `uv.lock`.

3. **Run the FastAPI application using `uvicorn`:**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

4. **Access the API:**

   * Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
   * Base URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)
