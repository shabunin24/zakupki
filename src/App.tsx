import { useEffect, useState } from 'react'

// Определяем, запущено ли приложение в Telegram
const isTelegramWebApp = () => {
  return window.Telegram && window.Telegram.WebApp
}

// Компонент для отображения в браузере
const BrowserVersion = () => (
  <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
    <h1 style={{ color: '#2563eb', fontSize: '24px', marginBottom: '16px' }}>
      🖥️ ГосЗакупки - Версия для браузера
    </h1>
    
    <div style={{ 
      backgroundColor: '#f0f9ff', 
      border: '1px solid #0ea5e9', 
      borderRadius: '8px', 
      padding: '16px',
      marginBottom: '16px'
    }}>
      <p style={{ color: '#0c4a6e', margin: '0' }}>
        ✅ Это версия для разработки в браузере
      </p>
    </div>
    
    <div style={{ 
      backgroundColor: '#fef3c7', 
      border: '1px solid #f59e0b', 
      borderRadius: '8px', 
      padding: '16px'
    }}>
      <h3 style={{ color: '#92400e', margin: '0 0 8px 0' }}>📱 Для тестирования в Telegram:</h3>
      <ul style={{ color: '#92400e', margin: '0', paddingLeft: '20px' }}>
        <li>Используйте ngrok для HTTPS</li>
        <li>Настройте бота через @BotFather</li>
        <li>Добавьте URL в Mini App</li>
      </ul>
    </div>
  </div>
)

// Компонент для отображения в Telegram
const TelegramVersion = () => {
  const [user, setUser] = useState<any>(null)
  
  useEffect(() => {
    if (isTelegramWebApp()) {
      const tg = window.Telegram.WebApp
      tg.ready()
      tg.expand()
      
      if (tg.initDataUnsafe?.user) {
        setUser(tg.initDataUnsafe.user)
      }
      
      console.log('Telegram WebApp инициализирован:', tg)
    }
  }, [])
  
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#8b5cf6', fontSize: '24px', marginBottom: '16px' }}>
        📱 ГосЗакупки - Telegram Mini App
      </h1>
      
      <div style={{ 
        backgroundColor: '#f3e8ff', 
        border: '1px solid #a855f7', 
        borderRadius: '8px', 
        padding: '16px',
        marginBottom: '16px'
      }}>
        <p style={{ color: '#581c87', margin: '0' }}>
          ✅ Запущено в Telegram WebApp!
        </p>
      </div>
      
      {user && (
        <div style={{ 
          backgroundColor: '#ecfdf5', 
          border: '1px solid #10b981', 
          borderRadius: '8px', 
          padding: '16px',
          marginBottom: '16px'
        }}>
          <h3 style={{ color: '#065f46', margin: '0 0 8px 0' }}>👤 Пользователь:</h3>
          <p style={{ color: '#065f46', margin: '0' }}>
            {user.firstName} {user.lastName}
          </p>
        </div>
      )}
      
      <div style={{ 
        backgroundColor: '#fef3c7', 
        border: '1px solid #f59e0b', 
        borderRadius: '8px', 
        padding: '16px'
      }}>
        <h3 style={{ color: '#92400e', margin: '0 0 8px 0' }}>🎯 Функции:</h3>
        <ul style={{ color: '#92400e', margin: '0', paddingLeft: '20px' }}>
          <li>Поиск закупок</li>
          <li>Избранное</li>
          <li>Уведомления</li>
          <li>Профиль пользователя</li>
        </ul>
      </div>
    </div>
  )
}

function App() {
  const [isTelegram, setIsTelegram] = useState(false)
  
  useEffect(() => {
    console.log('App: проверяем окружение...')
          const telegram = isTelegramWebApp()
      setIsTelegram(Boolean(telegram))
    console.log('Telegram WebApp:', telegram)
  }, [])

  console.log('App: рендерится, isTelegram:', isTelegram)

  return (
    <div>
      {isTelegram ? <TelegramVersion /> : <BrowserVersion />}
      
      <div style={{ 
        marginTop: '20px', 
        padding: '12px', 
        backgroundColor: '#f3f4f6', 
        borderRadius: '6px',
        fontSize: '14px',
        color: '#374151',
        textAlign: 'center'
      }}>
        <strong>Окружение:</strong> {isTelegram ? 'Telegram WebApp' : 'Браузер'} | 
        <strong>Время:</strong> {new Date().toLocaleTimeString()}
      </div>
    </div>
  )
}

export default App
