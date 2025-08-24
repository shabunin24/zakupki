// Нативный поиск в стиле Яндекс для ГосЗакупки
class YandexStyleSearch {
    constructor() {
        this.searchIndex = new Map();
        this.searchHistory = [];
        this.suggestions = [];
        this.currentQuery = '';
        this.searchResults = [];
        this.filters = {};
        
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
        
        mockPurchases.forEach((purchase, index) => {
            // Индексируем по всем полям
            const searchableText = [
                purchase.title,
                purchase.description,
                purchase.category,
                purchase.subcategory,
                purchase.region,
                purchase.customer,
                purchase.number || ''
            ].join(' ').toLowerCase();
            
            // Разбиваем на слова
            const words = searchableText.split(/\s+/);
            
            words.forEach(word => {
                if (word.length > 2) { // Игнорируем короткие слова
                    if (!this.searchIndex.has(word)) {
                        this.searchIndex.set(word, []);
                    }
                    this.searchIndex.get(word).push({
                        purchaseId: purchase.id,
                        field: this.getFieldForWord(word, purchase),
                        relevance: this.calculateWordRelevance(word, purchase)
                    });
                }
            });
            
            // Добавляем полные фразы
            this.addPhraseToIndex(purchase.title.toLowerCase(), purchase.id, 'title', 10);
            this.addPhraseToIndex(purchase.description.toLowerCase(), purchase.id, 'description', 5);
        });
        
        console.log('Поисковый индекс построен:', this.searchIndex.size, 'слов');
    }
    
    // Добавление фраз в индекс
    addPhraseToIndex(phrase, purchaseId, field, baseRelevance) {
        const words = phrase.split(/\s+/);
        
        // Добавляем фразы разной длины
        for (let i = 0; i < words.length; i++) {
            for (let j = i + 1; j <= words.length; j++) {
                const phrasePart = words.slice(i, j).join(' ');
                if (phrasePart.length > 2) {
                    if (!this.searchIndex.has(phrasePart)) {
                        this.searchIndex.set(phrasePart, []);
                    }
                    this.searchIndex.get(phrasePart).push({
                        purchaseId: purchaseId,
                        field: field,
                        relevance: baseRelevance + (j - i) * 2 // Длинные фразы важнее
                    });
                }
            }
        }
    }
    
    // Определение поля для слова
    getFieldForWord(word, purchase) {
        if (purchase.title.toLowerCase().includes(word)) return 'title';
        if (purchase.description.toLowerCase().includes(word)) return 'description';
        if (purchase.category.toLowerCase().includes(word)) return 'category';
        if (purchase.region.toLowerCase().includes(word)) return 'region';
        return 'other';
    }
    
    // Расчет релевантности слова
    calculateWordRelevance(word, purchase) {
        let relevance = 1;
        
        // Заголовок важнее всего
        if (purchase.title.toLowerCase().includes(word)) relevance += 10;
        
        // Описание менее важно
        if (purchase.description.toLowerCase().includes(word)) relevance += 5;
        
        // Категория и регион
        if (purchase.category.toLowerCase().includes(word)) relevance += 3;
        if (purchase.region.toLowerCase().includes(word)) relevance += 3;
        
        // Номер закупки
        if (purchase.number && purchase.number.includes(word)) relevance += 8;
        
        return relevance;
    }
    
    // Настройка обработчиков событий
    setupEventListeners() {
        const searchInput = document.getElementById('yandexSearchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearchInput(e.target.value));
            searchInput.addEventListener('keydown', (e) => this.handleSearchKeydown(e));
            searchInput.addEventListener('focus', () => this.showSuggestions());
            searchInput.addEventListener('blur', () => setTimeout(() => this.hideSuggestions(), 200));
        }
    }
    
    // Обработка ввода в поиске
    handleSearchInput(query) {
        this.currentQuery = query.trim();
        
        if (this.currentQuery.length === 0) {
            this.hideSuggestions();
            this.showRecentSearches();
            return;
        }
        
        if (this.currentQuery.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        // Поиск подсказок
        this.findSuggestions(this.currentQuery);
        this.showSuggestions();
        
        // Автопоиск при длинном запросе
        if (this.currentQuery.length > 3) {
            this.performSearch(this.currentQuery);
        }
    }
    
    // Обработка клавиш
    handleSearchKeydown(e) {
        if (e.key === 'Enter') {
            this.performSearch(this.currentQuery);
            this.hideSuggestions();
        } else if (e.key === 'ArrowDown') {
            this.navigateSuggestions(1);
        } else if (e.key === 'ArrowUp') {
            this.navigateSuggestions(-1);
        } else if (e.key === 'Escape') {
            this.hideSuggestions();
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
        
        // Поиск по категориям
        const categories = ['Товары', 'Услуги', 'Работы'];
        categories.forEach(category => {
            if (category.toLowerCase().includes(queryLower)) {
                suggestions.push({
                    text: this.highlightQuery(category, query),
                    type: 'category'
                });
            }
        });
        
        // Поиск по регионам
        const regions = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Краснодар', 'Екатеринбург'];
        regions.forEach(region => {
            if (region.toLowerCase().includes(queryLower)) {
                suggestions.push({
                    text: this.highlightQuery(region, query),
                    type: 'region'
                });
            }
        });
        
        this.suggestions = suggestions.slice(0, 8); // Максимум 8 подсказок
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
        
        let html = '';
        
        if (this.currentQuery.length > 0) {
            html += '<div class="suggestion-header">Поисковые подсказки</div>';
            
            this.suggestions.forEach((suggestion, index) => {
                html += `
                    <div class="suggestion-item" data-index="${index}" onclick="yandexSearch.selectSuggestion(${index})">
                        <div class="suggestion-text">${suggestion.text}</div>
                        <div class="suggestion-type">${this.getSuggestionTypeLabel(suggestion.type)}</div>
                    </div>
                `;
            });
        } else {
            html += '<div class="suggestion-header">Недавние поиски</div>';
            this.searchHistory.slice(0, 5).forEach(query => {
                html += `
                    <div class="suggestion-item" onclick="yandexSearch.selectSuggestionByQuery('${query}')">
                        <div class="suggestion-text">${query}</div>
                        <div class="suggestion-type">История</div>
                    </div>
                `;
            });
        }
        
        suggestionsContainer.innerHTML = html;
        suggestionsContainer.style.display = 'block';
    }
    
    // Скрытие подсказок
    hideSuggestions() {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        if (suggestionsContainer) {
            suggestionsContainer.style.display = 'none';
        }
    }
    
    // Показ недавних поисков
    showRecentSearches() {
        const suggestionsContainer = document.getElementById('searchSuggestions');
        if (!suggestionsContainer) return;
        
        if (this.searchHistory.length > 0) {
            let html = '<div class="suggestion-header">Недавние поиски</div>';
            this.searchHistory.slice(0, 5).forEach(query => {
                html += `
                    <div class="suggestion-item" onclick="yandexSearch.selectSuggestionByQuery('${query}')">
                        <div class="suggestion-text">${query}</div>
                        <div class="suggestion-type">История</div>
                    </div>
                `;
            });
            suggestionsContainer.innerHTML = html;
            suggestionsContainer.style.display = 'block';
        }
    }
    
    // Получение метки типа подсказки
    getSuggestionTypeLabel(type) {
        const labels = {
            'purchase': 'Закупка',
            'history': 'История',
            'category': 'Категория',
            'region': 'Регион'
        };
        return labels[type] || 'Другое';
    }
    
    // Навигация по подсказкам
    navigateSuggestions(direction) {
        const items = document.querySelectorAll('.suggestion-item');
        const currentActive = document.querySelector('.suggestion-item.active');
        
        if (items.length === 0) return;
        
        let nextIndex = 0;
        if (currentActive) {
            const currentIndex = parseInt(currentActive.dataset.index);
            nextIndex = (currentIndex + direction + items.length) % items.length;
        }
        
        items.forEach(item => item.classList.remove('active'));
        items[nextIndex].classList.add('active');
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
    
    // Выбор подсказки по запросу
    selectSuggestionByQuery(query) {
        this.performSearch(query);
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
        
        // Обновляем URL
        this.updateSearchURL(query);
    }
    
    // Поиск по запросу
    search(query) {
        const queryLower = query.toLowerCase();
        const results = [];
        const resultMap = new Map(); // Для избежания дубликатов
        
        // Поиск по индексу
        for (const [word, entries] of this.searchIndex) {
            if (word.includes(queryLower) || queryLower.includes(word)) {
                entries.forEach(entry => {
                    if (!resultMap.has(entry.purchaseId)) {
                        const purchase = mockPurchases.find(p => p.id === entry.purchaseId);
                        if (purchase) {
                            const relevance = this.calculateSearchRelevance(purchase, query);
                            resultMap.set(entry.purchaseId, {
                                purchase: purchase,
                                relevance: relevance,
                                highlights: this.getSearchHighlights(purchase, query)
                            });
                        }
                    }
                });
            }
        }
        
        // Преобразуем в массив и сортируем по релевантности
        results.push(...resultMap.values());
        results.sort((a, b) => b.relevance - a.relevance);
        
        return results;
    }
    
    // Расчет релевантности поиска
    calculateSearchRelevance(purchase, query) {
        const queryLower = query.toLowerCase();
        let relevance = 0;
        
        // Точное совпадение в заголовке
        if (purchase.title.toLowerCase().includes(queryLower)) {
            relevance += 100;
        }
        
        // Частичное совпадение в заголовке
        const titleWords = purchase.title.toLowerCase().split(/\s+/);
        titleWords.forEach(word => {
            if (word.includes(queryLower) || queryLower.includes(word)) {
                relevance += 50;
            }
        });
        
        // Совпадение в описании
        if (purchase.description.toLowerCase().includes(queryLower)) {
            relevance += 30;
        }
        
        // Совпадение в категории
        if (purchase.category.toLowerCase().includes(queryLower)) {
            relevance += 40;
        }
        
        // Совпадение в регионе
        if (purchase.region.toLowerCase().includes(queryLower)) {
            relevance += 35;
        }
        
        // Совпадение в номере закупки
        if (purchase.number && purchase.number.includes(query)) {
            relevance += 80;
        }
        
        // Дополнительные бонусы
        if (purchase.status === 'active') relevance += 10;
        if (purchase.price > 1000000) relevance += 5;
        
        return relevance;
    }
    
    // Получение подсветки для поиска
    getSearchHighlights(purchase, query) {
        const highlights = [];
        const queryLower = query.toLowerCase();
        
        // Подсветка в заголовке
        if (purchase.title.toLowerCase().includes(queryLower)) {
            highlights.push({
                field: 'title',
                text: this.highlightQuery(purchase.title, query)
            });
        }
        
        // Подсветка в описании
        if (purchase.description.toLowerCase().includes(queryLower)) {
            const desc = purchase.description;
            const index = desc.toLowerCase().indexOf(queryLower);
            const start = Math.max(0, index - 50);
            const end = Math.min(desc.length, index + query.length + 50);
            const excerpt = desc.substring(start, end);
            highlights.push({
                field: 'description',
                text: this.highlightQuery(excerpt, query)
            });
        }
        
        return highlights;
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
        results.forEach((result, index) => {
            const purchase = result.purchase;
            html += `
                <div class="search-result-item" data-id="${purchase.id}">
                    <div class="result-header">
                        <h3 class="result-title">
                            <a href="#" onclick="yandexSearch.showPurchaseDetails(${purchase.id})">
                                ${result.highlights.find(h => h.field === 'title')?.text || purchase.title}
                            </a>
                        </h3>
                        <div class="result-meta">
                            <span class="result-number">${purchase.number || '№' + purchase.id}</span>
                            <span class="result-status ${purchase.status}">${purchase.status === 'active' ? 'Активна' : 'Завершена'}</span>
                        </div>
                    </div>
                    <div class="result-content">
                        ${result.highlights.find(h => h.field === 'description')?.text || purchase.description.substring(0, 200) + '...'}
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
    
    // Добавление в историю поиска
    addToSearchHistory(query) {
        if (!this.searchHistory.includes(query)) {
            this.searchHistory.unshift(query);
            this.searchHistory = this.searchHistory.slice(0, 20); // Максимум 20 запросов
            localStorage.setItem('zakupkiSearchHistory', JSON.stringify(this.searchHistory));
        }
    }
    
    // Загрузка истории поиска
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
    
    // Обновление URL поиска
    updateSearchURL(query) {
        const url = new URL(window.location);
        url.searchParams.set('q', query);
        window.history.pushState({}, '', url);
    }
    
    // Показ деталей закупки
    showPurchaseDetails(purchaseId) {
        // Реализация показа деталей закупки
        console.log('Показать детали закупки:', purchaseId);
    }
    
    // Добавление в избранное
    addToFavorites(purchaseId) {
        // Реализация добавления в избранное
        console.log('Добавить в избранное:', purchaseId);
    }
    
    // Подача заявки
    submitApplication(purchaseId) {
        // Реализация подачи заявки
        console.log('Подать заявку:', purchaseId);
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

// Инициализация поиска
let yandexSearch;
document.addEventListener('DOMContentLoaded', () => {
    yandexSearch = new YandexStyleSearch();
});
