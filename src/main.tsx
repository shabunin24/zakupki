import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

console.log('main.tsx: начало выполнения')

// Проверяем наличие элемента root
const rootElement = document.getElementById('root')
if (!rootElement) {
  console.error('❌ Элемент с id "root" не найден!')
  document.body.innerHTML = '<div style="padding: 20px; color: red;">Ошибка: элемент root не найден</div>'
} else {
  console.log('✅ Элемент root найден:', rootElement)
  
  try {
    console.log('🔧 Создаем React root...')
    const root = ReactDOM.createRoot(rootElement)
    
    console.log('🚀 Рендерим App компонент...')
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
    )
    
    console.log('✅ React приложение успешно запущено')
  } catch (error) {
    console.error('❌ Ошибка при запуске React:', error)
    rootElement.innerHTML = `<div style="padding: 20px; color: red;">Ошибка React: ${error}</div>`
  }
}
