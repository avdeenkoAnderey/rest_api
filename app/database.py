from datetime import datetime


class InMemoryDB:
    def __init__(self):
        self._store: dict[int, dict] = {}
        self._next_id: int = 1

    def create(self, title: str, description: str, price: float, author: str) -> dict:
        advertisement = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "price": price,
            "author": author,
            "created_at": datetime.now(),
        }
        self._store[self._next_id] = advertisement
        self._next_id += 1
        return advertisement

    def get_by_id(self, advertisement_id: int) -> dict | None:
        return self._store.get(advertisement_id)

    def update(self, advertisement_id: int, **kwargs) -> dict | None:
        advertisement = self._store.get(advertisement_id)
        if advertisement is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                advertisement[key] = value
        return advertisement

    def delete(self, advertisement_id: int) -> bool:
        if advertisement_id in self._store:
            del self._store[advertisement_id]
            return True
        return False

    def search(self, title: str | None = None, description: str | None = None, author: str | None = None) -> list[dict]:
        results = list(self._store.values())
        if title:
            results = [a for a in results if title.lower() in a["title"].lower()]
        if description:
            results = [a for a in results if description.lower() in a["description"].lower()]
        if author:
            results = [a for a in results if author.lower() in a["author"].lower()]
        return results


db = InMemoryDB()
