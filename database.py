"""
Простое in-memory хранилище для терминов.
В продакшене можно заменить на реальную БД (PostgreSQL, MongoDB и т.д.)
"""
from typing import Dict, List, Optional
from datetime import datetime
from models import Term, TermCreate, TermUpdate


class Database:
    """In-memory база данных для терминов"""
    
    def __init__(self):
        self.terms: Dict[str, Term] = {}
        self._initialize_default_terms()
    
    def _initialize_default_terms(self):
        """Инициализация с базовыми PWA терминами"""
        default_terms = [
            {
                "keyword": "pwa",
                "title": "Progressive Web Application (PWA)",
                "definition": "Прогрессивное веб-приложение — это веб-приложение, использующее современные веб-технологии для обеспечения опыта, сопоставимого с нативными мобильными приложениями: офлайн-работа, установка на устройство, push-уведомления.",
                "source": "https://web.dev/progressive-web-apps/",
                "category": "Концепция",
                "related_terms": ["service-worker", "web-app-manifest", "offline-first"]
            },
            {
                "keyword": "service-worker",
                "title": "Service Worker",
                "definition": "Фоновый скрипт, работающий отдельно от веб-страницы, который перехватывает сетевые запросы, управляет кэшированием и обеспечивает офлайн-режим и push-уведомления.",
                "source": "https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API",
                "category": "Технология",
                "related_terms": ["pwa", "cache-api", "push-notifications"]
            },
            {
                "keyword": "web-app-manifest",
                "title": "Web App Manifest",
                "definition": "JSON-файл, содержащий метаданные о веб-приложении (иконки, имя, цвет темы, режим отображения), позволяющий устанавливать PWA на устройство пользователя.",
                "source": "https://developer.mozilla.org/en-US/docs/Web/Manifest",
                "category": "Технология",
                "related_terms": ["pwa", "installable", "display-mode"]
            },
            {
                "keyword": "offline-first",
                "title": "Offline First",
                "definition": "Подход к разработке, при котором приложение изначально проектируется для работы без подключения к интернету с последующей синхронизацией данных при восстановлении сети.",
                "source": "https://web.dev/offline-cookbook/",
                "category": "Архитектура",
                "related_terms": ["pwa", "service-worker", "background-sync"]
            },
            {
                "keyword": "cache-api",
                "title": "Cache API",
                "definition": "Интерфейс браузера, позволяющий хранить и извлекать HTTP-запросы и ответы, обеспечивая гибкое кэширование ресурсов в PWA.",
                "source": "https://developer.mozilla.org/en-US/docs/Web/API/Cache",
                "category": "API",
                "related_terms": ["service-worker", "offline-first"]
            },
            {
                "keyword": "background-sync",
                "title": "Background Sync",
                "definition": "Механизм, позволяющий откладывать выполнение задач (например, отправку данных на сервер) до момента восстановления интернет-соединения.",
                "source": "https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API",
                "category": "API",
                "related_terms": ["service-worker", "offline-first"]
            },
            {
                "keyword": "push-notifications",
                "title": "Push-уведомления",
                "definition": "Сообщения, отправляемые сервером и отображаемые пользователю даже при закрытом приложении, реализуемые в PWA через Service Worker.",
                "source": "https://developer.mozilla.org/en-US/docs/Web/API/Push_API",
                "category": "Функциональность",
                "related_terms": ["service-worker", "notifications-api"]
            },
            {
                "keyword": "notifications-api",
                "title": "Notifications API",
                "definition": "Web API для отображения системных уведомлений пользователю с его разрешения.",
                "source": "https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API",
                "category": "API",
                "related_terms": ["push-notifications", "service-worker"]
            },
            {
                "keyword": "installable",
                "title": "Устанавливаемость (Installable)",
                "definition": "Характеристика PWA, позволяющая пользователю установить приложение на домашний экран устройства без использования App Store или Google Play.",
                "source": "https://web.dev/install-criteria/",
                "category": "Характеристика",
                "related_terms": ["pwa", "web-app-manifest"]
            },
            {
                "keyword": "display-mode",
                "title": "Display Mode",
                "definition": "Параметр Web App Manifest, определяющий способ отображения приложения (fullscreen, standalone, minimal-ui, browser).",
                "source": "https://developer.mozilla.org/en-US/docs/Web/Manifest/display",
                "category": "Конфигурация",
                "related_terms": ["web-app-manifest", "installable"]
            },
            {
                "keyword": "lighthouse",
                "title": "Lighthouse",
                "definition": "Инструмент аудита от Google для анализа производительности, доступности и соответствия PWA-стандартам.",
                "source": "https://developer.chrome.com/docs/lighthouse/",
                "category": "Инструмент",
                "related_terms": ["pwa", "performance"]
            },
            {
                "keyword": "performance",
                "title": "Производительность",
                "definition": "Ключевой показатель качества PWA, включающий быструю загрузку, минимизацию ресурсов и оптимизацию рендеринга.",
                "source": "https://web.dev/performance/",
                "category": "Метрика",
                "related_terms": ["lighthouse", "offline-first"]
            },
            {
                "keyword": "responsive-design",
                "title": "Адаптивный дизайн",
                "definition": "Подход к веб-разработке, при котором интерфейс корректно отображается на различных устройствах и размерах экранов.",
                "source": "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design",
                "category": "Дизайн",
                "related_terms": ["pwa"]
            },
            {
                "keyword": "https",
                "title": "HTTPS",
                "definition": "Защищённый протокол передачи данных, обязательное требование для работы Service Worker и большинства возможностей PWA.",
                "source": "https://developer.mozilla.org/en-US/docs/Glossary/HTTPS",
                "category": "Безопасность",
                "related_terms": ["service-worker", "pwa"]
            },
            {
                "keyword": "app-shell",
                "title": "App Shell Model",
                "definition": "Архитектурный подход, при котором базовая оболочка интерфейса кэшируется отдельно от динамического контента для обеспечения быстрой загрузки.",
                "source": "https://web.dev/app-shell/",
                "category": "Архитектура",
                "related_terms": ["service-worker", "offline-first"]
            }
        ]

        for term_data in default_terms:
            term = TermCreate(**term_data)
            self.create_term(term)
    
    def get_all_terms(self) -> List[Term]:
        """Получить все термины"""
        return list(self.terms.values())
    
    def get_term(self, keyword: str) -> Optional[Term]:
        """Получить термин по ключевому слову"""
        return self.terms.get(keyword.lower())
    
    def create_term(self, term: TermCreate) -> Term:
        """Создать новый термин"""
        keyword_lower = term.keyword.lower()
        if keyword_lower in self.terms:
            raise ValueError(f"Термин с ключевым словом '{term.keyword}' уже существует")
        
        now = datetime.now()
        new_term = Term(
            id=keyword_lower,
            keyword=term.keyword,
            title=term.title,
            definition=term.definition,
            source=term.source,
            category=term.category,
            related_terms=term.related_terms or [],
            created_at=now,
            updated_at=now
        )
        self.terms[keyword_lower] = new_term
        return new_term
    
    def update_term(self, keyword: str, term_update: TermUpdate) -> Optional[Term]:
        """Обновить существующий термин"""
        keyword_lower = keyword.lower()
        if keyword_lower not in self.terms:
            return None
        
        existing_term = self.terms[keyword_lower]
        update_data = term_update.model_dump(exclude_unset=True)
        
        if "related_terms" in update_data:
            existing_term.related_terms = update_data["related_terms"]
        
        for field, value in update_data.items():
            if field != "related_terms" and value is not None:
                setattr(existing_term, field, value)
        
        existing_term.updated_at = datetime.now()
        return existing_term
    
    def delete_term(self, keyword: str) -> bool:
        """Удалить термин"""
        keyword_lower = keyword.lower()
        if keyword_lower in self.terms:
            del self.terms[keyword_lower]
            # Удаляем связи с этим термином из других терминов
            for term in self.terms.values():
                if keyword_lower in term.related_terms:
                    term.related_terms.remove(keyword_lower)
            return True
        return False
    
    def get_graph_data(self) -> Dict:
        """Получить данные для графа"""
        nodes = []
        edges = []
        category_colors = {
            "Концепция": "#3498DB",
            "Технология": "#4A90E2",
            "Архитектура": "#9B59B6",
            "API": "#F39C12",
            "Функциональность": "#E74C3C",
            "Дизайн": "#1ABC9C",
            "Безопасность": "#E91E63",
            "Инструмент": "#34495E",
            "Характеристика": "#50C878",
            "Конфигурация": "#607D8B",
        }
        
        for term in self.terms.values():
            nodes.append({
                "id": term.id,
                "label": term.title,
                "title": term.title,
                "definition": term.definition,
                "source": term.source,
                "category": term.category,
                "group": term.category or "Другое",
                "color": category_colors.get(term.category, "#95A5A6")
            })
            
            for related_keyword in term.related_terms:
                related_term = self.terms.get(related_keyword.lower())
                if related_term:
                    edges.append({
                        "from": term.id,
                        "to": related_term.id,
                        "label": "связан с"
                    })
        
        return {"nodes": nodes, "edges": edges}


# Глобальный экземпляр базы данных
db = Database()
