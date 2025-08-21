// Инициализация Telegram Web App
let tg = window.Telegram.WebApp;

// Конфигурация бота
const botToken = window.BOT_CONFIG?.token || '8203311811:AAEbVoeZ0inIO7CUFuGUbwNRdoL2xfpxfPw';
const botApiUrl = `https://api.telegram.org/bot${botToken}`;

// Основные переменные
let currentTab = 'home';
let favorites = [];

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    // Настройка Telegram Web App
    if (tg) {
        tg.ready();
        tg.expand();
        tg.setHeaderColor('#007AFF');
        tg.setBackgroundColor('#f2f2f7');
    }
    
    initializeEvents();
    loadInitialData();
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
            <h3 style="margin-bottom: 20px; font-size: 24px;">Поиск закупок</h3>
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <input type="text" placeholder="Название закупки" style="flex: 1; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px;">
                <button style="padding: 12px 20px; background: #007AFF; color: white; border: none; border-radius: 8px;">🔍</button>
            </div>
            <div class="search-filters">
                <input type="text" placeholder="Регион" style="width: 100%; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px; margin-bottom: 10px;">
                <div style="display: flex; gap: 10px;">
                    <input type="number" placeholder="Цена от" style="flex: 1; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px;">
                    <input type="number" placeholder="Цена до" style="flex: 1; padding: 12px; border: 1px solid #e5e5e7; border-radius: 8px;">
                </div>
            </div>
            <div class="search-results" style="margin-top: 20px;">
                <h4>Результаты поиска</h4>
                <div class="results-list"></div>
            </div>
        </div>
    `;
    
    document.querySelector('.app-container').appendChild(searchContent);
}

// Показ избранного
function showFavorites() {
    if (favorites.length === 0) {
        showNotification('У вас пока нет избранных закупок');
    } else {
        showFavoritesContent();
    }
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

// Выполнение поиска
function performSearch() {
    const inputs = document.querySelectorAll('.modal-input');
    const searchData = {
        name: inputs[0].value,
        region: inputs[1].value,
        priceFrom: inputs[2].value,
        priceTo: inputs[3].value
    };
    
    showNotification('Поиск выполняется...');
    
    setTimeout(() => {
        document.getElementById('searchModal').classList.remove('active');
        showSearchResults(searchData);
    }, 1000);
}

// Показ результатов поиска
function showSearchResults(searchData) {
    switchTab('search');
    
    const mockResults = [
        { name: 'Поставка офисной техники', price: '₽ 1,200,000', region: 'Москва', deadline: '25.12.2024' },
        { name: 'Услуги по обслуживанию зданий', price: '₽ 800,000', region: 'Санкт-Петербург', deadline: '30.12.2024' },
        { name: 'Закупка медицинского оборудования', price: '₽ 3,500,000', region: 'Новосибирск', deadline: '10.01.2025' }
    ];
    
    const resultsList = document.querySelector('.results-list');
    if (resultsList) {
        resultsList.innerHTML = '';
        
        mockResults.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.className = 'purchase-item';
            resultItem.innerHTML = `
                <div class="purchase-title">${result.name}</div>
                <div class="purchase-info">
                    <span class="price">${result.price}</span>
                    <span class="deadline">До ${result.deadline}</span>
                </div>
                <div style="margin-top: 8px; font-size: 12px; color: #666;">${result.region}</div>
            `;
            resultsList.appendChild(resultItem);
        });
    }
}

// Показ деталей закупки
function showPurchaseDetails(purchaseItem) {
    const title = purchaseItem.querySelector('.purchase-title').textContent;
    const price = purchaseItem.querySelector('.price').textContent;
    const deadline = purchaseItem.querySelector('.deadline').textContent;
    
    const detailsHTML = `
        <div style="padding: 20px;">
            <h3 style="margin-bottom: 20px;">${title}</h3>
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <p><strong>Цена:</strong> ${price}</p>
                <p><strong>Срок подачи:</strong> ${deadline}</p>
                <p><strong>Статус:</strong> Активна</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <button onclick="addToFavorites('${title}')" style="flex: 1; padding: 12px; background: #007AFF; color: white; border: none; border-radius: 8px;">В избранное</button>
                <button onclick="showNotification('Функция в разработке')" style="flex: 1; padding: 12px; background: #f2f2f7; color: #007AFF; border: none; border-radius: 8px;">Подать заявку</button>
            </div>
        </div>
    `;
    
    showModal('Детали закупки', detailsHTML);
}

// Добавление в избранное
function addToFavorites(title) {
    if (!favorites.includes(title)) {
        favorites.push(title);
        showNotification('Добавлено в избранное');
        
        // Отправляем уведомление через бота
        sendUserNotification(`✅ Закупка "${title}" добавлена в избранное`);
        
        // Сохраняем в localStorage
        saveFavorites();
        
        document.querySelector('.modal').classList.remove('active');
    } else {
        showNotification('Уже в избранном');
    }
}

// Показ моих заявок
function showMyApplications() {
    const applications = [
        { name: 'Поставка компьютеров', status: 'Рассматривается', date: '10.12.2024' },
        { name: 'Услуги по уборке', status: 'Одобрена', date: '05.12.2024' }
    ];
    
    let applicationsHTML = '<div style="padding: 20px;"><h3 style="margin-bottom: 20px;">Мои заявки</h3>';
    
    applications.forEach(app => {
        const statusColor = app.status === 'Одобрена' ? '#34C759' : '#FF9500';
        applicationsHTML += `
            <div style="background: white; padding: 16px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin-bottom: 8px;">${app.name}</h4>
                <p style="color: ${statusColor}; font-weight: 600; margin-bottom: 8px;">${app.status}</p>
                <span style="color: #999; font-size: 12px;">Подана: ${app.date}</span>
            </div>
        `;
    });
    
    applicationsHTML += '</div>';
    showModal('Мои заявки', applicationsHTML);
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
        
        const savedFavorites = localStorage.getItem('zakupki_favorites');
        if (savedFavorites) {
            favorites = JSON.parse(savedFavorites);
        }
    }, 500);
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
