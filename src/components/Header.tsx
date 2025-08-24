import React from 'react'
import { useTelegramApp } from '../hooks/useTelegramApp'
import { Search, Bell, Menu } from 'lucide-react'

const Header: React.FC = () => {
  const { user } = useTelegramApp()

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">Г</span>
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">ГосЗакупки</h1>
            {user && (
              <p className="text-sm text-gray-500">
                {user.firstName} {user.lastName}
              </p>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
            <Search size={20} />
          </button>
          <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
            <Bell size={20} />
          </button>
          <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
            <Menu size={20} />
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
