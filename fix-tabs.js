// Исправленные функции переключения вкладок
function switchTab(tab) {
    // Убираем активный класс со всех вкладок
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Добавляем активный класс к выбранной вкладке
    const activeTab = document.querySelector(`[data-tab="${tab}"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }

    currentTab = tab;
    showTabContent(tab);
}

// Показ контента вкладки
function showTabContent(tab) {
    hideAllSections();
    
    switch(tab) {
        case 'home':
            showHomeContent();
            break;
        case 'search':
            showSearchContent();
            break;
        case 'favorites':
            showFavoritesContent();
            break;
        case 'profile':
            showProfileContent();
            break;
        default:
            console.log('Неизвестная вкладка:', tab);
            showHomeContent();
    }
}

// Скрытие всех секций
function hideAllSections() {
    const sections = [
        'main-menu', 'quick-actions', 'recent-purchases',
        'search-content', 'favorites-content', 'profile-content'
    ];
    
    sections.forEach(section => {
        const element = document.querySelector(`.${section}`);
        if (element) {
            element.style.display = 'none';
        }
    });
}

// Показ домашнего контента
function showHomeContent() {
    const mainMenu = document.querySelector('.main-menu');
    const quickActions = document.querySelector('.quick-actions');
    const recentPurchases = document.querySelector('.recent-purchases');
    
    if (mainMenu) mainMenu.style.display = 'grid';
    if (quickActions) quickActions.style.display = 'block';
    if (recentPurchases) recentPurchases.style.display = 'block';
    
    console.log('Показан домашний контент');
}

// Показ контента поиска
function showSearchContent() {
    if (!document.querySelector('.search-content')) {
        createSearchContent();
    }
    
    const searchContent = document.querySelector('.search-content');
    if (searchContent) {
        searchContent.style.display = 'block';
    }
    
    console.log('Показан контент поиска');
}

// Показ контента избранного
function showFavoritesContent() {
    if (!document.querySelector('.favorites-content')) {
        createFavoritesContent();
    }
    
    const favoritesContent = document.querySelector('.favorites-content');
    if (favoritesContent) {
        favoritesContent.style.display = 'block';
    }
    
    console.log('Показан контент избранного');
}

// Показ контента профиля
function showProfileContent() {
    if (!document.querySelector('.profile-content')) {
        createProfileContent();
    }
    
    const profileContent = document.querySelector('.profile-content');
    if (profileContent) {
        profileContent.style.display = 'block';
    }
    
    console.log('Показан контент профиля');
}

// Создание контента поиска
function createSearchContent() {
    const mainContainer = document.querySelector('.main-container');
    if (!mainContainer) return;
    
    const searchContent = document.createElement('div');
    searchContent.className = 'search-content';
    searchContent.innerHTML = `
        <div class="search-header">
            <h2>🔍 Поиск закупок</h2>
            <p>Найдите нужные закупки по ключевым словам</p>
        </div>
        
        <div class="search-form">
            <input type="text" id="searchInput" placeholder="Введите название закупки, категорию или регион...">
            <button onclick="performSearch()">Найти</button>
        </div>
        
        <div class="search-filters">
            <select id="categoryFilter">
                <option value="">Все категории</option>
                <option value="Товары">Товары</option>
                <option value="Услуги">Услуги</option>
                <option value="Работы">Работы</option>
            </select>
            
            <select id="regionFilter">
                <option value="">Все регионы</option>
                <option value="Москва">Москва</option>
                <option value="Санкт-Петербург">Санкт-Петербург</option>
                <option value="Новосибирск">Новосибирск</option>
                <option value="Краснодар">Краснодар</option>
                <option value="Екатеринбург">Екатеринбург</option>
            </select>
            
            <select id="statusFilter">
                <option value="">Все статусы</option>
                <option value="active">Активные</option>
                <option value="completed">Завершенные</option>
            </select>
        </div>
        
        <div id="searchResults" class="search-results"></div>
    `;
    
    mainContainer.appendChild(searchContent);
}

// Создание контента избранного
function createFavoritesContent() {
    const mainContainer = document.querySelector('.main-container');
    if (!mainContainer) return;
    
    const favoritesContent = document.createElement('div');
    favoritesContent.className = 'favorites-content';
    favoritesContent.innerHTML = `
        <div class="favorites-header">
            <h2>⭐ Избранные закупки</h2>
            <p>Ваши сохраненные закупки</p>
        </div>
        
        <div id="favoritesList" class="favorites-list">
            ${favorites.length === 0 ? '<p>У вас пока нет избранных закупок</p>' : ''}
        </div>
    `;
    
    mainContainer.appendChild(favoritesContent);
    updateFavoritesList();
}

// Создание контента профиля
function createProfileContent() {
    const mainContainer = document.querySelector('.main-container');
    if (!mainContainer) return;
    
    const profileContent = document.createElement('div');
    profileContent.className = 'profile-content';
    profileContent.innerHTML = `
        <div class="profile-header">
            <h2>👤 Профиль пользователя</h2>
        </div>
        
        <div class="profile-info">
            <div class="profile-section">
                <h3>📊 Статистика</h3>
                <p>Избранных закупок: ${favorites.length}</p>
                <p>Подано заявок: ${userApplications.length}</p>
                <p>Поисковых запросов: ${searchHistory.length}</p>
            </div>
            
            <div class="profile-section">
                <h3>🔔 Уведомления</h3>
                <div id="notificationsList">
                    ${notifications.length === 0 ? '<p>Новых уведомлений нет</p>' : ''}
                </div>
            </div>
            
            <div class="profile-section">
                <h3>⚙️ Настройки</h3>
                <button onclick="clearAllData()">Очистить все данные</button>
                <button onclick="exportData()">Экспорт данных</button>
            </div>
        </div>
    `;
    
    mainContainer.appendChild(profileContent);
}

// Обновление списка избранного
function updateFavoritesList() {
    const favoritesList = document.getElementById('favoritesList');
    if (!favoritesList) return;
    
    if (favorites.length === 0) {
        favoritesList.innerHTML = '<p>У вас пока нет избранных закупок</p>';
        return;
    }
    
    let html = '';
    favorites.forEach(favoriteId => {
        const purchase = mockPurchases.find(p => p.id === favoriteId);
        if (purchase) {
            html += `
                <div class="favorite-item">
                    <h4>${purchase.title}</h4>
                    <p>${purchase.category} • ${purchase.region}</p>
                    <p>Цена: ${purchase.price.toLocaleString()} ₽</p>
                    <button onclick="removeFromFavorites(${purchase.id})">Убрать из избранного</button>
                </div>
            `;
        }
    });
    
    favoritesList.innerHTML = html;
}

// Выполнение поиска
function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    const category = document.getElementById('categoryFilter').value;
    const region = document.getElementById('regionFilter').value;
    const status = document.getElementById('statusFilter').value;
    
    if (!query && !category && !region && !status) {
        alert('Введите поисковый запрос или выберите фильтры');
        return;
    }
    
    const filters = {};
    if (category) filters.category = category;
    if (region) filters.region = region;
    if (status) filters.status = status;
    
    const results = searchPurchases(query, filters);
    displaySearchResults(results, query, filters);
}

// Отображение результатов поиска
function displaySearchResults(results, query, filters) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results">
                <h3>По вашему запросу ничего не найдено</h3>
                <p>Попробуйте изменить параметры поиска</p>
            </div>
        `;
        return;
    }
    
    let html = `<h3>Найдено ${results.length} результатов</h3>`;
    
    results.forEach(purchase => {
        html += `
            <div class="search-result-item">
                <h4>${purchase.title}</h4>
                <p>${purchase.category} • ${purchase.region}</p>
                <p>Цена: ${purchase.price.toLocaleString()} ₽</p>
                <p>Статус: ${purchase.status === 'active' ? 'Активна' : 'Завершена'}</p>
                <div class="result-actions">
                    <button onclick="addToFavorites(${purchase.id})">⭐ В избранное</button>
                    <button onclick="submitApplication(${purchase.id})">📝 Подать заявку</button>
                </div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// Добавление в избранное
function addToFavorites(purchaseId) {
    if (!favorites.includes(purchaseId)) {
        favorites.push(purchaseId);
        localStorage.setItem('zakupkiFavorites', JSON.stringify(favorites));
        updateFavoritesList();
        alert('Закупка добавлена в избранное!');
    } else {
        alert('Закупка уже в избранном!');
    }
}

// Удаление из избранного
function removeFromFavorites(purchaseId) {
    const index = favorites.indexOf(purchaseId);
    if (index > -1) {
        favorites.splice(index, 1);
        localStorage.setItem('zakupkiFavorites', JSON.stringify(favorites));
        updateFavoritesList();
        alert('Закупка удалена из избранного!');
    }
}

// Подача заявки
function submitApplication(purchaseId) {
    if (!userApplications.includes(purchaseId)) {
        userApplications.push(purchaseId);
        localStorage.setItem('zakupkiApplications', JSON.stringify(userApplications));
        alert('Заявка подана!');
    } else {
        alert('Заявка уже подана!');
    }
}

// Очистка всех данных
function clearAllData() {
    if (confirm('Вы уверены, что хотите очистить все данные?')) {
        favorites = [];
        userApplications = [];
        searchHistory = [];
        notifications = [];
        
        localStorage.removeItem('zakupkiFavorites');
        localStorage.removeItem('zakupkiApplications');
        localStorage.removeItem('zakupkiSearchHistory');
        localStorage.removeItem('zakupkiNotifications');
        
        alert('Все данные очищены!');
        location.reload();
    }
}

// Экспорт данных
function exportData() {
    const data = {
        favorites,
        userApplications,
        searchHistory,
        notifications,
        exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'zakupki-data.json';
    a.click();
    URL.revokeObjectURL(url);
}
