from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Dict, Any
from models import (
    Term, TermCreate, TermUpdate, TermListItem,
    GraphData, GraphNode, GraphEdge, Message
)
from database import db

app = FastAPI(
    title="Web3 Glossary API",
    description="API для управления глоссарием Web3 терминов с поддержкой семантического графа",
    version="1.0.0"
)

# Подключение статических файлов для фронтенда
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница - редирект на фронтенд"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/static/index.html">
        <title>Web3 Glossary</title>
    </head>
    <body>
        <p>Redirecting to <a href="/static/index.html">frontend</a>...</p>
    </body>
    </html>
    """


@app.get("/api/terms", response_model=List[TermListItem], tags=["Термины"])
async def get_all_terms():
    """
    Получить список всех терминов
    
    Возвращает упрощенный список всех терминов в глоссарии.
    """
    terms = db.get_all_terms()
    return [
        TermListItem(
            id=term.id,
            keyword=term.keyword,
            title=term.title,
            category=term.category
        )
        for term in terms
    ]


@app.get("/api/terms/{keyword}", response_model=Term, tags=["Термины"])
async def get_term(keyword: str):
    """
    Получить информацию о конкретном термине по ключевому слову
    
    - **keyword**: Ключевое слово термина (регистр не важен)
    """
    term = db.get_term(keyword)
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ключевым словом '{keyword}' не найден"
        )
    return term


@app.post("/api/terms", response_model=Term, status_code=status.HTTP_201_CREATED, tags=["Термины"])
async def create_term(term: TermCreate):
    """
    Добавить новый термин в глоссарий
    
    - **keyword**: Ключевое слово (уникальное)
    - **title**: Название термина
    - **definition**: Определение
    - **source**: Источник (опционально)
    - **category**: Категория (опционально)
    - **related_terms**: Список связанных терминов (опционально)
    """
    try:
        new_term = db.create_term(term)
        return new_term
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.put("/api/terms/{keyword}", response_model=Term, tags=["Термины"])
async def update_term(keyword: str, term_update: TermUpdate):
    """
    Обновить существующий термин
    
    - **keyword**: Ключевое слово термина для обновления
    - Все поля опциональны - обновляются только переданные поля
    """
    updated_term = db.update_term(keyword, term_update)
    if not updated_term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ключевым словом '{keyword}' не найден"
        )
    return updated_term


@app.delete("/api/terms/{keyword}", response_model=Message, tags=["Термины"])
async def delete_term(keyword: str):
    """
    Удалить термин из глоссария
    
    - **keyword**: Ключевое слово термина для удаления
    """
    deleted = db.delete_term(keyword)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ключевым словом '{keyword}' не найден"
        )
    return Message(message=f"Термин '{keyword}' успешно удален")


@app.get("/api/graph", tags=["Граф"])
async def get_graph_data() -> Dict[str, Any]:
    """
    Получить данные семантического графа для визуализации
    
    Возвращает узлы (термины) и ребра (связи между терминами) для построения графа.
    """
    graph_data = db.get_graph_data()
    
    nodes = [
        GraphNode(
            id=node["id"],
            label=node["label"],
            title=node["title"],
            definition=node["definition"],
            source=node.get("source"),
            category=node.get("category"),
            group=node.get("group")
        )
        for node in graph_data["nodes"]
    ]
    
    edges = [
        GraphEdge.model_validate({
            "from": edge["from"],
            "to": edge["to"],
            "label": edge.get("label")
        })
        for edge in graph_data["edges"]
    ]
    
    graph_result = GraphData(nodes=nodes, edges=edges)
    
    # Сериализуем с использованием алиасов для правильного формата JSON
    return graph_result.model_dump(mode='json', by_alias=True)


@app.get("/api/health", tags=["Система"])
async def health_check():
    """Проверка работоспособности API"""
    return {"status": "ok", "terms_count": len(db.terms)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
