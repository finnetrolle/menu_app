from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Dish:
    id: int
    name: str
    ingredients: Dict[str, float] = None
    nutrition: Optional[dict] = None
    # Nutrition attributes for API responses
    energy_kcal: float =0.0
    protein_g: float = 0.0
    fat_g: float = 0.0
    carbohydrates_g: float = 0.0
    weight_g: float = 0.0

    def __post_init__(self):
        if self.ingredients is None:
            self.ingredients = {}
        if self.nutrition is None:
            self.nutrition = {}

    @property
    def total_weight(self) -> float:
        """Возвращает общий вес порции как сумму весов всех ингредиентов"""
        return sum(self.ingredients.values())
