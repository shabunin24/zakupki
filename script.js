// Инициализация Telegram Web App
let tg = window.Telegram.WebApp;

// Конфигурация бота
const botToken = window.BOT_CONFIG?.token || '8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw';
const botApiUrl = `https://api.telegram.org/bot${botToken}`;

// Основные переменные
let currentTab = 'home';
let favorites = [];
let searchHistory = [];
let userApplications = [];
let notifications = [];

// Имитация базы данных закупок
const mockPurchases = [
    {
        id: 1,
        number: "0128300000123000001",
        title: "Поставка компьютерной техники для государственных учреждений",
        price: 2500000,
        currency: "RUB",
        customer: "Министерство цифрового развития",
        region: "Москва",
        deadline: "2024-12-15",
        status: "active",
        category: "Товары",
        subcategory: "Компьютерная техника",
        description: "Поставка персональных компьютеров, ноутбуков и периферийного оборудования",
        documents: ["Техническое задание.pdf", "Форма заявки.doc"],
        contacts: {
            phone: "+7 (495) 123-45-67",
            email: "zakupki@digital.gov.ru",
            contact: "Иванов И.И."
        }
    },
    {
        id: 2,
        number: "0128300000123000002",
        title: "Услуги по уборке и содержанию зданий",
        price: 500000,
        currency: "RUB",
        customer: "Администрация города",
        region: "Санкт-Петербург",
        deadline: "2024-12-20",
        status: "active",
        category: "Услуги",
        subcategory: "Бытовые услуги",
        description: "Комплексные услуги по уборке и содержанию административных зданий",
        documents: ["Техническое задание.pdf"],
        contacts: {
            phone: "+7 (812) 234-56-78",
            email: "zakupki@spb.gov.ru",
            contact: "Петров П.П."
        }
    },
    {
        id: 3,
        number: "0128300000123000003",
        title: "Закупка медицинского оборудования",
        price: 3500000,
        currency: "RUB",
        customer: "Министерство здравоохранения",
        region: "Новосибирск",
        deadline: "2025-01-10",
        status: "active",
        category: "Товары",
        subcategory: "Медицинское оборудование",
        description: "Поставка диагностического и лечебного медицинского оборудования",
        documents: ["Техническое задание.pdf", "Спецификация.xlsx"],
        contacts: {
            phone: "+7 (383) 345-67-89",
            email: "zakupki@health.gov.ru",
            contact: "Сидоров С.С."
        }
    },
    {
        id: 4,
        number: "0128300000123000004",
        title: "Строительные работы по ремонту дорог",
        price: 15000000,
        currency: "RUB",
        customer: "Федеральное дорожное агентство",
        region: "Краснодар",
        deadline: "2025-02-15",
        status: "active",
        category: "Работы",
        subcategory: "Строительные работы",
        description: "Капитальный ремонт автомобильных дорог федерального значения",
        documents: ["Проектная документация.pdf", "Смета.xlsx"],
        contacts: {
            phone: "+7 (861) 456-78-90",
            email: "zakupki@roads.gov.ru",
            contact: "Козлов К.К."
        }
    },
    {
        id: 5,
        number: "0128300000123000005",
        title: "Услуги по обучению персонала",
        price: 800000,
        currency: "RUB",
        customer: "Министерство образования",
        region: "Екатеринбург",
        deadline: "2025-01-25",
        status: "active",
        category: "Услуги",
        subcategory: "Образовательные услуги",
        description: "Проведение курсов повышения квалификации для государственных служащих",
        documents: ["Программа обучения.pdf", "Учебный план.doc"],
        contacts: {
            phone: "+7 (343) 567-89-01",
            email: "zakupki@education.gov.ru",
            contact: "Морозов М.М."
        }
    }
];

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    // Настройка Telegram Web App
    if (tg) {
        tg.ready();
        tg.expand();
        tg.setHeaderColor('#007AFF');
        tg.setBackgroundColor('#f2f2f7');
    }
    
    // Инициализация событий
    initializeEvents();
    
    // Загрузка данных
    loadInitialData();
    
    // Инициализация поиска
    initializeSearch();
});

// Инициализация событий
function initializeEvents() {
    // События для элементов меню
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function() {
            const section = this.dataset.section;
            handleMenuClick(section);
        });
    });
    
    // События для нижней навигации
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function() {
            const tab = this.dataset.tab;
            switchTab(tab);
        });
    });
    
    // События для кнопок быстрых действий
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const text = this.textContent;
            handleActionClick(text);
        });
    });
    
    // События для модальных окон
    initializeModalEvents();
    
    // События для элементов закупок
    document.querySelectorAll('.purchase-item').forEach(item => {
        item.addEventListener('click', function() {
            showPurchaseDetails(this);
        });
    });
}

// Обработка клика по элементам меню
function handleMenuClick(section) {
    switch(section) {
        case 'search':
            showSearchModal();
            break;
        case 'favorites':
            showFavorites();
            break;
        case 'categories':
            showCategories();
            break;
        case 'news':
            showNews();
            break;
    }
}

// Переключение вкладок
function switchTab(tab) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
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
    }
}

// Скрытие всех секций
function hideAllSections() {
    const sections = ['home', 'search', 'favorites', 'profile'];
    sections.forEach(section => {
        const element = document.querySelector(`.${section}-content`);
        if (element) {
            element.style.display = 'none';
        }
    });
}

// Показ домашнего контента
function showHomeContent() {
    document.querySelector('.main-menu').style.display = 'grid';
    document.querySelector('.quick-actions').style.display = 'block';
    document.querySelector('.recent-purchases').style.display = 'block';
}

// Показ контента поиска
function showSearchContent() {
    if (!document.querySelector('.search-content')) {
        createSearchContent();
    }
    
    document.querySelector('.search-content').style.display = 'block';
    document.querySelector('.main-menu').style.display = 'none';
    document.querySelector('.quick-actions').style.display = 'none';
    document.querySelector('.recent-purchases').style.display = 'none';
}

// Создание контента поиска
function createSearchContent() {
    const searchContent = document.createElement('div');
    searchContent.className = 'search-content';
    searchContent.innerHTML = `
        <div style="padding: 20px;">
            <h3 style="margin-bottom: 20px; font-size: 24px;">🔍 Расширенный поиск закупок</h3>
            
            <!-- Основной поиск -->
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <input type="text" id="mainSearchInput" placeholder="Название, номер или описание закупки" style="flex: 1; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px; font-size: 16px;">
                <button onclick="performAdvancedSearch()" style="padding: 12px 20px; background: #007AFF; color: white; border: none; border-radius: 8px; font-weight: 600;">🔍</button>
            </div>
            
            <!-- Расширенные фильтры -->
            <div class="search-filters" style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="margin-bottom: 16px; color: #333;">Фильтры поиска</h4>
                
                <!-- Категория -->
                <div style="margin-bottom: 16px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Категория:</label>
                    <select id="categoryFilter" style="width: 100%; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px; font-size: 16px;">
                        <option value="">Все категории</option>
                        <option value="Товары">Товары</option>
                        <option value="Услуги">Услуги</option>
                        <option value="Работы">Работы</option>
                    </select>
                </div>
                
                <!-- Регион -->
                <div style="margin-bottom: 16px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Регион:</label>
                    <select id="regionFilter" style="width: 100%; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px; font-size: 16px;">
                        <option value="">Все регионы</option>
                        <option value="Москва">Москва</option>
                        <option value="Санкт-Петербург">Санкт-Петербург</option>
                        <option value="Новосибирск">Новосибирск</option>
                        <option value="Краснодар">Краснодар</option>
                        <option value="Екатеринбург">Екатеринбург</option>
                    </select>
                </div>
                
                <!-- Ценовой диапазон -->
                <div style="margin-bottom: 16px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Ценовой диапазон (₽):</label>
                    <div style="display: flex; gap: 10px;">
                        <input type="number" id="priceFrom" placeholder="От" style="flex: 1; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px; font-size: 16px;">
                        <input type="number" id="priceTo" placeholder="До" style="flex: 1; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px; font-size: 16px;">
                    </div>
                </div>
                
                <!-- Статус -->
                <div style="margin-bottom: 16px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Статус:</label>
                    <select id="statusFilter" style="width: 100%; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px; font-size: 16px;">
                        <option value="">Все статусы</option>
                        <option value="active">Активные</option>
                        <option value="completed">Завершенные</option>
                    </select>
                </div>
                
                <!-- Кнопки фильтров -->
                <div style="display: flex; gap: 10px;">
                    <button onclick="applyFilters()" style="flex: 1; padding: 12px; background: #007AFF; color: white; border: none; border-radius: 8px; font-weight: 600;">
                        ✅ Применить фильтры
                    </button>
                    <button onclick="clearFilters()" style="flex: 1; padding: 12px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 8px; font-weight: 600;">
                        🗑️ Очистить
                    </button>
                </div>
            </div>
            
            <!-- Быстрые фильтры -->
            <div class="quick-filters" style="margin-bottom: 20px;">
                <h4 style="margin-bottom: 12px; color: #333;">Быстрые фильтры:</h4>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button onclick="quickFilter('price', 'low')" style="padding: 8px 16px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 20px; font-size: 14px;">
                        💰 До 1 млн ₽
                    </button>
                    <button onclick="quickFilter('price', 'high')" style="padding: 8px 16px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 20px; font-size: 14px;">
                        💎 От 10 млн ₽
                    </button>
                    <button onclick="quickFilter('deadline', 'week')" style="padding: 8px 16px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 20px; font-size: 14px;">
                        ⏰ До недели
                    </button>
                    <button onclick="quickFilter('category', 'services')" style="padding: 8px 16px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 20px; font-size: 14px;">
                        🛠️ Услуги
                    </button>
                </div>
            </div>
            
            <!-- Результаты поиска -->
            <div class="search-results">
                <h4 id="resultsHeader">Результаты поиска</h4>
                <div class="results-list"></div>
            </div>
        </div>
    `;
    
    document.querySelector('.app-container').appendChild(searchContent);
}

// Показ избранного
function showFavorites() {
    if (favorites.length === 0) {
        showModal('Избранное', `
            <div style="padding: 20px; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 16px; color: #8e8e93;">⭐</div>
                <h3 style="margin-bottom: 16px;">У вас пока нет избранных закупок</h3>
                <p style="color: #666; margin-bottom: 20px;">Добавляйте интересующие закупки в избранное для быстрого доступа</p>
                <button onclick="switchTab('search')" style="padding: 12px 24px; background: #007AFF; color: white; border: none; border-radius: 8px; font-weight: 600;">
                    🔍 Найти закупки
                </button>
            </div>
        `);
        return;
    }
    
    let favoritesHTML = '<div style="padding: 20px;"><h3 style="margin-bottom: 20px;">Избранные закупки</h3>';
    
    favorites.forEach(favoriteId => {
        const purchase = mockPurchases.find(p => p.id === favoriteId);
        if (purchase) {
            favoritesHTML += `
                <div style="background: white; padding: 16px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                        <div style="flex: 1;">
                            <h4 style="margin-bottom: 8px; color: #333;">${purchase.title}</h4>
                            <div style="font-size: 12px; color: #666; margin-bottom: 8px;">
                                №${purchase.number} • ${purchase.region}
                            </div>
                        </div>
                        <button onclick="removeFromFavorites(${purchase.id})" style="padding: 4px 8px; background: #FF3B30; color: white; border: none; border-radius: 4px; font-size: 12px;">
                            ❌
                        </button>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="color: #007AFF; font-weight: 600;">
                            ${formatPrice(purchase.price, purchase.currency)}
                        </span>
                        <span style="color: #999; font-size: 12px;">
                            До ${formatDate(purchase.deadline)}
                        </span>
                    </div>
                    
                    <div style="display: flex; gap: 8px;">
                        <button onclick="showPurchaseDetails(${purchase.id})" style="flex: 1; padding: 8px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 6px; font-size: 12px;">
                            📋 Детали
                        </button>
                        <button onclick="submitApplication(${purchase.id})" style="flex: 1; padding: 8px; background: #34C759; color: white; border: none; border-radius: 6px; font-size: 12px;">
                            📝 Подать заявку
                        </button>
                    </div>
                </div>
            `;
        }
    });
    
    favoritesHTML += '</div>';
    showModal('Избранное', favoritesHTML);
}

// Удаление из избранного
function removeFromFavorites(purchaseId) {
    favorites = favorites.filter(id => id !== purchaseId);
    saveFavorites();
    
    showNotification('Убрано из избранного');
    
    // Обновляем отображение
    showFavorites();
}

// Показ категорий
function showCategories() {
    const categories = [
        'Товары', 'Работы', 'Услуги', 'Техника', 
        'Строительство', 'Медицина', 'Образование', 'Транспорт'
    ];
    
    let categoriesHTML = '<div style="padding: 20px;"><h3 style="margin-bottom: 20px;">Категории закупок</h3><div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">';
    
    categories.forEach(category => {
        categoriesHTML += `
            <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="font-size: 24px; margin-bottom: 8px;">📁</div>
                <span style="font-size: 14px; font-weight: 500;">${category}</span>
            </div>
        `;
    });
    
    categoriesHTML += '</div></div>';
    showModal('Категории', categoriesHTML);
}

// Показ новостей
function showNews() {
    const news = [
        { title: 'Обновление системы закупок', date: '15.12.2024', content: 'Внедрены новые функции для удобства пользователей' },
        { title: 'Изменения в законодательстве', date: '10.12.2024', content: 'Обновлены правила проведения электронных торгов' },
        { title: 'Техническое обслуживание', date: '05.12.2024', content: 'Система будет недоступна 20 декабря с 02:00 до 06:00' }
    ];
    
    let newsHTML = '<div style="padding: 20px;"><h3 style="margin-bottom: 20px;">Новости</h3>';
    
    news.forEach(item => {
        newsHTML += `
            <div style="background: white; padding: 16px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin-bottom: 8px; color: #007AFF;">${item.title}</h4>
                <p style="color: #666; font-size: 14px; margin-bottom: 8px;">${item.content}</p>
                <span style="color: #999; font-size: 12px;">${item.date}</span>
            </div>
        `;
    });
    
    newsHTML += '</div>';
    showModal('Новости', newsHTML);
}

// Обработка клика по кнопкам действий
function handleActionClick(actionText) {
    switch(actionText) {
        case 'Найти закупку':
            showSearchModal();
            break;
        case 'Мои заявки':
            showMyApplications();
            break;
        case 'Помощь':
            showHelp();
            break;
    }
}

// Показ модального окна поиска
function showSearchModal() {
    const modal = document.getElementById('searchModal');
    modal.classList.add('active');
}

// Инициализация событий модальных окон
function initializeModalEvents() {
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            modal.classList.remove('active');
        });
    });
    
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });
    
    const searchSubmitBtn = document.querySelector('.search-submit-btn');
    if (searchSubmitBtn) {
        searchSubmitBtn.addEventListener('click', performSearch);
    }
}

// Инициализация поиска
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearchInput);
        searchInput.addEventListener('focus', showSearchSuggestions);
    }
}

// Обработка ввода в поиск
function handleSearchInput(e) {
    const query = e.target.value.trim();
    
    if (query.length > 2) {
        const suggestions = getSearchSuggestions(query);
        showSearchSuggestions(suggestions);
    } else {
        hideSearchSuggestions();
    }
}

// Получение поисковых подсказок
function getSearchSuggestions(query) {
    const suggestions = [];
    const lowerQuery = query.toLowerCase();
    
    // Поиск по названию
    mockPurchases.forEach(purchase => {
        if (purchase.title.toLowerCase().includes(lowerQuery)) {
            suggestions.push({
                type: 'title',
                text: purchase.title,
                purchase: purchase
            });
        }
    });
    
    // Поиск по категории
    mockPurchases.forEach(purchase => {
        if (purchase.category.toLowerCase().includes(lowerQuery) || 
            purchase.subcategory.toLowerCase().includes(lowerQuery)) {
            suggestions.push({
                type: 'category',
                text: `${purchase.category} - ${purchase.subcategory}`,
                purchase: purchase
            });
        }
    });
    
    // Поиск по региону
    mockPurchases.forEach(purchase => {
        if (purchase.region.toLowerCase().includes(lowerQuery)) {
            suggestions.push({
                type: 'region',
                text: purchase.region,
                purchase: purchase
            });
        }
    });
    
    return suggestions.slice(0, 5); // Максимум 5 подсказок
}

// Показ поисковых подсказок
function showSearchSuggestions(suggestions = null) {
    let suggestionsToShow = suggestions;
    
    if (!suggestionsToShow) {
        // Показываем последние поиски
        suggestionsToShow = searchHistory.slice(0, 5).map(item => ({
            type: 'history',
            text: item,
            isHistory: true
        }));
    }
    
    if (suggestionsToShow.length === 0) return;
    
    // Создаем или обновляем блок подсказок
    let suggestionsBlock = document.querySelector('.search-suggestions');
    if (!suggestionsBlock) {
        suggestionsBlock = document.createElement('div');
        suggestionsBlock.className = 'search-suggestions';
        suggestionsBlock.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #e5e5e7;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            max-height: 300px;
            overflow-y: auto;
        `;
        
        const searchContainer = document.querySelector('.search-container');
        searchContainer.style.position = 'relative';
        searchContainer.appendChild(suggestionsBlock);
    }
    
    // Очищаем и заполняем подсказки
    suggestionsBlock.innerHTML = '';
    
    suggestionsToShow.forEach(suggestion => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.style.cssText = `
            padding: 12px 16px;
            border-bottom: 1px solid #f0f0f0;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
        `;
        
        if (suggestion.isHistory) {
            item.innerHTML = `
                <span style="color: #8e8e93;">🕒</span>
                <span style="color: #666;">${suggestion.text}</span>
            `;
        } else {
            const icon = suggestion.type === 'title' ? '📋' : 
                        suggestion.type === 'category' ? '📁' : '📍';
            item.innerHTML = `
                <span style="color: #007AFF;">${icon}</span>
                <span>${suggestion.text}</span>
            `;
        }
        
        item.addEventListener('click', () => {
            if (suggestion.purchase) {
                showPurchaseDetails(suggestion.purchase);
            } else if (suggestion.isHistory) {
                document.querySelector('.search-input').value = suggestion.text;
                performSearch(suggestion.text);
            }
            hideSearchSuggestions();
        });
        
        suggestionsBlock.appendChild(item);
    });
}

// Скрытие поисковых подсказок
function hideSearchSuggestions() {
    const suggestionsBlock = document.querySelector('.search-suggestions');
    if (suggestionsBlock) {
        suggestionsBlock.remove();
    }
}

// Выполнение поиска
function performSearch(query = null) {
    const searchInput = document.querySelector('.search-input');
    const queryText = query || searchInput.value.trim();
    
    if (!queryText) {
        showNotification('Введите поисковый запрос');
        return;
    }
    
    // Добавляем в историю поиска
    if (!searchHistory.includes(queryText)) {
        searchHistory.unshift(queryText);
        searchHistory = searchHistory.slice(0, 10); // Максимум 10 записей
        localStorage.setItem('zakupki_search_history', JSON.stringify(searchHistory));
    }
    
    // Выполняем поиск
    const results = searchPurchases(queryText);
    
    // Показываем результаты
    showSearchResults(results, queryText);
    
    // Скрываем подсказки
    hideSearchSuggestions();
}

// Расширенный поиск закупок с фильтрами
function searchPurchases(query, filters = {}) {
    const lowerQuery = query ? query.toLowerCase() : '';
    const results = [];
    
    mockPurchases.forEach(purchase => {
        let score = 0;
        let passesFilters = true;
        
        // Применяем фильтры
        if (filters.category && purchase.category !== filters.category) {
            passesFilters = false;
        }
        
        if (filters.region && purchase.region !== filters.region) {
            passesFilters = false;
        }
        
        if (filters.status && purchase.status !== filters.status) {
            passesFilters = false;
        }
        
        if (filters.priceFrom && purchase.price < filters.priceFrom) {
            passesFilters = false;
        }
        
        if (filters.priceTo && purchase.price > filters.priceTo) {
            passesFilters = false;
        }
        
        if (!passesFilters) return;
        
        // Если есть поисковый запрос, вычисляем релевантность
        if (lowerQuery) {
            // Поиск по названию (высокий приоритет)
            if (purchase.title.toLowerCase().includes(lowerQuery)) {
                score += 100;
            }
            
            // Поиск по категории
            if (purchase.category.toLowerCase().includes(lowerQuery) || 
                purchase.subcategory.toLowerCase().includes(lowerQuery)) {
                score += 50;
            }
            
            // Поиск по региону
            if (purchase.region.toLowerCase().includes(lowerQuery)) {
                score += 30;
            }
            
            // Поиск по описанию
            if (purchase.description.toLowerCase().includes(lowerQuery)) {
                score += 20;
            }
            
            // Поиск по номеру закупки
            if (purchase.number.includes(query)) {
                score += 80;
            }
            
            if (score > 0) {
                results.push({ ...purchase, score });
            }
        } else {
            // Если нет поискового запроса, показываем все прошедшие фильтры
            results.push({ ...purchase, score: 0 });
        }
    });
    
    // Сортируем по релевантности, затем по цене
    return results.sort((a, b) => {
        if (b.score !== a.score) {
            return b.score - a.score;
        }
        return a.price - b.price;
    });
}

// Выполнение расширенного поиска
function performAdvancedSearch() {
    const searchInput = document.getElementById('mainSearchInput');
    const query = searchInput ? searchInput.value.trim() : '';
    
    const filters = getCurrentFilters();
    const results = searchPurchases(query, filters);
    
    showSearchResults(results, query, filters);
}

// Получение текущих фильтров
function getCurrentFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const regionFilter = document.getElementById('regionFilter');
    const statusFilter = document.getElementById('statusFilter');
    const priceFrom = document.getElementById('priceFrom');
    const priceTo = document.getElementById('priceTo');
    
    return {
        category: categoryFilter ? categoryFilter.value : '',
        region: regionFilter ? regionFilter.value : '',
        status: statusFilter ? statusFilter.value : '',
        priceFrom: priceFrom && priceFrom.value ? parseInt(priceFrom.value) : null,
        priceTo: priceTo && priceTo.value ? parseInt(priceTo.value) : null
    };
}

// Применение фильтров
function applyFilters() {
    performAdvancedSearch();
}

// Очистка фильтров
function clearFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const regionFilter = document.getElementById('regionFilter');
    const statusFilter = document.getElementById('statusFilter');
    const priceFrom = document.getElementById('priceFrom');
    const priceTo = document.getElementById('priceTo');
    const mainSearchInput = document.getElementById('mainSearchInput');
    
    if (categoryFilter) categoryFilter.value = '';
    if (regionFilter) regionFilter.value = '';
    if (statusFilter) statusFilter.value = '';
    if (priceFrom) priceFrom.value = '';
    if (priceTo) priceTo.value = '';
    if (mainSearchInput) mainSearchInput.value = '';
    
    // Показываем все закупки
    const results = searchPurchases('', {});
    showSearchResults(results, '', {});
}

// Быстрые фильтры
function quickFilter(type, value) {
    let filters = {};
    
    switch (type) {
        case 'price':
            if (value === 'low') {
                filters.priceTo = 1000000;
            } else if (value === 'high') {
                filters.priceFrom = 10000000;
            }
            break;
        case 'deadline':
            if (value === 'week') {
                const weekFromNow = new Date();
                weekFromNow.setDate(weekFromNow.getDate() + 7);
                filters.deadlineFrom = weekFromNow.toISOString().split('T')[0];
            }
            break;
        case 'category':
            if (value === 'services') {
                filters.category = 'Услуги';
            }
            break;
    }
    
    const results = searchPurchases('', filters);
    showSearchResults(results, '', filters);
    
    // Обновляем UI фильтров
    updateFiltersUI(filters);
}

// Показ результатов поиска
function showSearchResults(results, query, filters = {}) {
    // Переключаемся на вкладку поиска
    switchTab('search');
    
    // Создаем контент поиска если его нет
    if (!document.querySelector('.search-content')) {
        createSearchContent();
    }
    
    const searchContent = document.querySelector('.search-content');
    const resultsList = searchContent.querySelector('.results-list');
    const resultsHeader = searchContent.querySelector('#resultsHeader');
    
    if (resultsList) {
        resultsList.innerHTML = '';
        
        if (results.length === 0) {
            resultsList.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">
                    <div style="font-size: 48px; margin-bottom: 16px;">🔍</div>
                    <h3>По вашему запросу ничего не найдено</h3>
                    <p>Попробуйте изменить поисковый запрос или использовать фильтры</p>
                    <button onclick="clearFilters()" style="margin-top: 16px; padding: 12px 24px; background: #007AFF; color: white; border: none; border-radius: 8px; font-weight: 600;">
                        🗑️ Очистить фильтры
                    </button>
                </div>
            `;
        } else {
            // Показываем количество результатов и примененные фильтры
            let headerText = `Результаты поиска: ${results.length} закупок`;
            
            if (query) {
                headerText += ` по запросу "${query}"`;
            }
            
            const activeFilters = getActiveFiltersText(filters);
            if (activeFilters) {
                headerText += ` • ${activeFilters}`;
            }
            
            if (resultsHeader) {
                resultsHeader.innerHTML = headerText;
            }
            
            // Добавляем статистику
            const statsHTML = createSearchStats(results);
            resultsList.appendChild(statsHTML);
            
            // Отображаем результаты
            results.forEach((purchase, index) => {
                const resultItem = createPurchaseItem(purchase);
                resultItem.style.animationDelay = `${index * 0.1}s`;
                resultsList.appendChild(resultItem);
            });
        }
    }
}

// Создание статистики поиска
function createSearchStats(results) {
    const statsDiv = document.createElement('div');
    statsDiv.style.cssText = `
        background: #f8f9fa;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 16px;
    `;
    
    // Статистика по категориям
    const categories = {};
    const regions = {};
    let totalPrice = 0;
    
    results.forEach(purchase => {
        categories[purchase.category] = (categories[purchase.category] || 0) + 1;
        regions[purchase.region] = (regions[purchase.region] || 0) + 1;
        totalPrice += purchase.price;
    });
    
    const avgPrice = totalPrice / results.length;
    
    statsDiv.innerHTML = `
        <div style="text-align: center;">
            <div style="font-size: 24px; color: #007AFF; font-weight: 600;">${results.length}</div>
            <div style="font-size: 12px; color: #666;">Всего закупок</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 24px; color: #34C759; font-weight: 600;">${Object.keys(categories).length}</div>
            <div style="font-size: 12px; color: #666;">Категорий</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 24px; color: #FF9500; font-weight: 600;">${Object.keys(regions).length}</div>
            <div style="font-size: 12px; color: #666;">Регионов</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 24px; color: #5856D6; font-weight: 600;">${formatPrice(avgPrice, 'RUB')}</div>
            <div style="font-size: 12px; color: #666;">Средняя цена</div>
        </div>
    `;
    
    return statsDiv;
}

// Получение текста активных фильтров
function getActiveFiltersText(filters) {
    const activeFilters = [];
    
    if (filters.category) activeFilters.push(filters.category);
    if (filters.region) activeFilters.push(filters.region);
    if (filters.status) activeFilters.push(filters.status === 'active' ? 'Активные' : 'Завершенные');
    if (filters.priceFrom) activeFilters.push(`от ${formatPrice(filters.priceFrom, 'RUB')}`);
    if (filters.priceTo) activeFilters.push(`до ${formatPrice(filters.priceTo, 'RUB')}`);
    
    return activeFilters.length > 0 ? activeFilters.join(', ') : '';
}

// Обновление UI фильтров
function updateFiltersUI(filters) {
    const categoryFilter = document.getElementById('categoryFilter');
    const regionFilter = document.getElementById('regionFilter');
    const statusFilter = document.getElementById('statusFilter');
    const priceFrom = document.getElementById('priceFrom');
    const priceTo = document.getElementById('priceTo');
    
    if (categoryFilter && filters.category) categoryFilter.value = filters.category;
    if (regionFilter && filters.region) regionFilter.value = filters.region;
    if (statusFilter && filters.status) statusFilter.value = filters.status;
    if (priceFrom && filters.priceFrom) priceFrom.value = filters.priceFrom;
    if (priceTo && filters.priceTo) priceTo.value = filters.priceTo;
}

// Создание элемента закупки
function createPurchaseItem(purchase) {
    const item = document.createElement('div');
    item.className = 'purchase-item';
    item.style.cssText = `
        background: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.2s;
    `;
    
    item.innerHTML = `
        <div class="purchase-header" style="margin-bottom: 12px;">
            <div class="purchase-number" style="font-size: 12px; color: #666; margin-bottom: 4px;">
                №${purchase.number}
            </div>
            <div class="purchase-title" style="font-size: 16px; font-weight: 600; color: #333; line-height: 1.4;">
                ${purchase.title}
            </div>
        </div>
        
        <div class="purchase-info" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span class="price" style="font-size: 18px; font-weight: 700; color: #007AFF;">
                ${formatPrice(purchase.price, purchase.currency)}
            </span>
            <span class="deadline" style="font-size: 14px; color: #666;">
                До ${formatDate(purchase.deadline)}
            </span>
        </div>
        
        <div class="purchase-details" style="display: flex; gap: 16px; font-size: 12px; color: #666;">
            <span>📍 ${purchase.region}</span>
            <span>📁 ${purchase.category}</span>
            <span>👤 ${purchase.customer}</span>
        </div>
        
        <div class="purchase-actions" style="margin-top: 12px; display: flex; gap: 8px;">
            <button onclick="addToFavorites(${purchase.id})" style="flex: 1; padding: 8px; background: #007AFF; color: white; border: none; border-radius: 6px; font-size: 12px;">
                ⭐ В избранное
            </button>
            <button onclick="showPurchaseDetails(${purchase.id})" style="flex: 1; padding: 8px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 6px; font-size: 12px;">
                📋 Подробнее
            </button>
        </div>
    `;
    
    // Добавляем обработчик клика
    item.addEventListener('click', (e) => {
        if (!e.target.tagName === 'BUTTON') {
            showPurchaseDetails(purchase);
        }
    });
    
    return item;
}

// Форматирование цены
function formatPrice(price, currency) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0
    }).format(price);
}

// Форматирование даты
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
}

// Показ деталей закупки
function showPurchaseDetails(purchaseId) {
    const purchase = typeof purchaseId === 'object' ? purchaseId : mockPurchases.find(p => p.id === purchaseId);
    
    if (!purchase) {
        showNotification('Закупка не найдена');
        return;
    }
    
    const detailsHTML = `
        <div style="padding: 20px;">
            <div style="margin-bottom: 20px;">
                <h3 style="margin-bottom: 8px; color: #333;">${purchase.title}</h3>
                <div style="font-size: 14px; color: #666; margin-bottom: 16px;">
                    №${purchase.number} • ${purchase.status === 'active' ? '🟢 Активна' : '🔴 Завершена'}
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                    <div>
                        <strong>Цена:</strong><br>
                        <span style="color: #007AFF; font-weight: 600;">${formatPrice(purchase.price, purchase.currency)}</span>
                    </div>
                    <div>
                        <strong>Срок подачи:</strong><br>
                        <span style="color: #666;">${formatDate(purchase.deadline)}</span>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div>
                        <strong>Заказчик:</strong><br>
                        <span style="color: #666;">${purchase.customer}</span>
                    </div>
                    <div>
                        <strong>Регион:</strong><br>
                        <span style="color: #666;">${purchase.region}</span>
                    </div>
                </div>
                
                <div style="margin-top: 12px;">
                    <strong>Категория:</strong><br>
                    <span style="color: #666;">${purchase.category} → ${purchase.subcategory}</span>
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <strong>Описание:</strong><br>
                <p style="color: #666; margin: 8px 0 0 0; line-height: 1.4;">${purchase.description}</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <strong>Документы:</strong><br>
                <div style="margin-top: 8px;">
                    ${purchase.documents.map(doc => `
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                            <span style="color: #007AFF;">📄</span>
                            <span style="color: #666;">${doc}</span>
                            <button onclick="downloadDocument('${doc}')" style="margin-left: auto; padding: 4px 8px; background: #007AFF; color: white; border: none; border-radius: 4px; font-size: 12px;">
                                Скачать
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <strong>Контакты:</strong><br>
                <div style="margin-top: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <span style="color: #007AFF;">👤</span>
                        <span style="color: #666;">${purchase.contacts.contact}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <span style="color: #007AFF;">📞</span>
                        <span style="color: #666;">${purchase.contacts.phone}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: #007AFF;">✉️</span>
                        <span style="color: #666;">${purchase.contacts.email}</span>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px;">
                <button onclick="addToFavorites(${purchase.id})" style="flex: 1; padding: 12px; background: #007AFF; color: white; border: none; border-radius: 8px; font-weight: 600;">
                    ⭐ В избранное
                </button>
                <button onclick="submitApplication(${purchase.id})" style="flex: 1; padding: 12px; background: #34C759; color: white; border: none; border-radius: 8px; font-weight: 600;">
                    📝 Подать заявку
                </button>
            </div>
        </div>
    `;
    
    showModal('Детали закупки', detailsHTML);
}

// Добавление в избранное
function addToFavorites(purchaseId) {
    const purchase = mockPurchases.find(p => p.id === purchaseId);
    if (!purchase) {
        showNotification('Закупка не найдена');
        return;
    }
    
    if (!favorites.includes(purchaseId)) {
        favorites.push(purchaseId);
        showNotification('Добавлено в избранное');
        
        // Отправляем уведомление через бота
        sendUserNotification(`✅ Закупка "${purchase.title}" добавлена в избранное`);
        
        // Сохраняем в localStorage
        saveFavorites();
        
        // Закрываем модальное окно если оно открыто
        const modal = document.querySelector('.modal');
        if (modal) {
            modal.classList.remove('active');
        }
    } else {
        showNotification('Уже в избранном');
    }
}

// Подача заявки
function submitApplication(purchaseId) {
    const purchase = mockPurchases.find(p => p.id === purchaseId);
    if (!purchase) {
        showNotification('Закупка не найдена');
        return;
    }
    
    // Проверяем, не подана ли уже заявка
    const existingApplication = userApplications.find(app => app.purchaseId === purchaseId);
    if (existingApplication) {
        showNotification('Заявка уже подана');
        return;
    }
    
    // Создаем заявку
    const application = {
        id: Date.now(),
        purchaseId: purchaseId,
        purchaseTitle: purchase.title,
        purchaseNumber: purchase.number,
        status: 'submitted',
        submittedAt: new Date().toISOString(),
        price: purchase.price,
        currency: purchase.currency
    };
    
    userApplications.push(application);
    
    // Сохраняем в localStorage
    localStorage.setItem('zakupki_applications', JSON.stringify(userApplications));
    
    showNotification('Заявка подана успешно!');
    
    // Отправляем уведомление через бота
    sendUserNotification(`📝 Заявка на закупку "${purchase.title}" подана успешно`);
    
    // Закрываем модальное окно
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Скачивание документа
function downloadDocument(filename) {
    // Имитация скачивания документа
    showNotification(`📄 Документ "${filename}" скачивается...`);
    
    // В реальном приложении здесь был бы запрос к серверу
    setTimeout(() => {
        showNotification('✅ Документ скачан успешно');
    }, 2000);
}

// Показ моих заявок
function showMyApplications() {
    if (userApplications.length === 0) {
        showModal('Мои заявки', `
            <div style="padding: 20px; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 16px; color: #8e8e93;">📝</div>
                <h3 style="margin-bottom: 16px;">У вас пока нет заявок</h3>
                <p style="color: #666; margin-bottom: 20px;">Подайте заявку на интересующую вас закупку</p>
                <button onclick="switchTab('search')" style="padding: 12px 24px; background: #007AFF; color: white; border: none; border-radius: 8px; font-weight: 600;">
                    🔍 Найти закупки
                </button>
            </div>
        `);
        return;
    }
    
    let applicationsHTML = '<div style="padding: 20px;"><h3 style="margin-bottom: 20px;">Мои заявки</h3>';
    
    userApplications.forEach(app => {
        const purchase = mockPurchases.find(p => p.id === app.purchaseId);
        const statusInfo = getStatusInfo(app.status);
        const submittedDate = new Date(app.submittedAt).toLocaleDateString('ru-RU');
        
        applicationsHTML += `
            <div style="background: white; padding: 16px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div style="flex: 1;">
                        <h4 style="margin-bottom: 8px; color: #333;">${app.purchaseTitle}</h4>
                        <div style="font-size: 12px; color: #666; margin-bottom: 8px;">
                            №${app.purchaseNumber}
                        </div>
                    </div>
                    <span style="padding: 4px 8px; background: ${statusInfo.color}; color: white; border-radius: 4px; font-size: 12px; font-weight: 600;">
                        ${statusInfo.text}
                    </span>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="color: #007AFF; font-weight: 600;">
                        ${formatPrice(app.price, app.currency)}
                    </span>
                    <span style="color: #999; font-size: 12px;">
                        Подана: ${submittedDate}
                    </span>
                </div>
                
                <div style="display: flex; gap: 8px;">
                    <button onclick="showPurchaseDetails(${app.purchaseId})" style="flex: 1; padding: 8px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 6px; font-size: 12px;">
                        📋 Детали закупки
                    </button>
                    <button onclick="cancelApplication(${app.id})" style="flex: 1; padding: 8px; background: #FF3B30; color: white; border: none; border-radius: 6px; font-size: 12px;">
                        ❌ Отменить
                    </button>
                </div>
            </div>
        `;
    });
    
    applicationsHTML += '</div>';
    showModal('Мои заявки', applicationsHTML);
}

// Получение информации о статусе
function getStatusInfo(status) {
    const statuses = {
        'submitted': { text: 'Подана', color: '#007AFF' },
        'reviewing': { text: 'Рассматривается', color: '#FF9500' },
        'approved': { text: 'Одобрена', color: '#34C759' },
        'rejected': { text: 'Отклонена', color: '#FF3B30' },
        'completed': { text: 'Завершена', color: '#8E8E93' }
    };
    
    return statuses[status] || { text: 'Неизвестно', color: '#8E8E93' };
}

// Отмена заявки
function cancelApplication(applicationId) {
    const application = userApplications.find(app => app.id === applicationId);
    if (!application) {
        showNotification('Заявка не найдена');
        return;
    }
    
    if (confirm('Вы уверены, что хотите отменить заявку?')) {
        userApplications = userApplications.filter(app => app.id !== applicationId);
        localStorage.setItem('zakupki_applications', JSON.stringify(userApplications));
        
        showNotification('Заявка отменена');
        
        // Обновляем отображение
        showMyApplications();
    }
}

// Показ помощи
function showHelp() {
    const helpHTML = `
        <div style="padding: 20px;">
            <h3 style="margin-bottom: 20px;">Помощь</h3>
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <h4 style="margin-bottom: 12px;">Как найти закупку?</h4>
                <ol style="padding-left: 20px; line-height: 1.6;">
                    <li>Нажмите "Поиск закупок"</li>
                    <li>Введите название или ключевые слова</li>
                    <li>Укажите регион и ценовой диапазон</li>
                    <li>Нажмите "Найти"</li>
                </ol>
            </div>
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px;">
                <h4 style="margin-bottom: 12px;">Контакты поддержки</h4>
                <p>Телефон: 8-800-200-08-31</p>
                <p>Email: support@zakupki.gov.ru</p>
            </div>
        </div>
    `;
    
    showModal('Помощь', helpHTML);
}

// Показ уведомления
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: #007AFF;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        z-index: 10000;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Показ модального окна
function showModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${title}</h3>
                <button class="close-btn">✕</button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    modal.querySelector('.close-btn').addEventListener('click', () => {
        modal.remove();
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// Загрузка начальных данных
function loadInitialData() {
    setTimeout(() => {
        updateStatusBar();
        
        // Загружаем избранное
        const savedFavorites = localStorage.getItem('zakupki_favorites');
        if (savedFavorites) {
            favorites = JSON.parse(savedFavorites);
        }
        
        // Загружаем заявки
        const savedApplications = localStorage.getItem('zakupki_applications');
        if (savedApplications) {
            userApplications = JSON.parse(savedApplications);
        }
        
        // Загружаем историю поиска
        const savedSearchHistory = localStorage.getItem('zakupki_search_history');
        if (savedSearchHistory) {
            searchHistory = JSON.parse(savedSearchHistory);
        }
        
        // Загружаем уведомления
        const savedNotifications = localStorage.getItem('zakupki_notifications');
        if (savedNotifications) {
            notifications = JSON.parse(savedNotifications);
        }
        
        // Обновляем отображение последних закупок
        updateRecentPurchases();
    }, 500);
}

// Обновление отображения последних закупок
function updateRecentPurchases() {
    const purchaseList = document.querySelector('.purchase-list');
    if (purchaseList) {
        purchaseList.innerHTML = '';
        
        // Показываем последние 3 закупки
        const recentPurchases = mockPurchases.slice(0, 3);
        
        recentPurchases.forEach(purchase => {
            const purchaseItem = createPurchaseItem(purchase);
            purchaseItem.style.marginBottom = '12px';
            purchaseList.appendChild(purchaseItem);
        });
    }
}

// Обновление статус бара
function updateStatusBar() {
    const timeElement = document.querySelector('.time');
    if (timeElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ru-RU', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        timeElement.textContent = timeString;
    }
}

// Сохранение избранного
function saveFavorites() {
    localStorage.setItem('zakupki_favorites', JSON.stringify(favorites));
}

// Отправка сообщения через бота
async function sendBotMessage(chatId, message) {
    try {
        const response = await fetch(`${botApiUrl}/sendMessage`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                chat_id: chatId,
                text: message,
                parse_mode: 'HTML'
            })
        });
        
        const result = await response.json();
        return result.ok;
    } catch (error) {
        console.error('Ошибка отправки сообщения:', error);
        return false;
    }
}

// Получение информации о пользователе
function getUserInfo() {
    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
        return tg.initDataUnsafe.user;
    }
    return null;
}

// Отправка уведомления пользователю через бота
function sendUserNotification(message) {
    const user = getUserInfo();
    if (user && user.id) {
        sendBotMessage(user.id, `🔔 <b>ГосЗакупки</b>\n\n${message}`);
    }
}

// Обработка ошибок
window.addEventListener('error', function(e) {
    console.error('Ошибка приложения:', e.error);
    showNotification('Произошла ошибка. Попробуйте обновить страницу.');
});

// Обработка онлайн/офлайн статуса
window.addEventListener('online', function() {
    showNotification('Соединение восстановлено');
});

window.addEventListener('offline', function() {
    showNotification('Нет соединения с интернетом');
});
