// Простое приложение для поиска закупок
let tg = window.Telegram.WebApp;

// Простые данные закупок
const purchases = [
    {
        id: 1,
        title: "Закупка через гов.закупки.ру: поставка офисной мебели",
        price: 1800000,
        region: "Москва",
        description: "Поставка офисной мебели через портал гов.закупки.ру"
    },
    {
        id: 2,
        title: "Услуги по обслуживанию гов.закупки.ру",
        price: 3200000,
        region: "Москва",
        description: "Техническое обслуживание портала государственных закупок гов.закупки.ру"
    },
    {
        id: 3,
        title: "Обучение работе с закупки.ру для госслужащих",
        price: 950000,
        region: "Москва",
        description: "Проведение обучающих семинаров по работе с порталом закупки.ру"
    },
    {
        id: 4,
        title: "Поставка компьютерной техники",
        price: 2500000,
        region: "Санкт-Петербург",
        description: "Поставка персональных компьютеров и ноутбуков"
    },
    {
        id: 5,
        title: "Услуги по уборке зданий",
        price: 500000,
        region: "Новосибирск",
        description: "Комплексные услуги по уборке административных зданий"
    }
];

// Простая функция поиска
function searchPurchases(query) {
    if (!query) return purchases;
    
    const lowerQuery = query.toLowerCase();
    return purchases.filter(purchase => 
        purchase.title.toLowerCase().includes(lowerQuery) ||
        purchase.description.toLowerCase().includes(lowerQuery) ||
        purchase.region.toLowerCase().includes(lowerQuery)
    );
}

// Показать результаты поиска
function showSearchResults(results, query) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #666;">
                <h3>По запросу "${query}" ничего не найдено</h3>
                <p>Попробуйте изменить поисковый запрос</p>
            </div>
        `;
        return;
    }
    
    let html = `<h3>Найдено ${results.length} закупок по запросу "${query}"</h3>`;
    
    results.forEach(purchase => {
        html += `
            <div style="background: white; padding: 16px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin: 0 0 8px 0;">${purchase.title}</h4>
                <p style="margin: 0 0 8px 0; color: #666;">${purchase.description}</p>
                <div style="display: flex; justify-content: space-between; color: #888; font-size: 14px;">
                    <span>${purchase.region}</span>
                    <span>${purchase.price.toLocaleString()} ₽</span>
                </div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// Выполнить поиск
function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    
    if (!query) {
        alert('Введите поисковый запрос');
        return;
    }
    
    console.log('Выполняю поиск по запросу:', query);
    const results = searchPurchases(query);
    console.log('Найдено результатов:', results.length);
    showSearchResults(results, query);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Приложение загружено');
    
    // Инициализация Telegram Web App
    if (tg) {
        tg.ready();
        tg.expand();
    }
    
    // Показать все закупки при загрузке
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        showSearchResults(purchases, '');
    }
});
