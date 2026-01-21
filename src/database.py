from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

Base = declarative_base()

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    protein_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)
    carbohydrates_g = Column(Float, nullable=False)

class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    ingredients = relationship('DishIngredient', back_populates='dish')

class DishIngredient(Base):
    __tablename__ = 'dish_ingredients'
    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    amount = Column(Float, nullable=False)
    
    dish = relationship('Dish', back_populates='ingredients')
    ingredient = relationship('Ingredient')

# Настройка подключения
engine = create_engine('sqlite:///menu.db')
Base.metadata.create_all(engine)

def get_session() -> Session:
    return Session(bind=engine)
