from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class TermBase(BaseModel):
    """Базовая модель термина"""
    keyword: str = Field(..., description="Ключевое слово термина", min_length=1)
    title: str = Field(..., description="Название термина", min_length=1)
    definition: str = Field(..., description="Определение термина", min_length=1)
    source: Optional[str] = Field(None, description="Источник определения")
    category: Optional[str] = Field(None, description="Категория термина")


class TermCreate(TermBase):
    """Модель для создания термина"""
    related_terms: Optional[List[str]] = Field(default=[], description="Список связанных терминов (ключевые слова)")


class TermUpdate(BaseModel):
    """Модель для обновления термина"""
    title: Optional[str] = Field(None, description="Название термина", min_length=1)
    definition: Optional[str] = Field(None, description="Определение термина", min_length=1)
    source: Optional[str] = Field(None, description="Источник определения")
    category: Optional[str] = Field(None, description="Категория термина")
    related_terms: Optional[List[str]] = Field(default=None, description="Список связанных терминов")


class Term(TermBase):
    """Модель термина с полной информацией"""
    id: str
    created_at: datetime
    updated_at: datetime
    related_terms: List[str] = Field(default=[], description="Список связанных терминов")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "blockchain",
                "keyword": "blockchain",
                "title": "Блокчейн",
                "definition": "Распределенная база данных, которая хранит информацию в блоках",
                "source": "https://example.com",
                "category": "Технология",
                "related_terms": ["cryptocurrency", "distributed-ledger"],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class TermListItem(BaseModel):
    """Упрощенная модель термина для списка"""
    id: str
    keyword: str
    title: str
    category: Optional[str] = None


class GraphNode(BaseModel):
    """Узел графа для визуализации"""
    id: str
    label: str
    title: str
    definition: str
    source: Optional[str] = None
    category: Optional[str] = None
    group: Optional[str] = None  # Для группировки по категориям


class GraphEdge(BaseModel):
    """Ребро графа для визуализации"""
    model_config = ConfigDict(
        populate_by_name=True,
        # Используем serialization_alias для вывода в JSON
    )
    
    from_id: str = Field(..., description="ID узла источника", serialization_alias="from", validation_alias="from")
    to_id: str = Field(..., description="ID узла назначения", serialization_alias="to", validation_alias="to")
    label: Optional[str] = None


class GraphData(BaseModel):
    """Данные графа для фронтенда"""
    model_config = ConfigDict(populate_by_name=True)
    
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class Message(BaseModel):
    """Модель для сообщений об ошибках/успехе"""
    message: str
