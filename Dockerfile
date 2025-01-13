# Використання офіційного slim-образу Python
FROM python:3.11-slim

# Встановлення робочої директорії
WORKDIR /app

# Додавання залежностей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копіювання файлу залежностей
COPY requirements.txt .

# Інсталяція Python-залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання проекту
COPY . .

# Визначення команди запуску
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
