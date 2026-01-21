from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Dish:
    id: int
    name: str
    ingredients: Dict[str, float] = None
    nutrition: Optional[dict] = None

    def __post_init__(self):
        if self.ingredients is None:
            self.ingredients = {}
        if self.nutrition is None:
            self.nutrition = {}

    @property
    def total_weight(self) -> float:
        """Возвращает общий вес порции как сумму весов всех ингредиентов"""
        return sum(self.ingredients.values())
