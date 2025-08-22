// Автоматический тест функционала Telegram Mini App ГосЗакупки
console.log('🧪 Запуск автоматического тестирования...');

// Глобальные переменные для тестирования
let testResults = {
    passed: 0,
    failed: 0,
    total: 0,
    details: []
};

// Функция для записи результатов теста
function recordTest(name, passed, details = '') {
    testResults.total++;
    if (passed) {
        testResults.passed++;
        console.log(`✅ ${name} - ПРОШЕЛ`);
    } else {
        testResults.failed++;
        console.log(`❌ ${name} - НЕ ПРОШЕЛ: ${details}`);
    }
    
    testResults.details.push({
        name,
        passed,
        details
    });
}

// Тест 1: Проверка инициализации
function testInitialization() {
    console.log('\n🔍 Тест 1: Инициализация приложения');
    
    // Проверяем основные переменные
    const hasMockPurchases = typeof mockPurchases !== 'undefined' && mockPurchases.length > 0;
    recordTest('База данных закупок', hasMockPurchases, `Найдено ${mockPurchases?.length || 0} закупок`);
    
    const hasFunctions = typeof searchPurchases === 'function' && 
                        typeof showPurchaseDetails === 'function' &&
                        typeof addToFavorites === 'function';
    recordTest('Основные функции', hasFunctions, 'Проверка наличия ключевых функций');
    
    const hasConfig = typeof botToken !== 'undefined' && botToken.length > 0;
    recordTest('Конфигурация бота', hasConfig, `Токен: ${botToken?.substring(0, 10)}...`);
}

// Тест 2: Тестирование поиска
function testSearch() {
    console.log('\n🔍 Тест 2: Система поиска');
    
    // Тест поиска по названию
    const titleResults = searchPurchases('компьютер');
    const titlePassed = titleResults.length > 0 && titleResults[0].title.toLowerCase().includes('компьютер');
    recordTest('Поиск по названию', titlePassed, `Найдено: ${titleResults.length} результатов`);
    
    // Тест поиска по категории
    const categoryResults = searchPurchases('услуги');
    const categoryPassed = categoryResults.length > 0 && categoryResults.some(p => p.category === 'Услуги');
    recordTest('Поиск по категории', categoryPassed, `Найдено: ${categoryResults.length} результатов`);
    
    // Тест поиска по региону
    const regionResults = searchPurchases('москва');
    const regionPassed = regionResults.length > 0 && regionResults.some(p => p.region === 'Москва');
    recordTest('Поиск по региону', regionPassed, `Найдено: ${regionResults.length} результатов`);
    
    // Тест поиска с фильтрами
    const filteredResults = searchPurchases('', { category: 'Товары', region: 'Москва' });
    const filterPassed = filteredResults.length > 0 && 
                        filteredResults.every(p => p.category === 'Товары' && p.region === 'Москва');
    recordTest('Поиск с фильтрами', filterPassed, `Найдено: ${filteredResults.length} результатов`);
}

// Тест 3: Тестирование избранного
function testFavorites() {
    console.log('\n⭐ Тест 3: Система избранного');
    
    const initialCount = favorites.length;
    
    // Добавляем закупку в избранное
    addToFavorites(1);
    const afterAdd = favorites.length;
    const addPassed = afterAdd > initialCount;
    recordTest('Добавление в избранное', addPassed, `Было: ${initialCount}, стало: ${afterAdd}`);
    
    // Проверяем, что закупка уже в избранном
    const alreadyExists = favorites.includes(1);
    recordTest('Проверка дублирования', alreadyExists, 'Закупка в избранном');
    
    // Убираем из избранного
    removeFromFavorites(1);
    const afterRemove = favorites.length;
    const removePassed = afterRemove === initialCount;
    recordTest('Удаление из избранного', removePassed, `Было: ${afterAdd}, стало: ${afterRemove}`);
}

// Тест 4: Тестирование заявок
function testApplications() {
    console.log('\n📝 Тест 4: Система заявок');
    
    const initialCount = userApplications.length;
    
    // Подаем заявку
    submitApplication(1);
    const afterSubmit = userApplications.length;
    const submitPassed = afterSubmit > initialCount;
    recordTest('Подача заявки', submitPassed, `Было: ${initialCount}, стало: ${afterSubmit}`);
    
    // Проверяем детали заявки
    const application = userApplications.find(app => app.purchaseId === 1);
    const detailsPassed = application && application.status === 'submitted';
    recordTest('Детали заявки', detailsPassed, `Статус: ${application?.status}`);
    
    // Отменяем заявку
    const beforeCancel = userApplications.length;
    cancelApplication(application.id);
    const afterCancel = userApplications.length;
    const cancelPassed = afterCancel < beforeCancel;
    recordTest('Отмена заявки', cancelPassed, `Было: ${beforeCancel}, стало: ${afterCancel}`);
}

// Тест 5: Тестирование форматирования
function testFormatting() {
    console.log('\n🔧 Тест 5: Форматирование данных');
    
    // Тест форматирования цены
    const priceFormatted = formatPrice(2500000, 'RUB');
    const pricePassed = priceFormatted.includes('₽') && priceFormatted.includes('2');
    recordTest('Форматирование цены', pricePassed, `Результат: ${priceFormatted}`);
    
    // Тест форматирования даты
    const dateFormatted = formatDate('2024-12-15');
    const datePassed = dateFormatted.length > 0 && dateFormatted.includes('2024');
    recordTest('Форматирование даты', datePassed, `Результат: ${dateFormatted}`);
}

// Тест 6: Тестирование модальных окон
function testModals() {
    console.log('\n🪟 Тест 6: Модальные окна');
    
    // Тест показа модального окна
    const modalContent = 'Тестовое содержимое';
    showModal('Тест', modalContent);
    
    const modal = document.querySelector('.modal');
    const modalShown = modal && modal.classList.contains('active');
    recordTest('Показ модального окна', modalShown, 'Модальное окно отображается');
    
    // Закрываем модальное окно
    if (modal) {
        const closeBtn = modal.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.click();
            setTimeout(() => {
                const modalClosed = !modal.classList.contains('active');
                recordTest('Закрытие модального окна', modalClosed, 'Модальное окно закрыто');
            }, 100);
        }
    }
}

// Тест 7: Тестирование уведомлений
function testNotifications() {
    console.log('\n🔔 Тест 7: Система уведомлений');
    
    // Тест показа уведомления
    showNotification('Тестовое уведомление');
    
    const notification = document.querySelector('div[style*="position: fixed"]');
    const notificationShown = notification && notification.textContent.includes('Тестовое уведомление');
    recordTest('Показ уведомления', notificationShown, 'Уведомление отображается');
    
    // Ждем исчезновения уведомления
    setTimeout(() => {
        const notificationGone = !document.querySelector('div[style*="position: fixed"]');
        recordTest('Автоскрытие уведомления', notificationGone, 'Уведомление скрыто');
    }, 3100);
}

// Тест 8: Тестирование навигации
function testNavigation() {
    console.log('\n🧭 Тест 8: Система навигации');
    
    // Тест переключения вкладок
    const initialTab = currentTab;
    switchTab('search');
    const searchTabActive = currentTab === 'search';
    recordTest('Переключение на вкладку поиска', searchTabActive, `Текущая вкладка: ${currentTab}`);
    
    // Возвращаемся на главную
    switchTab('home');
    const homeTabActive = currentTab === 'home';
    recordTest('Возврат на главную', homeTabActive, `Текущая вкладка: ${currentTab}`);
}

// Тест 9: Тестирование данных
function testDataIntegrity() {
    console.log('\n📊 Тест 9: Целостность данных');
    
    // Проверяем структуру закупок
    const validPurchases = mockPurchases.every(p => 
        p.id && p.title && p.price && p.region && p.category && p.deadline
    );
    recordTest('Структура данных закупок', validPurchases, 'Все обязательные поля заполнены');
    
    // Проверяем уникальность ID
    const ids = mockPurchases.map(p => p.id);
    const uniqueIds = new Set(ids).size === ids.length;
    recordTest('Уникальность ID закупок', uniqueIds, `Всего: ${ids.length}, уникальных: ${new Set(ids).size}`);
    
    // Проверяем корректность цен
    const validPrices = mockPurchases.every(p => p.price > 0 && typeof p.price === 'number');
    recordTest('Корректность цен', validPrices, 'Все цены положительные числа');
}

// Тест 10: Тестирование производительности
function testPerformance() {
    console.log('\n⚡ Тест 10: Производительность');
    
    const startTime = performance.now();
    
    // Выполняем поиск по всем закупкам
    for (let i = 0; i < 100; i++) {
        searchPurchases('тест');
    }
    
    const endTime = performance.now();
    const searchTime = endTime - startTime;
    const performancePassed = searchTime < 1000; // Должно выполняться менее чем за 1 секунду
    
    recordTest('Производительность поиска', performancePassed, `Время: ${searchTime.toFixed(2)}ms`);
}

// Главная функция тестирования
function runAllTests() {
    console.log('🚀 ЗАПУСК АВТОМАТИЧЕСКОГО ТЕСТИРОВАНИЯ');
    console.log('=' * 60);
    
    // Запускаем все тесты
    testInitialization();
    testSearch();
    testFavorites();
    testApplications();
    testFormatting();
    testModals();
    testNotifications();
    testNavigation();
    testDataIntegrity();
    testPerformance();
    
    // Итоговый отчет
    console.log('\n📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ');
    console.log('=' * 60);
    console.log(`✅ ПРОШЕЛ: ${testResults.passed}`);
    console.log(`❌ НЕ ПРОШЕЛ: ${testResults.failed}`);
    console.log(`📈 ВСЕГО: ${testResults.total}`);
    console.log(`📊 УСПЕШНОСТЬ: ${((testResults.passed / testResults.total) * 100).toFixed(1)}%`);
    
    // Детали неудачных тестов
    if (testResults.failed > 0) {
        console.log('\n❌ ДЕТАЛИ НЕУДАЧНЫХ ТЕСТОВ:');
        testResults.details
            .filter(test => !test.passed)
            .forEach(test => {
                console.log(`   • ${test.name}: ${test.details}`);
            });
    }
    
    // Рекомендации
    console.log('\n💡 РЕКОМЕНДАЦИИ:');
    if (testResults.passed === testResults.total) {
        console.log('🎉 Все тесты пройдены! Приложение готово к использованию.');
    } else if (testResults.passed >= testResults.total * 0.8) {
        console.log('⚠️  Большинство тестов пройдено. Незначительные проблемы требуют исправления.');
    } else {
        console.log('❌ Много проблем. Требуется серьезная доработка.');
    }
    
    return testResults;
}

// Автоматический запуск тестов после загрузки страницы
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(runAllTests, 2000); // Ждем 2 секунды для полной инициализации
    });
} else {
    setTimeout(runAllTests, 2000);
}

// Экспорт для ручного запуска
window.runZakupkiTests = runAllTests;
