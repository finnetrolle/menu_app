document.addEventListener('DOMContentLoaded', function() {
    let chart = null;
    let currentIngredients = [];

    // Инициализация поиска ингредиентов
    const searchInput = document.getElementById('ingredient-search');
    const searchResults = document.getElementById('search-results');

    function debounce(func, delay) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    function renderSearchResults(ingredients) {
        searchResults.innerHTML = '';
        if (ingredients.length === 0) return;
        
        const ul = document.createElement('ul');
        ul.className = 'search-results-list';
        
        ingredients.forEach(ing => {
            const li = document.createElement('li');
            li.className = 'search-result-item';
            li.textContent = ing.name;
            li.dataset.id = ing.id;
            li.addEventListener('click', () => addIngredient(ing));
            ul.appendChild(li);
        });
        
        searchResults.appendChild(ul);
    }

    function addIngredient(ingredient) {
        if (currentIngredients.some(ing => ing.name === ingredient.name)) {
            alert('Этот ингредиент уже добавлен в блюдо');
            return;
        }
        
        // Рассчитываем КБЖУ для 100г
        const baseNutrition = ingredient.nutrition;
        const amount = 100;
        const calories = baseNutrition.calories * amount / 100;
        const proteins = baseNutrition.proteins * amount / 100;
        const fats = baseNutrition.fats * amount / 100;
        const carbohydrates = baseNutrition.carbohydrates * amount / 100;
        
        const newIngredient = {
            name: ingredient.name,
            amount: amount,
            calories: calories,
            proteins: proteins,
            fats: fats,
            carbohydrates: carbohydrates
        };
        
        currentIngredients.push(newIngredient);
        renderIngredientsTable(currentIngredients);
        updateDishStats();
        updateChart();
        colorizeNutritionTable();
        
        searchInput.value = '';
        searchResults.innerHTML = '';
    }

    searchInput.addEventListener('input', debounce(async function() {
        const query = this.value.trim();
        if (query.length < 2) {
            searchResults.innerHTML = '';
            return;
        }

        try {
            const response = await fetch('/api/ingredients');
            if (!response.ok) throw new Error('Ошибка загрузки ингредиентов');
            const ingredients = await response.json();
            
            const filtered = ingredients.filter(ing => 
                ing.name.toLowerCase().includes(query.toLowerCase())
            );
            
            renderSearchResults(filtered);
        } catch (error) {
            console.error('Ошибка поиска:', error);
        }
    }, 300));

    // Инициализация пустого состояния
    renderIngredientsTable(currentIngredients);
    colorizeNutritionTable();
    updateDishStats();
    initChart();

    function renderIngredientsTable(ingredients) {
        const tbody = document.getElementById('ingredients-table-body');
        tbody.innerHTML = '';
        
        ingredients.forEach(ingredient => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${ingredient.name}</td>
                <td><input type="number" class="ingredient-weight" data-name="${ingredient.name}" 
                          value="${ingredient.amount}" min="0" step="1" style="width: 80px"></td>
                <td>${ingredient.calories.toFixed(1)}</td>
                <td>${ingredient.proteins.toFixed(1)}</td>
                <td>${ingredient.fats.toFixed(1)}</td>
                <td>${ingredient.carbohydrates.toFixed(1)}</td>
                <td><button class="remove-btn delete-ingredient" data-name="${ingredient.name}">Удалить</button></td>
            `;
            tbody.appendChild(row);
            
            // Обработчик удаления ингредиента
            const deleteButton = row.querySelector('.delete-ingredient');
            if (deleteButton) {
                deleteButton.addEventListener('click', function() {
                    const name = this.dataset.name;
                    currentIngredients = currentIngredients.filter(ing => ing.name !== name);
                    renderIngredientsTable(currentIngredients);
                    updateDishStats();
                    updateChart();
                    colorizeNutritionTable();
                });
            }
        });

        // Добавляем обработчики изменений
        document.querySelectorAll('.ingredient-weight').forEach(input => {
            input.addEventListener('input', function() {
                const name = this.dataset.name;
                const newAmount = parseFloat(this.value) || 0;
                
                // Находим старое значение amount
                const oldIngredient = currentIngredients.find(ing => ing.name === name);
                if (!oldIngredient) return;
                const oldAmount = oldIngredient.amount;
                
                // Вычисляем коэффициент, избегая деления на ноль
                const ratio = oldAmount > 0 ? newAmount / oldAmount : 1;
                
                // Обновляем данные с пересчетом показателей
                currentIngredients = currentIngredients.map(ing => {
                    if (ing.name === name) {
                        return {
                            ...ing,
                            amount: newAmount,
                            calories: ing.calories * ratio,
                            proteins: ing.proteins * ratio,
                            fats: ing.fats * ratio,
                            carbohydrates: ing.carbohydrates * ratio
                        };
                    }
                    return ing;
                });
                
                updateDishStats();
                updateChart();
                colorizeNutritionTable();
                updateIngredientRow(name);
            });
        });
    }

    function calculateNutrition() {
        let total = {
            weight: 0,
            calories: 0,
            proteins: 0,
            fats: 0,
            carbohydrates: 0
        };

        currentIngredients.forEach(ing => {
            total.weight += ing.amount;
            total.calories += ing.calories;
            total.proteins += ing.proteins;
            total.fats += ing.fats;
            total.carbohydrates += ing.carbohydrates;
        });

        return total;
    }

    function updateDishStats() {
        const nutrition = calculateNutrition();
        
        document.getElementById('total-weight').textContent = `${nutrition.weight.toFixed(1)} г`;
        document.getElementById('total-calories').textContent = `${nutrition.calories.toFixed(1)} ккал`;
        document.getElementById('total-proteins').textContent = `${nutrition.proteins.toFixed(1)} г`;
        document.getElementById('total-fats').textContent = `${nutrition.fats.toFixed(1)} г`;
        document.getElementById('total-carbs').textContent = `${nutrition.carbohydrates.toFixed(1)} г`;
    }

    function initChart() {
        const ctx = document.getElementById('nutrition-chart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Белки', 'Жиры', 'Углеводы'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        updateChart();
    }

    function updateChart() {
        const nutrition = calculateNutrition();
        
        // Рассчитываем калорийный вклад
        const proteinCalories = nutrition.proteins * 4;
        const fatCalories = nutrition.fats * 9;
        const carbCalories = nutrition.carbohydrates * 4;
        const totalCalories = proteinCalories + fatCalories + carbCalories;
        
        // Рассчитываем проценты
        const proteinPercent = totalCalories ? (proteinCalories / totalCalories) * 100 : 0;
        const fatPercent = totalCalories ? (fatCalories / totalCalories) * 100 : 0;
        const carbPercent = totalCalories ? (carbCalories / totalCalories) * 100 : 0;
        
        chart.data.datasets[0].data = [
            proteinPercent,
            fatPercent,
            carbPercent
        ];
        chart.update();
    }

    function colorizeNutritionTable() {
        const table = document.getElementById('ingredients-table-body');
        if (!table) return;
        
        const rows = table.querySelectorAll('tr');
        // Индексы столбцов: Калории, Белки, Жиры, Углеводы (начиная с 0)
        const columns = [2, 3, 4, 5];
        
        columns.forEach(colIndex => {
            let max = 0;
            // Собираем значения и находим максимум
            rows.forEach(row => {
                const cell = row.cells[colIndex];
                const value = parseFloat(cell.textContent) || 0;
                if (value > max) max = value;
            });
            
            // Раскрашиваем ячейки
            if (max > 0) {
                rows.forEach(row => {
                    const cell = row.cells[colIndex];
                    const value = parseFloat(cell.textContent) || 0;
                    const intensity = value / max;
                    
                    // Плавный переход от зеленого к красному
                    const r = Math.round(255 * intensity);
                    const g = Math.round(255 * (1 - intensity));
                    cell.style.backgroundColor = `rgba(${r}, ${g}, 0, 0.3)`;
                });
            }
        });
    }

    function updateIngredientRow(name) {
        const tbody = document.getElementById('ingredients-table-body');
        const rows = tbody.querySelectorAll('tr');
        for (let row of rows) {
            const cells = row.querySelectorAll('td');
            if (cells[0].textContent === name) {
                const ingredient = currentIngredients.find(ing => ing.name === name);
                if (ingredient) {
                    cells[2].textContent = ingredient.calories.toFixed(1);
                    cells[3].textContent = ingredient.proteins.toFixed(1);
                    cells[4].textContent = ingredient.fats.toFixed(1);
                    cells[5].textContent = ingredient.carbohydrates.toFixed(1);
                }
                break;
            }
        }
    }

    // Обработчик кнопки сохранения
    document.getElementById('save-dish').addEventListener('click', function() {
        const dishNameInput = document.getElementById('dish-name');
        const dishName = dishNameInput.value.trim();
        
        if (!dishName) {
            alert('Название блюда не может быть пустым');
            dishNameInput.focus();
            return;
        }

        const updatedIngredients = currentIngredients.map(ing => ({
            name: ing.name,
            amount: ing.amount
        }));

        fetch('/api/dish/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                name: dishName,
                ingredients: updatedIngredients 
            })
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сохранения');
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                alert('Блюдо успешно добавлено!');
                window.location.href = '/';
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Не удалось добавить блюдо');
        });
    });
});
