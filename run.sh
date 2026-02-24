#!/bin/bash
# Скрипт для запуска приложения

# Активация виртуального окружения, если оно существует
if [ -d "venv" ]; then
    echo "🔌 Активация виртуального окружения..."
    source venv/bin/activate
fi

echo "🚀 Запуск PWA Glossary API..."
echo "API будет доступен по адресу: http://localhost:8000"
echo "Frontend: http://localhost:8000/static/index.html"
echo "API документация: http://localhost:8000/docs"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
