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
        """Инициализация с базовыми Web3 терминами"""
        default_terms = [
            {
                "keyword": "blockchain",
                "title": "Блокчейн",
                "definition": "Распределенная база данных, которая хранит информацию в блоках, связанных между собой криптографическими хешами. Каждый блок содержит хеш предыдущего блока, что обеспечивает целостность данных.",
                "source": "https://en.wikipedia.org/wiki/Blockchain",
                "category": "Технология",
                "related_terms": ["cryptocurrency", "distributed-ledger", "consensus"]
            },
            {
                "keyword": "cryptocurrency",
                "title": "Криптовалюта",
                "definition": "Цифровая или виртуальная валюта, защищенная криптографией, что делает практически невозможной подделку или двойное расходование. Большинство криптовалют основаны на технологии блокчейн.",
                "source": "https://en.wikipedia.org/wiki/Cryptocurrency",
                "category": "Финансы",
                "related_terms": ["blockchain", "bitcoin", "token"]
            },
            {
                "keyword": "bitcoin",
                "title": "Биткоин",
                "definition": "Первая и самая известная криптовалюта, созданная в 2009 году. Использует децентрализованную сеть и технологию блокчейн для осуществления транзакций без посредников.",
                "source": "https://bitcoin.org/",
                "category": "Криптовалюта",
                "related_terms": ["cryptocurrency", "blockchain", "mining"]
            },
            {
                "keyword": "ethereum",
                "title": "Эфириум",
                "definition": "Децентрализованная платформа с открытым исходным кодом, которая использует технологию блокчейн для создания смарт-контрактов и децентрализованных приложений (DApps).",
                "source": "https://ethereum.org/",
                "category": "Платформа",
                "related_terms": ["blockchain", "smart-contract", "dapp"]
            },
            {
                "keyword": "smart-contract",
                "title": "Смарт-контракт",
                "definition": "Самоисполняющийся контракт, условия которого записаны в виде кода на блокчейне. Автоматически выполняет условия соглашения при выполнении определенных условий.",
                "source": "https://ethereum.org/en/developers/docs/smart-contracts/",
                "category": "Технология",
                "related_terms": ["ethereum", "blockchain", "dapp"]
            },
            {
                "keyword": "dapp",
                "title": "Децентрализованное приложение",
                "definition": "Приложение, которое работает на децентрализованной сети, такой как блокчейн, и не контролируется единым органом. Использует смарт-контракты для выполнения логики.",
                "source": "https://ethereum.org/en/developers/docs/dapps/",
                "category": "Приложение",
                "related_terms": ["ethereum", "smart-contract", "web3"]
            },
            {
                "keyword": "web3",
                "title": "Web3",
                "definition": "Концепция следующего поколения интернета, основанная на децентрализации, блокчейне и токенах. Предполагает возврат контроля над данными пользователям.",
                "source": "https://web3.foundation/",
                "category": "Концепция",
                "related_terms": ["blockchain", "dapp", "decentralization"]
            },
            {
                "keyword": "nft",
                "title": "NFT (Non-Fungible Token)",
                "definition": "Уникальный токен, который представляет право собственности на цифровой или физический актив. Каждый NFT уникален и не может быть заменен другим токеном.",
                "source": "https://ethereum.org/en/nft/",
                "category": "Токен",
                "related_terms": ["token", "blockchain", "ethereum"]
            },
            {
                "keyword": "token",
                "title": "Токен",
                "definition": "Цифровой актив, выпущенный на блокчейне. Может представлять различные активы: криптовалюту, право собственности, голосование и т.д.",
                "source": "https://ethereum.org/en/developers/docs/standards/tokens/",
                "category": "Токен",
                "related_terms": ["cryptocurrency", "nft", "blockchain"]
            },
            {
                "keyword": "defi",
                "title": "DeFi (Decentralized Finance)",
                "definition": "Финансовая система, построенная на блокчейне, которая устраняет посредников и позволяет пользователям напрямую взаимодействовать с финансовыми услугами через смарт-контракты.",
                "source": "https://ethereum.org/en/defi/",
                "category": "Финансы",
                "related_terms": ["smart-contract", "blockchain", "dapp"]
            },
            {
                "keyword": "mining",
                "title": "Майнинг",
                "definition": "Процесс добавления новых транзакций в блокчейн путем решения сложных математических задач. Майнеры получают вознаграждение за свою работу.",
                "source": "https://en.wikipedia.org/wiki/Cryptocurrency",
                "category": "Процесс",
                "related_terms": ["bitcoin", "blockchain", "consensus"]
            },
            {
                "keyword": "consensus",
                "title": "Консенсус",
                "definition": "Механизм достижения согласия в децентрализованной сети о состоянии блокчейна. Популярные алгоритмы: Proof of Work (PoW) и Proof of Stake (PoS).",
                "source": "https://ethereum.org/en/developers/docs/consensus-mechanisms/",
                "category": "Механизм",
                "related_terms": ["blockchain", "mining", "proof-of-stake"]
            },
            {
                "keyword": "proof-of-stake",
                "title": "Proof of Stake (PoS)",
                "definition": "Алгоритм консенсуса, при котором валидаторы блоков выбираются на основе количества токенов, которые они держат и готовы 'заблокировать' (стейкать).",
                "source": "https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/",
                "category": "Механизм",
                "related_terms": ["consensus", "ethereum", "staking"]
            },
            {
                "keyword": "staking",
                "title": "Стейкинг",
                "definition": "Процесс блокировки криптовалюты для участия в валидации транзакций в сети Proof of Stake и получения вознаграждений.",
                "source": "https://ethereum.org/en/staking/",
                "category": "Процесс",
                "related_terms": ["proof-of-stake", "consensus", "ethereum"]
            },
            {
                "keyword": "wallet",
                "title": "Криптокошелек",
                "definition": "Цифровой инструмент для хранения, отправки и получения криптовалют. Содержит приватные ключи, необходимые для доступа к средствам на блокчейне.",
                "source": "https://ethereum.org/en/wallets/",
                "category": "Инструмент",
                "related_terms": ["cryptocurrency", "private-key", "blockchain"]
            },
            {
                "keyword": "private-key",
                "title": "Приватный ключ",
                "definition": "Секретный ключ, который используется для подписи транзакций и доступа к криптовалюте. Должен храниться в секрете, так как его потеря означает потерю доступа к средствам.",
                "source": "https://ethereum.org/en/developers/docs/accounts/",
                "category": "Безопасность",
                "related_terms": ["wallet", "cryptocurrency", "public-key"]
            },
            {
                "keyword": "public-key",
                "title": "Публичный ключ",
                "definition": "Криптографический ключ, который может быть публично раскрыт и используется для получения криптовалюты. Выводится из приватного ключа, но обратное преобразование невозможно.",
                "source": "https://ethereum.org/en/developers/docs/accounts/",
                "category": "Безопасность",
                "related_terms": ["private-key", "wallet", "address"]
            },
            {
                "keyword": "address",
                "title": "Адрес",
                "definition": "Уникальный идентификатор в блокчейне, используемый для отправки и получения криптовалюты. Обычно представлен в виде строки символов.",
                "source": "https://ethereum.org/en/developers/docs/accounts/",
                "category": "Идентификатор",
                "related_terms": ["public-key", "wallet", "blockchain"]
            },
            {
                "keyword": "distributed-ledger",
                "title": "Распределенный реестр",
                "definition": "База данных, которая реплицируется и синхронизируется между участниками сети. Блокчейн является одним из типов распределенного реестра.",
                "source": "https://en.wikipedia.org/wiki/Distributed_ledger",
                "category": "Технология",
                "related_terms": ["blockchain", "decentralization"]
            },
            {
                "keyword": "decentralization",
                "title": "Децентрализация",
                "definition": "Распределение контроля и принятия решений от центрального органа к распределенной сети участников. Основной принцип Web3 и блокчейна.",
                "source": "https://ethereum.org/en/web3/",
                "category": "Концепция",
                "related_terms": ["web3", "blockchain", "distributed-ledger"]
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
            "Технология": "#4A90E2",
            "Финансы": "#50C878",
            "Криптовалюта": "#FFD700",
            "Платформа": "#9B59B6",
            "Приложение": "#E74C3C",
            "Концепция": "#3498DB",
            "Токен": "#F39C12",
            "Процесс": "#E67E22",
            "Механизм": "#1ABC9C",
            "Инструмент": "#34495E",
            "Безопасность": "#E91E63",
            "Идентификатор": "#607D8B"
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
