import React from 'react'
import { useTelegramApp } from '../hooks/useTelegramApp'
import { usePurchase } from '../contexts/PurchaseContext'
import { User, Settings, Bell, Shield, HelpCircle, Info, LogOut, Heart, Clock, CheckCircle } from 'lucide-react'

const ProfilePage: React.FC = () => {
  const { user, webApp } = useTelegramApp()
  const { state } = usePurchase()

  const profileSections = [
    {
      title: 'Аккаунт',
      items: [
        { icon: User, label: 'Личные данные', action: () => console.log('Личные данные') },
        { icon: Settings, label: 'Настройки', action: () => console.log('Настройки') },
        { icon: Bell, label: 'Уведомления', action: () => console.log('Уведомления') },
      ]
    },
    {
      title: 'Приложение',
      items: [
        { icon: HelpCircle, label: 'Помощь', action: () => console.log('Помощь') },
        { icon: Info, label: 'О приложении', action: () => console.log('О приложении') },
        { icon: Shield, label: 'Политика конфиденциальности', action: () => console.log('Политика') },
      ]
    }
  ]

  const stats = [
    { icon: Heart, label: 'В избранном', value: state.favorites.length, color: 'text-red-600' },
    { icon: Clock, label: 'Активные', value: state.purchases.filter(p => p.status === 'bidding').length, color: 'text-yellow-600' },
    { icon: CheckCircle, label: 'Завершенные', value: state.purchases.filter(p => p.status === 'completed').length, color: 'text-green-600' },
  ]

  const handleLogout = () => {
    // В реальном приложении здесь будет логика выхода
    console.log('Выход из приложения')
  }

  return (
    <div className="px-4 py-6 space-y-6">
      {/* Профиль пользователя */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 text-center">
        <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <User size={32} className="text-primary-600" />
        </div>
        
        <h1 className="text-xl font-semibold text-gray-900 mb-2">
          {user ? `${user.firstName} ${user.lastName || ''}` : 'Пользователь'}
        </h1>
        
        {user?.username && (
          <p className="text-gray-600 mb-4">@{user.username}</p>
        )}
        
        <div className="text-sm text-gray-500">
          ID: {user?.id || 'Неизвестно'}
        </div>
      </div>

      {/* Статистика */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Статистика</h2>
        
        <div className="grid grid-cols-3 gap-4">
          {stats.map(({ icon: Icon, label, value, color }) => (
            <div key={label} className="text-center">
              <Icon size={24} className={`mx-auto mb-2 ${color}`} />
              <div className={`text-2xl font-bold ${color}`}>{value}</div>
              <div className="text-sm text-gray-600">{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Настройки */}
      {profileSections.map((section) => (
        <div key={section.title} className="bg-white rounded-lg border border-gray-200">
          <div className="px-4 py-3 border-b border-gray-100">
            <h3 className="font-semibold text-gray-900">{section.title}</h3>
          </div>
          
          <div className="divide-y divide-gray-100">
            {section.items.map(({ icon: Icon, label, action }) => (
              <button
                key={label}
                onClick={action}
                className="w-full px-4 py-3 flex items-center space-x-3 hover:bg-gray-50 transition-colors"
              >
                <Icon size={20} className="text-gray-600" />
                <span className="text-gray-900">{label}</span>
                <div className="ml-auto">
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </button>
            ))}
          </div>
        </div>
      ))}

      {/* Информация о приложении */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h3 className="font-semibold text-gray-900 mb-3">О приложении</h3>
        
        <div className="space-y-2 text-sm text-gray-600">
          <div>Версия: 1.0.0</div>
          <div>Платформа: {webApp?.platform || 'Web'}</div>
          <div>Telegram WebApp версия: {webApp?.version || 'Неизвестно'}</div>
        </div>
      </div>

      {/* Кнопка выхода */}
      <button
        onClick={handleLogout}
        className="w-full p-3 bg-red-50 text-red-700 border border-red-200 rounded-lg font-medium hover:bg-red-100 transition-colors flex items-center justify-center space-x-2"
      >
        <LogOut size={20} />
        <span>Выйти из приложения</span>
      </button>
    </div>
  )
}

export default ProfilePage
