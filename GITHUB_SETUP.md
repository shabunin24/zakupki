# 🔐 Настройка GitHub токена

## 📋 Что нужно сделать

Для работы с GitHub API в некоторых скриптах проекта требуется Personal Access Token.

## 🚀 Создание токена

1. **Перейдите в настройки GitHub:**
   - Откройте [GitHub Settings](https://github.com/settings)
   - Войдите в свой аккаунт

2. **Создайте новый токен:**
   - В левом меню выберите "Developer settings" → "Personal access tokens" → "Tokens (classic)"
   - Нажмите "Generate new token (classic)"

3. **Настройте токен:**
   - **Note:** `Zakupki Bot Token`
   - **Expiration:** Выберите срок действия (рекомендуется 90 дней)
   - **Scopes:** Отметьте `repo` (полный доступ к репозиториям)

4. **Скопируйте токен:**
   - Нажмите "Generate token"
   - **⚠️ ВАЖНО:** Скопируйте токен сразу! Он больше не будет показан

## 🔧 Настройка в проекте

### Вариант 1: Переменные окружения (рекомендуется)

Создайте файл `.env` в корне проекта:

```bash
# .env
GITHUB_TOKEN=ghp_your_token_here
```

### Вариант 2: Прямая замена в коде

Замените `YOUR_GITHUB_TOKEN_HERE` на ваш токен в файлах:

- `enable-github-pages.py` (строка 12)
- `monitor-github-pages.py` (строка 13)

```python
TOKEN = "ghp_your_actual_token_here"
```

## 📱 Использование

После настройки токена вы сможете:

- **Включить GitHub Pages:** `python enable-github-pages.py`
- **Мониторить статус:** `python monitor-github-pages.py`

## 🔒 Безопасность

- **Никогда не коммитьте токен в Git!**
- Используйте `.env` файл и добавьте его в `.gitignore`
- Регулярно обновляйте токен
- Используйте минимально необходимые права доступа

## 🚨 Если токен скомпрометирован

1. Немедленно отзовите токен в GitHub
2. Создайте новый токен
3. Обновите все места использования
4. Проверьте логи на предмет несанкционированного доступа

## 📚 Полезные ссылки

- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Pages](https://pages.github.com/)
