// Импортируем React и ReactDOM
const { useState, useEffect } = React;
const { render } = ReactDOM;

// Основной компонент приложения
const App = () => {
    const [goals, setGoals] = useState({
        protein: 0,
        fat: 0,
        carbohydrates: 0,
        calories: 0
    });
    
    const [dishes, setDishes] = useState([]);
    const [selectedDishes, setSelectedDishes] = useState([]);
    const [currentNutrients, setCurrentNutrients] = useState({
        protein: 0,
        fat: 0,
        carbohydrates: 0,
        calories: 0
    });
    
    const [currentPage, setCurrentPage] = useState('home');
    const [ingredients, setIngredients] = useState({});
    const [allIngredients, setAllIngredients] = useState({});
const [searchQuery, setSearchQuery] = useState('');
const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
    const [ingredientSearchQuery, setIngredientSearchQuery] = useState('');
    const [ingredientSortConfig, setIngredientSortConfig] = useState({ key: null, direction: 'asc' });
    const [openIngredientRow, setOpenIngredientRow] = useState(null);
    const [dishIngredients, setDishIngredients] = useState({});
    const [currentEditDishId, setCurrentEditDishId] = useState(null);
    const [editingIngredient, setEditingIngredient] = useState(null);
    const [newIngredient, setNewIngredient] = useState({
        name: '',
        proteins: 0,
        fats: 0,
        carbohydrates: 0
    });
    
    // Загрузка данных о блюдах
    useEffect(() => {
        fetch('/api/dishes')
            .then(response => response.json())
            .then(data => setDishes(data));
    }, []);
    
    // Загрузка целевых значений
    useEffect(() => {
        fetch('/api/goals')
            .then(response => response.json())
            .then(data => setGoals(data));
    }, []);
    
    // Загрузка всех ингредиентов при переходе на страницу
    useEffect(() => {
        if (currentPage === 'ingredients') {
            fetch('/api/ingredients')
                .then(response => response.json())
                .then(data => {
                    // Проверяем, является ли ответ массивом
                    if (Array.isArray(data)) {
                        // Преобразуем массив ингредиентов в объект с названиями в качестве ключей
                        // И извлекаем данные о питательных веществах на верхний уровень
                        const ingredientsMap = data.reduce((acc, item) => {
                            acc[item.name] = {
                                calories: item.nutrition.calories,
                                proteins: item.nutrition.proteins,
                                fats: item.nutrition.fats,
                                carbohydrates: item.nutrition.carbohydrates
                            };
                            return acc;
                        }, {});
                        setAllIngredients(ingredientsMap);
                    } else {
                        // Если ответ уже объект, проверяем структуру и преобразуем при необходимости
                        const ingredientsMap = {};
                        Object.entries(data).forEach(([name, item]) => {
                            if (item.nutrition) {
                                ingredientsMap[name] = {
                                    calories: item.nutrition.calories,
                                    proteins: item.nutrition.proteins,
                                    fats: item.nutrition.fats,
                                    carbohydrates: item.nutrition.carbohydrates
                                };
                            } else {
                                ingredientsMap[name] = item;
                            }
                        });
                        setAllIngredients(ingredientsMap);
                    }
                })
                .catch(error => {
                    console.error('Ошибка загрузки ингредиентов:', error);
                    setAllIngredients({});
                });
        }
    }, [currentPage]);
    
    // Функция для получения цвета ячейки в зависимости от значения
    const getPercentageCellClass = (value) => {
        if (value < 20) return 'bg-success-subtle';
        if (value < 40) return 'bg-info-subtle';
        if (value < 60) return 'bg-warning-subtle';
        if (value < 80) return 'bg-danger-subtle';
        return 'bg-danger';
    };
    
    // Функция для переключения отображения ингредиентов
    const toggleIngredientRow = async (id) => {
        if (openIngredientRow === id) {
            setOpenIngredientRow(null);
        } else {
            setOpenIngredientRow(id);
            // Если ингредиенты для этого блюда еще не загружены
            if (!dishIngredients[id]) {
                try {
                    const response = await fetch(`/api/dish/${id}`);
                    const data = await response.json();
                    // Добавляем единицу измерения 'г' для всех ингредиентов
                    const ingredientsWithUnit = data.ingredients.map(ing => ({
                        ...ing,
                        unit: 'г'
                    }));
                    setDishIngredients(prev => ({
                        ...prev,
                        [id]: ingredientsWithUnit
                    }));
                } catch (error) {
                    console.error('Ошибка загрузки ингредиентов:', error);
                    setDishIngredients(prev => ({
                        ...prev,
                        [id]: []
                    }));
                }
            }
        }
    };
    
    // Подготовка данных для таблицы ингредиентов
    const ingredientsArray = React.useMemo(() => {
        return Object.entries(allIngredients).map(([name, data]) => ({
            name,
            ...data
        }));
    }, [allIngredients]);

    const filteredIngredients = React.useMemo(() => {
        let filtered = [...ingredientsArray];
        
        if (ingredientSearchQuery.length >= 2) {
            filtered = filtered.filter(ing => 
                ing.name.toLowerCase().includes(ingredientSearchQuery.toLowerCase())
            );
        }
        
        return filtered;
    }, [ingredientsArray, ingredientSearchQuery]);

    const sortedIngredients = React.useMemo(() => {
        let sorted = [...filteredIngredients];
        
        if (ingredientSortConfig.key !== null) {
            sorted.sort((a, b) => {
                let aValue = a[ingredientSortConfig.key];
                let bValue = b[ingredientSortConfig.key];
                
                if (aValue < bValue) {
                    return ingredientSortConfig.direction === 'asc' ? -1 : 1;
                }
                if (aValue > bValue) {
                    return ingredientSortConfig.direction === 'asc' ? 1 : -1;
                }
                return 0;
            });
        }
        
        return sorted;
    }, [filteredIngredients, ingredientSortConfig]);

    const requestIngredientSort = (key) => {
        let direction = 'asc';
        if (ingredientSortConfig.key === key && ingredientSortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setIngredientSortConfig({ key, direction });
    };
    
    // Расчет калорий из БЖУ
    const calculateCalories = (proteins, fats, carbohydrates) => {
        return proteins * 4 + fats * 9 + carbohydrates * 4;
    };
    
    // Обработчик добавления нового ингредиента
    const handleAddNewIngredient = () => {
        if (!newIngredient.name.trim()) {
            alert('Введите название ингредиента');
            return;
        }
        
        const calories = calculateCalories(
            newIngredient.proteins, 
            newIngredient.fats, 
            newIngredient.carbohydrates
        );
        
        const ingredientData = {
            name: newIngredient.name,
            nutrition: {
                calories,
                proteins: newIngredient.proteins,
                fats: newIngredient.fats,
                carbohydrates: newIngredient.carbohydrates
            }
        };
        
        fetch('/api/ingredients', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(ingredientData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при сохранении');
            }
            return response.json();
        })
        .then(() => {
            const updatedIngredients = {
                ...allIngredients,
                [newIngredient.name]: {
                    ...newIngredient,
                    calories
                }
            };
            setAllIngredients(updatedIngredients);
            
            // Сбрасываем форму
            setNewIngredient({
                name: '',
                proteins: 0,
                fats: 0,
                carbohydrates: 0
            });
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Не удалось сохранить ингредиент');
        });
    };
    
    // Обработчик сохранения измененного ингредиента
    const handleSaveIngredient = (ingredient) => {
        const calories = calculateCalories(
            ingredient.proteins, 
            ingredient.fats, 
            ingredient.carbohydrates
        );
        
        const ingredientData = {
            nutrition: {
                calories,
                proteins: ingredient.proteins,
                fats: ingredient.fats,
                carbohydrates: ingredient.carbohydrates
            }
        };
        
        fetch(`/api/ingredients/${encodeURIComponent(ingredient.name)}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(ingredientData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при обновлении');
            }
            return response.json();
        })
        .then(() => {
            const updatedIngredients = {
                ...allIngredients,
                [ingredient.name]: {
                    ...ingredient,
                    calories
                }
            };
            setAllIngredients(updatedIngredients);
            setEditingIngredient(null);
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Не удалось обновить ингредиент');
        });
    };
    
    // Обработчик удаления ингредиента
    const handleDeleteIngredient = (name) => {
        if (confirm(`Удалить ингредиент "${name}"?`)) {
            fetch(`/api/ingredients/${encodeURIComponent(name)}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка при удалении');
                }
                return response.json();
            })
            .then(() => {
                const {[name]: deleted, ...rest} = allIngredients;
                setAllIngredients(rest);
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Не удалось удалить ингредиент');
            });
        }
    };

// Сортировка и фильтрация данных
// Расчет распределения калорийности по макронутриентам
const calculateMacronutrientDistribution = (protein, fat, carbohydrates) => {
    // Рассчитываем калории по формуле: белки * 4 + жиры * 9 + углеводы * 4
    const proteinCalories = protein * 4;
    const fatCalories = fat * 9;
    const carbohydratesCalories = carbohydrates * 4;
    
    const totalCalories = proteinCalories + fatCalories + carbohydratesCalories;
    
    if (totalCalories === 0) {
        return { protein: 0, fat: 0, carbohydrates: 0 };
    }
    
    const proteinPercentage = (proteinCalories / totalCalories) * 100;
    const fatPercentage = (fatCalories / totalCalories) * 100;
    const carbohydratesPercentage = (carbohydratesCalories / totalCalories) * 100;
    
    return {
        protein: proteinPercentage,
        fat: fatPercentage,
        carbohydrates: carbohydratesPercentage
    };
};

const sortedDishes = React.useMemo(() => {
        let filteredItems = [...dishes];
        
        // Фильтрация по поисковому запросу (минимум 3 символа)
        if (searchQuery.length >= 3) {
            filteredItems = filteredItems.filter(dish => 
                dish.name.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }
        
        // Сортировка
        if (sortConfig.key !== null) {
            filteredItems.sort((a, b) => {
                let aValue, bValue;
                
                // Специальная обработка для процентных значений
                if (['proteinPercentage', 'fatPercentage', 'carbsPercentage'].includes(sortConfig.key)) {
                    const aDist = calculateMacronutrientDistribution(a.protein_g, a.fat_g, a.carbohydrates_g);
                    const bDist = calculateMacronutrientDistribution(b.protein_g, b.fat_g, b.carbohydrates_g);
                    
let field = sortConfig.key.replace('Percentage', '');
if (field === 'carbs') {
    field = 'carbohydrates';
}
aValue = aDist[field];
bValue = bDist[field];
                } else {
                    aValue = a[sortConfig.key];
                    bValue = b[sortConfig.key];
                }
                
                if (aValue < bValue) {
                    return sortConfig.direction === 'asc' ? -1 : 1;
                }
                if (aValue > bValue) {
                    return sortConfig.direction === 'asc' ? 1 : -1;
                }
                return 0;
            });
        }
        
        return filteredItems;
    }, [dishes, searchQuery, sortConfig]);
    
    // Обработка запроса на сортировку
    const requestSort = (key) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };
    
    // Обновление текущих значений при изменении выбранных блюд
    useEffect(() => {
        const total = selectedDishes.reduce((acc, dish) => {
            const dishObj = dishes.find(d => d.id === dish.id);
            if (dishObj) {
                const portions = dish.portions || 1;
                acc.protein += dishObj.protein_g * portions;
                acc.fat += dishObj.fat_g * portions;
                acc.carbohydrates += dishObj.carbohydrates_g * portions;
                acc.calories += dishObj.energy_kcal * portions;
            }
            return acc;
        }, { protein: 0, fat: 0, carbohydrates: 0, calories: 0 });
        
        setCurrentNutrients(total);
    }, [selectedDishes, dishes]);
    
    // Обработка установки целевых значений
    const handleSetGoals = (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const goalsData = {
            protein: parseFloat(formData.get('protein')),
            fat: parseFloat(formData.get('fat')),
            carbohydrates: parseFloat(formData.get('carbohydrates')),
            calories: parseFloat(formData.get('calories'))
        };
        
        fetch('/api/goals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(goalsData)
        })
        .then(response => response.json())
        .then(data => {
            // Обновляем состояние после успешного запроса
            setGoals(data.goals);
        });
    };
    
    // Обработка drag start для блюд
    const handleDragStart = (e, dish) => {
        e.dataTransfer.setData("dish", JSON.stringify(dish));
        e.dataTransfer.effectAllowed = "move";
    };
    
    // Обработка drag over
    const handleDragOver = (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = "move";
    };
    
    // Обработка drop в правую панель (выбранные блюда)
    const handleDropToRight = (e) => {
        e.preventDefault();
        const dishData = e.dataTransfer.getData("dish");
        if (dishData) {
            const dish = JSON.parse(dishData);
            const existing = selectedDishes.find(d => d.id === dish.id);
            if (!existing) {
                setSelectedDishes([...selectedDishes, { ...dish, portions: 1 }]);
            }
        }
    };
    
    // Обработка drop в левую панель (возврат блюда обратно к доступным)
    const handleDropToLeft = (e) => {
        e.preventDefault();
        const dishData = e.dataTransfer.getData("dish");
        if (dishData) {
            const dish = JSON.parse(dishData);
            setSelectedDishes(selectedDishes.filter(d => d.id !== dish.id));
        }
    };
    
    // Добавление блюда в список выбранных (для старого способа)
    const handleAddDish = (dish) => {
        const existing = selectedDishes.find(d => d.id === dish.id);
        if (!existing) {
            setSelectedDishes([...selectedDishes, { ...dish, portions: 1 }]);
        }
    };
    
    // Удаление блюда из списка выбранных
    const handleRemoveDish = (dishId) => {
        setSelectedDishes(selectedDishes.filter(d => d.id !== dishId));
    };
    
    // Обновление количества порций
    const handleUpdatePortions = (dishId, newPortions) => {
        setSelectedDishes(selectedDishes.map(d => 
            d.id === dishId ? { ...d, portions: newPortions } : d
        ));
    };
    
    // Генерация меню
    const handleGenerateMenu = async () => {
        try {
            const response = await fetch('/api/menu', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    dishes: selectedDishes
                })
            });
            
            const data = await response.json();
            setIngredients(data.ingredients);
            setCurrentPage('ingredients');
        } catch (error) {
            console.error('Ошибка при генерации меню:', error);
        }
    };
    
    // Расчет процента выполнения цели
    const calculateProgress = (current, goal) => {
        if (goal === 0) return 0;
        return Math.min((current / goal) * 100, 100);
    };
    
    // Получение цвета для прогресс бара
    const getProgressBarColor = (current, goal) => {
        if (goal === 0) return 'bg-secondary';
        
        const progress = calculateProgress(current, goal);
        if (progress >= 100) {
            return 'bg-success';
        } else if (progress >= 75) {
            return 'bg-info';
        } else if (progress >= 50) {
            return 'bg-warning';
        }
        return 'bg-danger';
    };
    
    
    // Расчет доли блюда в общем потреблении (учитывая порции)
    const calculateDishContribution = (dish, portions) => {
        const dishObj = dishes.find(d => d.id === dish.id);
        if (!dishObj) return { protein: 0, fat: 0, carbohydrates: 0, calories: 0 };
        
        const totalProtein = dishObj.protein_g * portions;
        const totalFat = dishObj.fat_g * portions;
        const totalCarbohydrates = dishObj.carbohydrates_g * portions;
        const totalCalories = dishObj.energy_kcal * portions;
        
        return {
            protein: totalProtein,
            fat: totalFat,
            carbohydrates: totalCarbohydrates,
            calories: totalCalories
        };
    };
    
    // Расчет процента вклада блюда в общую норму
    const calculateContributionPercentage = (dish, portions) => {
        const contribution = calculateDishContribution(dish, portions);
        
        return {
            protein: calculateProgress(contribution.protein, goals.protein),
            fat: calculateProgress(contribution.fat, goals.fat),
            carbohydrates: calculateProgress(contribution.carbohydrates, goals.carbohydrates),
            calories: calculateProgress(contribution.calories, goals.calories)
        };
    };
    
    return (
        <>
            <header className="app-header bg-light py-3">
                <div className="container">
                    <div className="d-flex justify-content-between align-items-center">
                        <h1 className="h3 mb-0">Меню приложение</h1>
                        <nav>
                            <ul className="nav">
                                <li className="nav-item">
                                    <a href="#" className="nav-link" onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}>Главная</a>
                                </li>
                                <li className="nav-item">
                                    <a href="#" className="nav-link" onClick={(e) => { e.preventDefault(); setCurrentPage('dishes'); }}>Таблица блюд</a>
                                </li>
                    <li className="nav-item">
                        <a href="/add_dish" className="nav-link">Добавить блюдо</a>
                    </li>
                    <li className="nav-item">
                        <a href="#" className="nav-link" onClick={(e) => { e.preventDefault(); setCurrentPage('ingredients'); }}>Редактор ингредиентов</a>
                    </li>
                            </ul>
                        </nav>
                    </div>
                </div>
            </header>
            <div className="container mt-4">
                {currentPage === 'home' && (
                    <>
                        <h1 className="text-center mb-4">Недельное меню</h1>
                        <div className="card mb-4">
                            <div className="card-header">
                                <h3 className="mb-0">Установить цели</h3>
                            </div>
                            <div className="card-body">
                                <form onSubmit={handleSetGoals}>
                                    <div className="row">
                                        <div className="col-md-3 mb-3">
                                            <input 
                                                type="number" 
                                                name="protein" 
                                                placeholder="Белки (г)" 
                                                className="form-control"
                                                defaultValue={goals.protein}
                                            />
                                        </div>
                                        <div className="col-md-3 mb-3">
                                            <input 
                                                type="number" 
                                                name="fat" 
                                                placeholder="Жиры (г)" 
                                                className="form-control"
                                                defaultValue={goals.fat}
                                            />
                                        </div>
                                        <div className="col-md-3 mb-3">
                                            <input 
                                                type="number" 
                                                name="carbohydrates" 
                                                placeholder="Углеводы (г)" 
                                                className="form-control"
                                                defaultValue={goals.carbohydrates}
                                            />
                                        </div>
                                        <div className="col-md-3 mb-3">
                                            <input 
                                                type="number" 
                                                name="calories" 
                                                placeholder="Калории (ккал)" 
                                                className="form-control"
                                                defaultValue={goals.calories}
                                            />
                                        </div>
                                    </div>
                                    <div className="text-center">
                                        <button type="submit" className="btn btn-success">Установить цели</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        
                        <div className="card mb-4">
                            <div className="card-header">
                                <h3 className="mb-0">Текущие значения</h3>
                            </div>
                            <div className="card-body">
                                <div className="row g-2">
                                    <div className="col-md-3 mb-2">
                                        <h5>Белки (г)</h5>
                                        <div className="d-flex justify-content-between mb-1">
                                            <span>{currentNutrients.protein.toFixed(1)} / {goals.protein}</span>
                                            <span>{calculateProgress(currentNutrients.protein, goals.protein).toFixed(1)}%</span>
                                        </div>
                                        <div className="progress">
                                            <div 
                                                className={`progress-bar ${getProgressBarColor(currentNutrients.protein, goals.protein)}`}
                                                role="progressbar"
                                                style={{ width: `${calculateProgress(currentNutrients.protein, goals.protein)}%` }}
                                                aria-valuenow={currentNutrients.protein}
                                                aria-valuemin="0"
                                                aria-valuemax={goals.protein}
                                            >
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div className="col-md-3 mb-2">
                                        <h5>Жиры (г)</h5>
                                        <div className="d-flex justify-content-between mb-1">
                                            <span>{currentNutrients.fat.toFixed(1)} / {goals.fat}</span>
                                            <span>{calculateProgress(currentNutrients.fat, goals.fat).toFixed(1)}%</span>
                                        </div>
                                        <div className="progress">
                                            <div 
                                                className={`progress-bar ${getProgressBarColor(currentNutrients.fat, goals.fat)}`}
                                                role="progressbar"
                                                style={{ width: `${calculateProgress(currentNutrients.fat, goals.fat)}%` }}
                                                aria-valuenow={currentNutrients.fat}
                                                aria-valuemin="0"
                                                aria-valuemax={goals.fat}
                                            >
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div className="col-md-3 mb-2">
                                        <h5>Углеводы (г)</h5>
                                        <div className="d-flex justify-content-between mb-1">
                                            <span>{currentNutrients.carbohydrates.toFixed(1)} / {goals.carbohydrates}</span>
                                            <span>{calculateProgress(currentNutrients.carbohydrates, goals.carbohydrates).toFixed(1)}%</span>
                                        </div>
                                        <div className="progress">
                                            <div 
                                                className={`progress-bar ${getProgressBarColor(currentNutrients.carbohydrates, goals.carbohydrates)}`}
                                                role="progressbar"
                                                style={{ width: `${calculateProgress(currentNutrients.carbohydrates, goals.carbohydrates)}%` }}
                                                aria-valuenow={currentNutrients.carbohydrates}
                                                aria-valuemin="0"
                                                aria-valuemax={goals.carbohydrates}
                                            >
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div className="col-md-3 mb-2">
                                        <h5>Калории (ккал)</h5>
                                        <div className="d-flex justify-content-between mb-1">
                                            <span>{currentNutrients.calories.toFixed(1)} / {goals.calories}</span>
                                            <span>{calculateProgress(currentNutrients.calories, goals.calories).toFixed(1)}%</span>
                                        </div>
                                        <div className="progress">
                                            <div 
                                                className={`progress-bar ${getProgressBarColor(currentNutrients.calories, goals.calories)}`}
                                                role="progressbar"
                                                style={{ width: `${calculateProgress(currentNutrients.calories, goals.calories)}%` }}
                                                aria-valuenow={currentNutrients.calories}
                                                aria-valuemin="0"
                                                aria-valuemax={goals.calories}
                                            >
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div className="row">
                            <div 
                                className="col-md-6 mb-4"
                                onDragOver={handleDragOver}
                                onDrop={handleDropToRight}
                            >
                                <div className="card h-100">
                                    <div className="card-header">
                                        <h3 className="mb-0">Доступные блюда</h3>
                                    </div>
                                    <div className="card-body">
                                        {dishes.length === 0 ? (
                                            <p>Загрузка блюд...</p>
                                        ) : (
                                            <div className="row">
                                                {dishes.map(dish => {
                                                    const distribution = calculateMacronutrientDistribution(
                                                        dish.protein_g,
                                                        dish.fat_g,
                                                        dish.carbohydrates_g
                                                    );
                                                    
                                                    return (
                                                        <div key={dish.id} className="col-md-12 mb-3">
                                                            <div 
                                                                className="card h-100 draggable card-with-button"
                                                                draggable={true}
                                                                onDragStart={(e) => handleDragStart(e, dish)}
                                                            >
      <div className="card-body card-content">
        <h5 className="card-title">
          {dish.name} {dish.weight_g ? (<small className="dish-weight">({dish.weight_g} г)</small>) : ''}
        </h5>
        <div className="button-group">
<button 
  className="edit-button"
  onClick={() => {
    window.location.href = `/edit_dish/${dish.id}`;
  }}
>
  Редактировать
</button>
          <button 
            className="add-button"
            onClick={() => handleAddDish(dish)}
          >
            Добавить
          </button>
        </div>
        <p className="card-text">
          <strong>КБЖУ:</strong> <strong>{dish.energy_kcal}</strong> ккал, {dish.protein_g} г, {dish.fat_g} г, {dish.carbohydrates_g} г<br/>
        </p>
        <div className="mt-2">
          <div className="d-flex" style={{ height: '20px' }}>
            <div 
              className="bg-primary" 
              style={{ 
                width: `${distribution.protein}%`,
                height: '50%',
                borderTopLeftRadius: '4px',
                borderBottomLeftRadius: '4px'
              }}
              title={`Белки: ${distribution.protein.toFixed(1)}%`}
            ></div>
            <div 
              className="bg-danger" 
              style={{ 
                width: `${distribution.fat}%`,
                height: '50%'
              }}
              title={`Жиры: ${distribution.fat.toFixed(1)}%`}
            ></div>
            <div 
              className="bg-warning" 
              style={{ 
                width: `${distribution.carbohydrates}%`,
                height: '50%',
                borderTopRightRadius: '4px',
                borderBottomRightRadius: '4px'
              }}
              title={`Углеводы: ${distribution.carbohydrates.toFixed(1)}%`}
            ></div>
          </div>
        </div>
      </div>
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                            
                            <div 
                                className="col-md-6 mb-4"
                                onDragOver={handleDragOver}
                                onDrop={handleDropToLeft}
                            >
                                <div className="card h-100">
                                    <div className="card-header">
                                        <h3 className="mb-0">Выбранные блюда</h3>
                                    </div>
                                    <div className="card-body">
                                        {selectedDishes.length === 0 ? (
                                            <p>Нет выбранных блюд</p>
                                        ) : (
                                            <div className="row">
                                                {selectedDishes.map(dish => {
                                                    const contribution = calculateContributionPercentage(dish, dish.portions || 1);
                                                    
                                                    return (
                                                        <div key={dish.id} className="col-md-12 mb-3">
                                                            <div className="card h-100">
                                                                <div className="card-body">
                                                                    <div className="d-flex justify-content-between align-items-center mb-2">
                                                                        <h5 className="card-title mb-0">{dish.name}</h5>
                                                                        <div className="d-flex align-items-center">
                                                                            <button 
                                                                                className="btn btn-outline-secondary btn-sm me-1"
                                                                                onClick={() => {
                                                                                    const newPortions = Math.max(1, dish.portions - 1);
                                                                                    handleUpdatePortions(dish.id, newPortions);
                                                                                }}
                                                                            >
                                                                                -
                                                                            </button>
                                                                            <input 
                                                                                type="number" 
                                                                                className="form-control text-center mx-1"
                                                                                style={{ width: '60px' }}
                                                                                value={dish.portions || 1}
                                                                                onChange={(e) => {
                                                                                    const newPortions = Math.max(1, parseInt(e.target.value) || 1);
                                                                                    handleUpdatePortions(dish.id, newPortions);
                                                                                }}
                                                                                min="1"
                                                                            />
                                                                            <button 
                                                                                className="btn btn-outline-secondary btn-sm ms-1"
                                                                                onClick={() => {
                                                                                    const newPortions = (dish.portions || 1) + 1;
                                                                                    handleUpdatePortions(dish.id, newPortions);
                                                                                }}
                                                                            >
                                                                                +
                                                                            </button>
                                                                            <button 
                                                                                className="btn btn-danger btn-sm ms-2"
                                                                                onClick={() => handleRemoveDish(dish.id)}
                                                                            >
                                                                                Удалить
                                                                            </button>
                                                                        </div>
                                                                    </div>
                                                                    
                                                                    <div className="mt-2">
                                                                        <div className="row g-1">
                                                                            <div className="col-12 mb-1">
                                                                                <div className="d-flex justify-content-between small">
                                                                                    <span>Белки:</span>
                                                                                    <span>{contribution.protein.toFixed(1)}%</span>
                                                                                </div>
                                                                                <div className="progress" style={{ height: '12px' }}>
                                                                                    <div 
                                                                                        className={`progress-bar ${getProgressBarColor(
                                                                                            calculateDishContribution(dish, dish.portions || 1).protein,
                                                                                            goals.protein
                                                                                        )}`}
                                                                                        role="progressbar"
                                                                                        style={{ width: `${contribution.protein}%` }}
                                                                                        aria-valuenow={calculateDishContribution(dish, dish.portions || 1).protein}
                                                                                        aria-valuemin="0"
                                                                                        aria-valuemax={goals.protein}
                                                                                    >
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                            <div className="col-12 mb-1">
                                                                                <div className="d-flex justify-content-between small">
                                                                                    <span>Жиры:</span>
                                                                                    <span>{contribution.fat.toFixed(1)}%</span>
                                                                                </div>
                                                                                <div className="progress" style={{ height: '12px' }}>
                                                                                    <div 
                                                                                        className={`progress-bar ${getProgressBarColor(
                                                                                            calculateDishContribution(dish, dish.portions || 1).fat,
                                                                                            goals.fat
                                                                                        )}`}
                                                                                        role="progressbar"
                                                                                        style={{ width: `${contribution.fat}%` }}
                                                                                        aria-valuenow={calculateDishContribution(dish, dish.portions || 1).fat}
                                                                                        aria-valuemin="0"
                                                                                        aria-valuemax={goals.fat}
                                                                                    >
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                            <div className="col-12 mb-1">
                                                                                <div className="d-flex justify-content-between small">
                                                                                    <span>Углеводы:</span>
                                                                                    <span>{contribution.carbohydrates.toFixed(1)}%</span>
                                                                                </div>
                                                                                <div className="progress" style={{ height: '12px' }}>
                                                                                    <div 
                                                                                        className={`progress-bar ${getProgressBarColor(
                                                                                            calculateDishContribution(dish, dish.portions || 1).carbohydrates,
                                                                                            goals.carbohydrates
                                                                                        )}`}
                                                                                        role="progressbar"
                                                                                        style={{ width: `${contribution.carbohydrates}%` }}
                                                                                        aria-valuenow={calculateDishContribution(dish, dish.portions || 1).carbohydrates}
                                                                                        aria-valuemin="0"
                                                                                        aria-valuemax={goals.carbohydrates}
                                                                                    >
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                            <div className="col-12">
                                                                                <div className="d-flex justify-content-between small">
                                                                                    <span>Калории:</span>
                                                                                    <span>{contribution.calories.toFixed(1)}%</span>
                                                                                </div>
                                                                                <div className="progress" style={{ height: '12px' }}>
                                                                                    <div 
                                                                                        className={`progress-bar ${getProgressBarColor(
                                                                                            calculateDishContribution(dish, dish.portions || 1).calories,
                                                                                            goals.calories
                                                                                        )}`}
                                                                                        role="progressbar"
                                                                                        style={{ width: `${contribution.calories}%` }}
                                                                                        aria-valuenow={calculateDishContribution(dish, dish.portions || 1).calories}
                                                                                        aria-valuemin="0"
                                                                                        aria-valuemax={goals.calories}
                                                                                    >
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        )}
                                    </div>
                                    <div className="card-footer text-center">
                                        <button 
                                            className="btn btn-primary"
                                            onClick={handleGenerateMenu}
                                            disabled={selectedDishes.length === 0}
                                        >
                                            Готово
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </>
                )}

                {currentPage === 'dishes' && (
                    <div className="card">
                        <div className="card-body">
                            <h3 className="card-title">Таблица блюд</h3>
                            <div className="mb-3">
                                <input 
                                    type="text" 
                                    className="form-control" 
                                    placeholder="Поиск блюд (минимум 3 символа)..." 
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                />
                                {searchQuery && searchQuery.length < 3 && (
                                    <small className="text-muted">Введите минимум 3 символа для поиска</small>
                                )}
                            </div>
                            <div className="table-responsive">
                                <table className="table table-striped table-hover">
                                    <thead>
                                        <tr>
                                            <th onClick={() => requestSort('name')} style={{ cursor: 'pointer' }}>
                                                Название {sortConfig.key === 'name' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('weight')} style={{ cursor: 'pointer' }}>
                                                Вес {sortConfig.key === 'weight' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('energy_kcal')} style={{ cursor: 'pointer' }}>
                                                Калории {sortConfig.key === 'energy_kcal' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('protein_g')} style={{ cursor: 'pointer' }}>
                                                Белки {sortConfig.key === 'protein_g' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('fat_g')} style={{ cursor: 'pointer' }}>
                                                Жиры {sortConfig.key === 'fat_g' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('carbohydrates_g')} style={{ cursor: 'pointer' }}>
                                                Углеводы {sortConfig.key === 'carbohydrates_g' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('proteinPercentage')} style={{ cursor: 'pointer' }}>
                                                % белков {sortConfig.key === 'proteinPercentage' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('fatPercentage')} style={{ cursor: 'pointer' }}>
                                                % жиров {sortConfig.key === 'fatPercentage' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th onClick={() => requestSort('carbsPercentage')} style={{ cursor: 'pointer' }}>
                                                % углеводов {sortConfig.key === 'carbsPercentage' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                                            </th>
                                            <th>Распределение</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {sortedDishes.map(dish => {
                                            const distribution = calculateMacronutrientDistribution(
                                                dish.protein_g,
                                                dish.fat_g,
                                                dish.carbohydrates_g
                                            );
                                            
                                            return (
                                                <React.Fragment key={dish.id}>
                                                    <tr>
                                                        <td>
                                                            {dish.name}
                                                            <span 
                                                                className="ms-2 cursor-pointer" 
                                                                onClick={() => toggleIngredientRow(dish.id)}
                                                                style={{ userSelect: 'none' }}
                                                            >
                                                                {openIngredientRow === dish.id ? '▲' : '▼'}
                                                            </span>
                                                        </td>
                                                        <td>{dish.weight_g ? `${dish.weight_g} г` : '-'}</td>
                                                        <td>{dish.energy_kcal} ккал</td>
                                                        <td>{dish.protein_g} г</td>
                                                        <td>{dish.fat_g} г</td>
                                                        <td>{dish.carbohydrates_g} г</td>
                                                        <td className={getPercentageCellClass(distribution.protein)}>
                                                            {distribution.protein.toFixed(1)}%
                                                        </td>
                                                        <td className={getPercentageCellClass(distribution.fat)}>
                                                            {distribution.fat.toFixed(1)}%
                                                        </td>
                                                        <td className={getPercentageCellClass(distribution.carbohydrates)}>
                                                            {distribution.carbohydrates.toFixed(1)}%
                                                        </td>
                                                        <td>
                                                            <div className="d-flex" style={{ height: '10px', borderRadius: '2px', overflow: 'hidden' }}>
                                                                <div 
                                                                    className="bg-primary" 
                                                                    style={{ width: `${distribution.protein}%` }}
                                                                    title={`Белки: ${distribution.protein.toFixed(1)}%`}
                                                                ></div>
                                                                <div 
                                                                    className="bg-danger" 
                                                                    style={{ width: `${distribution.fat}%` }}
                                                                    title={`Жиры: ${distribution.fat.toFixed(1)}%`}
                                                                ></div>
                                                                <div 
                                                                    className="bg-warning" 
                                                                    style={{ width: `${distribution.carbohydrates}%` }}
                                                                    title={`Углеводы: ${distribution.carbohydrates.toFixed(1)}%`}
                                                                ></div>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                            {openIngredientRow === dish.id && (
                                                                <tr>
                                                                    <td colSpan="10" className="bg-light p-3">
                                                                        <h6>Ингредиенты:</h6>
{dishIngredients[dish.id] ? (
    dishIngredients[dish.id].length > 0 ? (
        <ul className="mb-0">
            {dishIngredients[dish.id].map((ing, index) => (
                <li key={index}>
                    {ing.name}: {ing.amount} {ing.unit} 
                    ({ing.calories} ккал, {ing.proteins} г белков, {ing.fats} г жиров, {ing.carbohydrates} г углеводов)
                </li>
            ))}
        </ul>
    ) : (
        <p className="mb-0 text-muted">Ингредиенты не указаны</p>
    )
) : (
    <p className="mb-0 text-muted">Загрузка ингредиентов...</p>
)}
                                                                    </td>
                                                                </tr>
                                                            )}
                                                </React.Fragment>
                                            );
                                        })}
                                    </tbody>
                                </table>
                                {sortedDishes.length === 0 && (
                                    <p className="text-center text-muted">Блюда не найдены</p>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {currentPage === 'add-dish' && (
                    <div className="card">
                        <div className="card-body">
                            <h3 className="card-title">Добавить новое блюдо</h3>
                            <form>
                                <div className="mb-3">
                                    <label className="form-label">Название блюда</label>
                                    <input type="text" className="form-control" />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Ингредиенты</label>
                                    <div className="input-group mb-2">
                                        <input type="text" className="form-control" placeholder="Ингредиент" />
                                        <input type="number" className="form-control" placeholder="Количество (г)" />
                                        <button className="btn btn-outline-secondary" type="button">+</button>
                                    </div>
                                </div>
                                <button type="submit" className="btn btn-primary">Сохранить</button>
                            </form>
                        </div>
                    </div>
                )}

{currentPage === 'ingredients' && (
    <div className="card">
        <div className="card-body">
            <h3 className="card-title">Список ингредиентов</h3>
            <div className="mb-3">
                <input 
                    type="text" 
                    className="form-control" 
                    placeholder="Поиск по названию (минимум 2 символа)..." 
                    value={ingredientSearchQuery}
                    onChange={(e) => setIngredientSearchQuery(e.target.value)}
                />
                {ingredientSearchQuery && ingredientSearchQuery.length < 2 && (
                    <small className="text-muted">Введите минимум 2 символа для поиска</small>
                )}
            </div>
            <div className="table-responsive">
                <table className="table table-striped table-hover">
                    <thead>
                        <tr className="align-middle">
                            <th onClick={() => requestIngredientSort('name')} style={{ cursor: 'pointer', width: '25%' }}>
                                Название {ingredientSortConfig.key === 'name' && (ingredientSortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th onClick={() => requestIngredientSort('calories')} style={{ cursor: 'pointer', width: '15%' }}>
                                Калории {ingredientSortConfig.key === 'calories' && (ingredientSortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th onClick={() => requestIngredientSort('proteins')} style={{ cursor: 'pointer', width: '15%' }}>
                                Белки {ingredientSortConfig.key === 'proteins' && (ingredientSortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th onClick={() => requestIngredientSort('fats')} style={{ cursor: 'pointer', width: '15%' }}>
                                Жиры {ingredientSortConfig.key === 'fats' && (ingredientSortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th onClick={() => requestIngredientSort('carbohydrates')} style={{ cursor: 'pointer', width: '15%' }}>
                                Углеводы {ingredientSortConfig.key === 'carbohydrates' && (ingredientSortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th style={{ width: '15%' }}>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        {/* Форма для добавления нового ингредиента */}
                        <tr className="new-ingredient-row align-middle">
                            <td>
                                <input 
                                    type="text" 
                                    className="form-control form-control-sm" 
                                    value={newIngredient.name}
                                    onChange={(e) => setNewIngredient({...newIngredient, name: e.target.value})}
                                    placeholder="Название"
                                    autoFocus
                                />
                            </td>
                            <td>
                                {calculateCalories(newIngredient.proteins, newIngredient.fats, newIngredient.carbohydrates).toFixed(1)} ккал
                            </td>
                            <td>
                                <input 
                                    type="number" 
                                    className="form-control form-control-sm" 
                                    value={newIngredient.proteins}
                                    onChange={(e) => {
                                        const proteins = parseFloat(e.target.value) || 0;
                                        setNewIngredient({
                                            ...newIngredient,
                                            proteins
                                        });
                                    }}
                                    step="0.1"
                                    min="0"
                                />
                            </td>
                            <td>
                                <input 
                                    type="number" 
                                    className="form-control form-control-sm" 
                                    value={newIngredient.fats}
                                    onChange={(e) => {
                                        const fats = parseFloat(e.target.value) || 0;
                                        setNewIngredient({
                                            ...newIngredient,
                                            fats
                                        });
                                    }}
                                    step="0.1"
                                    min="0"
                                />
                            </td>
                            <td>
                                <input 
                                    type="number" 
                                    className="form-control form-control-sm" 
                                    value={newIngredient.carbohydrates}
                                    onChange={(e) => {
                                        const carbs = parseFloat(e.target.value) || 0;
                                        setNewIngredient({
                                            ...newIngredient,
                                            carbohydrates: carbs
                                        });
                                    }}
                                    step="0.1"
                                    min="0"
                                />
                            </td>
                            <td>
                                <button 
                                    className="btn btn-success btn-sm w-100"
                                    onClick={handleAddNewIngredient}
                                >
                                    Добавить
                                </button>
                            </td>
                        </tr>

                        {sortedIngredients.map((ing, index) => {
                            if (editingIngredient && editingIngredient.name === ing.name) {
                                return (
                                    <tr key={index} className="editing-row align-middle">
                                        <td>
                                            <input 
                                                type="text" 
                                                className="form-control form-control-sm" 
                                                value={editingIngredient.name}
                                                onChange={(e) => setEditingIngredient({...editingIngredient, name: e.target.value})}
                                            />
                                        </td>
                                        <td>
                                            {calculateCalories(
                                                editingIngredient.proteins, 
                                                editingIngredient.fats, 
                                                editingIngredient.carbohydrates
                                            ).toFixed(1)} ккал
                                        </td>
                                        <td>
                                            <input 
                                                type="number" 
                                                className="form-control form-control-sm" 
                                                value={editingIngredient.proteins}
                                                onChange={(e) => {
                                                    const proteins = parseFloat(e.target.value) || 0;
                                                    setEditingIngredient({
                                                        ...editingIngredient,
                                                        proteins
                                                    });
                                                }}
                                                step="0.1"
                                                min="0"
                                            />
                                        </td>
                                        <td>
                                            <input 
                                                type="number" 
                                                className="form-control form-control-sm" 
                                                value={editingIngredient.fats}
                                                onChange={(e) => {
                                                    const fats = parseFloat(e.target.value) || 0;
                                                    setEditingIngredient({
                                                        ...editingIngredient,
                                                        fats
                                                    });
                                                }}
                                                step="0.1"
                                                min="0"
                                            />
                                        </td>
                                        <td>
                                            <input 
                                                type="number" 
                                                className="form-control form-control-sm" 
                                                value={editingIngredient.carbohydrates}
                                                onChange={(e) => {
                                                    const carbs = parseFloat(e.target.value) || 0;
                                                    setEditingIngredient({
                                                        ...editingIngredient,
                                                        carbohydrates: carbs
                                                    });
                                                }}
                                                step="0.1"
                                                min="0"
                                            />
                                        </td>
                                        <td>
                                            <div className="d-flex gap-1">
                                                <button 
                                                    className="btn btn-success btn-sm flex-fill"
                                                    onClick={() => handleSaveIngredient(editingIngredient)}
                                                >
                                                    Сохранить
                                                </button>
                                                <button 
                                                    className="btn btn-secondary btn-sm flex-fill"
                                                    onClick={() => setEditingIngredient(null)}
                                                >
                                                    Отмена
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                );
                            }
                            
                            return (
                                <tr key={index} className="align-middle">
                                    <td>{ing.name}</td>
                                    <td>{ing.calories.toFixed(1)} ккал</td>
                                    <td>{ing.proteins.toFixed(1)} г</td>
                                    <td>{ing.fats.toFixed(1)} г</td>
                                    <td>{ing.carbohydrates.toFixed(1)} г</td>
                                    <td>
                                        <div className="d-flex gap-1">
                                            <button 
                                                className="btn btn-primary btn-sm flex-fill"
                                                onClick={() => setEditingIngredient(ing)}
                                            >
                                                Редактировать
                                            </button>
                                            <button 
                                                className="btn btn-danger btn-sm flex-fill"
                                                onClick={() => handleDeleteIngredient(ing.name)}
                                            >
                                                Удалить
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
                {sortedIngredients.length === 0 && (
                    <p className="text-center text-muted">Ингредиенты не найдены</p>
                )}
            </div>
        </div>
    </div>
)}
            </div>
        </>
    );
};

// Рендерим приложение
render(<App />, document.getElementById('root'));
