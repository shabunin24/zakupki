// Нативный поиск в стиле Яндекс для ГосЗакупки
class YandexStyleSearch {
    constructor() {
        this.searchIndex = new Map();
        this.searchHistory = [];
        this.suggestions = [];
        this.currentQuery = '';
        this.searchResults = [];
        
        this.init();
    }
    
    init() {
        this.buildSearchIndex();
        this.setupEventListeners();
        this.loadSearchHistory();
    }
    
    // Построение поискового индекса
    buildSearchIndex() {
        if (typeof mockPurchases === 'undefined') return;
        
        mockPurchases.forEach((purchase) => {
            const searchableText = [
                purchase.title,
                purchase.description,
                purchase.category,
                purchase.region
            ].join(' ').toLowerCase();
            
            const words = searchableText.split(/\s+/);
            
            words.forEach(word => {
                if (word.length > 2) {
                    if (!this.searchIndex.has(word)) {
                        this.searchIndex.set(word, []);
                    }
                    this.searchIndex.get(word).push({
                        purchaseId: purchase.id,
                        relevance: this.calculateWordRelevance(word, purchase)
                    });
                }
            });
        });
        
        console.log('Поисковый индекс построен:', this.searchIndex.size, 'слов');
    }
    
    // Расчет релевантности
    calculateWordRelevance(word, purchase) {
        let relevance = 1;
        
        if (purchase.title.toLowerCase().includes(word)) relevance += 10;
        if (purchase.description.toLowerCase().includes(word)) relevance += 5;
        if (purchase.category.toLowerCase().includes(word)) relevance += 3;
        if (purchase.region.toLowerCase().includes(word)) relevance += 3;
        
        return relevance;
    }
    
    // Поиск
    search(query) {
        const queryLower = query.toLowerCase();
        const results = [];
        const resultMap = new Map();
        
        for (const [word, entries] of this.searchIndex) {
            if (word.includes(queryLower) || queryLower.includes(word)) {
                entries.forEach(entry => {
                    if (!resultMap.has(entry.purchaseId)) {
                        const purchase = mockPurchases.find(p => p.id === entry.purchaseId);
                        if (purchase) {
                            const relevance = this.calculateSearchRelevance(purchase, query);
                            resultMap.set(entry.purchaseId, {
                                purchase: purchase,
                                relevance: relevance
                            });
                        }
                    }
                });
            }
        }
        
        results.push(...resultMap.values());
        results.sort((a, b) => b.relevance - a.relevance);
        
        return results;
    }
    
    // Расчет релевантности поиска
    calculateSearchRelevance(purchase, query) {
        const queryLower = query.toLowerCase();
        let relevance = 0;
        
        if (purchase.title.toLowerCase().includes(queryLower)) relevance += 100;
        if (purchase.description.toLowerCase().includes(queryLower)) relevance += 30;
        if (purchase.category.toLowerCase().includes(queryLower)) relevance += 40;
        if (purchase.region.toLowerCase().includes(queryLower)) relevance += 35;
        
        return relevance;
    }
    
    // Добавление в историю
    addToSearchHistory(query) {
        if (!this.searchHistory.includes(query)) {
            this.searchHistory.unshift(query);
            this.searchHistory = this.searchHistory.slice(0, 20);
            localStorage.setItem('zakupkiSearchHistory', JSON.stringify(this.searchHistory));
        }
    }
    
    // Загрузка истории
    loadSearchHistory() {
        try {
            const history = localStorage.getItem('zakupkiSearchHistory');
            if (history) {
                this.searchHistory = JSON.parse(history);
            }
        } catch (e) {
            console.error('Ошибка загрузки истории поиска:', e);
        }
    }
    
    // Настройка обработчиков событий
    setupEventListeners() {
        const searchInput = document.getElementById('yandexSearchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearchInput(e.target.value));
            searchInput.addEventListener('focus', () => this.showSearchHistory());
        }
    }
    
    // Обработка ввода в поиске
    handleSearchInput(query) {
        this.currentQuery = query.trim();
        
        if (this.currentQuery.length === 0) {
            this.showSearchHistory();
            return;
        }
        
        if (this.currentQuery.length > 2) {
            this.findSuggestions(this.currentQuery);
        }
    }
    
    // Поиск подсказок
    findSuggestions(query) {
        const suggestions = [];
        const queryLower = query.toLowerCase();
        
        // Поиск по индексу
        for (const [word, entries] of this.searchIndex) {
            if (word.startsWith(queryLower) || word.includes(queryLower)) {
                const purchase = mockPurchases.find(p => p.id === entries[0].purchaseId);
                if (purchase) {
                    suggestions.push({
                        text: this.highlightQuery(purchase.title, query),
                        purchase: purchase,
                        type: 'purchase'
                    });
                }
            }
        }
        
        // Поиск по истории
        this.searchHistory.forEach(historyItem => {
            if (historyItem.toLowerCase().includes(queryLower)) {
                suggestions.push({
                    text: this.highlightQuery(historyItem, query),
                    type: 'history'
                });
            }
        });
        
        this.suggestions = suggestions.slice(0, 8);
        this.showSuggestions();
    }
    
    // Подсветка поискового запроса
    highlightQuery(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<strong>$1</strong>');
    }
    
    // Показ подсказок
    showSuggestions() {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        if (!suggestionsContainer || this.suggestions.length === 0) return;
        
        let html = '<div class="suggestion-header">Поисковые подсказки</div>';
        
        this.suggestions.forEach((suggestion, index) => {
            html += `
                <div class="suggestion-item" onclick="yandexSearch.selectSuggestion(${index})">
                    <div class="suggestion-text">${suggestion.text}</div>
                    <div class="suggestion-type">${this.getSuggestionTypeLabel(suggestion.type)}</div>
                </div>
            `;
        });
        
        suggestionsContainer.innerHTML = html;
        suggestionsContainer.style.display = 'block';
    }
    
    // Получение метки типа подсказки
    getSuggestionTypeLabel(type) {
        const labels = {
            'purchase': 'Закупка',
            'history': 'История'
        };
        return labels[type] || 'Другое';
    }
    
    // Выбор подсказки
    selectSuggestion(index) {
        const suggestion = this.suggestions[index];
        if (suggestion.type === 'purchase') {
            this.performSearch(suggestion.purchase.title);
        } else {
            this.performSearch(suggestion.text.replace(/<[^>]*>/g, ''));
        }
    }
    
    // Показ истории поиска
    showSearchHistory() {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        if (!suggestionsContainer) return;
        
        if (this.searchHistory.length > 0) {
            let html = '<div class="suggestion-header">Недавние поиски</div>';
            this.searchHistory.slice(0, 5).forEach(query => {
                html += `
                    <div class="suggestion-item" onclick="yandexSearch.performSearch('${query}')">
                        <div class="suggestion-text">${query}</div>
                        <div class="suggestion-type">История</div>
                    </div>
                `;
            });
            suggestionsContainer.innerHTML = html;
            suggestionsContainer.style.display = 'block';
        }
    }
    
    // Выполнение поиска
    performSearch(query) {
        if (!query.trim()) return;
        
        console.log('Выполняем поиск:', query);
        
        // Добавляем в историю
        this.addToSearchHistory(query);
        
        // Выполняем поиск
        const results = this.search(query);
        
        // Показываем результаты
        this.displaySearchResults(results, query);
        
        // Скрываем подсказки
        this.hideSuggestions();
        
        // Обновляем URL
        this.updateSearchURL(query);
    }
    
    // Скрытие подсказок
    hideSuggestions() {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        if (suggestionsContainer) {
            suggestionsContainer.style.display = 'none';
        }
    }
    
    // Отображение результатов поиска
    displaySearchResults(results, query) {
        const resultsContainer = document.getElementById('searchResults');
        if (!resultsContainer) return;
        
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <div class="no-results-icon">🔍</div>
                    <h3>По вашему запросу ничего не найдено</h3>
                    <p>Попробуйте изменить поисковый запрос или использовать фильтры</p>
                    <div class="search-tips">
                        <h4>Советы по поиску:</h4>
                        <ul>
                            <li>Используйте ключевые слова</li>
                            <li>Попробуйте синонимы</li>
                            <li>Упростите запрос</li>
                        </ul>
                    </div>
                </div>
            `;
            return;
        }
        
        // Статистика поиска
        const stats = this.getSearchStats(results, query);
        
        let html = `
            <div class="search-stats">
                <div class="stats-item">
                    <span class="stats-number">${results.length}</span>
                    <span class="stats-label">результатов</span>
                </div>
                <div class="stats-item">
                    <span class="stats-number">${stats.categories}</span>
                    <span class="stats-label">категорий</span>
                </div>
                <div class="stats-item">
                    <span class="stats-number">${stats.regions}</span>
                    <span class="stats-label">регионов</span>
                </div>
                <div class="stats-item">
                    <span class="stats-number">${stats.avgPrice}</span>
                    <span class="stats-label">средняя цена</span>
                </div>
            </div>
        `;
        
        // Результаты поиска
        results.forEach((result) => {
            const purchase = result.purchase;
            html += `
                <div class="search-result-item" data-id="${purchase.id}">
                    <div class="result-header">
                        <h3 class="result-title">
                            <a href="#" onclick="yandexSearch.showPurchaseDetails(${purchase.id})">
                                ${purchase.title}
                            </a>
                        </h3>
                        <div class="result-meta">
                            <span class="result-number">${purchase.number || '№' + purchase.id}</span>
                            <span class="result-status ${purchase.status}">${purchase.status === 'active' ? 'Активна' : 'Завершена'}</span>
                        </div>
                    </div>
                    <div class="result-content">
                        ${purchase.description}
                    </div>
                    <div class="result-footer">
                        <div class="result-category">${purchase.category}</div>
                        <div class="result-region">${purchase.region}</div>
                        <div class="result-price">${this.formatPrice(purchase.price)}</div>
                        <div class="result-deadline">До ${this.formatDate(purchase.deadline)}</div>
                    </div>
                    <div class="result-actions">
                        <button onclick="yandexSearch.addToFavorites(${purchase.id})" class="btn-favorite">
                            ⭐ Добавить в избранное
                        </button>
                        <button onclick="yandexSearch.submitApplication(${purchase.id})" class="btn-apply">
                            📝 Подать заявку
                        </button>
                    </div>
                </div>
            `;
        });
        
        resultsContainer.innerHTML = html;
    }
    
    // Получение статистики поиска
    getSearchStats(results, query) {
        const categories = new Set();
        const regions = new Set();
        let totalPrice = 0;
        
        results.forEach(result => {
            categories.add(result.purchase.category);
            regions.add(result.purchase.region);
            totalPrice += result.purchase.price;
        });
        
        return {
            categories: categories.size,
            regions: regions.size,
            avgPrice: this.formatPrice(totalPrice / results.length)
        };
    }
    
    // Обновление URL поиска
    updateSearchURL(query) {
        const url = new URL(window.location);
        url.searchParams.set('q', query);
        window.history.pushState({}, '', url);
    }
    
    // Показ деталей закупки
    showPurchaseDetails(purchaseId) {
        console.log('Показать детали закупки:', purchaseId);
        // Здесь можно добавить модальное окно с деталями
    }
    
    // Добавление в избранное
    addToFavorites(purchaseId) {
        console.log('Добавить в избранное:', purchaseId);
        // Здесь можно добавить логику избранного
    }
    
    // Подача заявки
    submitApplication(purchaseId) {
        console.log('Подать заявку:', purchaseId);
        // Здесь можно добавить логику заявок
    }
    
    // Форматирование цены
    formatPrice(price) {
        return new Intl.NumberFormat('ru-RU', {
            style: 'currency',
            currency: 'RUB',
            minimumFractionDigits: 0
        }).format(price);
    }
    
    // Форматирование даты
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU');
    }
}

// Инициализация
let yandexSearch;
document.addEventListener('DOMContentLoaded', () => {
    yandexSearch = new YandexStyleSearch();
});
