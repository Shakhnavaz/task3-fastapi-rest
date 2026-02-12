# Многоэтапная сборка для оптимизации размера образа
FROM python:3.13.11-slim as builder

# Установка системных зависимостей для компиляции
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Финальный образ (без компиляторов для уменьшения размера)
FROM python:3.13.11-slim

# Создание непривилегированного пользователя
RUN useradd -m -u 1000 appuser

# Копирование установленных пакетов из builder в домашнюю директорию пользователя
COPY --from=builder /root/.local /home/appuser/.local

# Установка переменных окружения
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Создание рабочей директории
WORKDIR /app

# Копирование кода приложения
COPY main.py models.py database.py ./
COPY static/ ./static/

# Изменение владельца файлов
RUN chown -R appuser:appuser /app /home/appuser/.local

# Переключение на непривилегированного пользователя
USER appuser

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
