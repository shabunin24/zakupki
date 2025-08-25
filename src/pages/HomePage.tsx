import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, TrendingUp, Clock, Star } from 'lucide-react'
import { usePurchase } from '../contexts/PurchaseContext'
import PurchaseCard from '../components/PurchaseCard'
import { Purchase } from '../types'

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const { state, dispatch } = usePurchase()
  const [recentPurchases, setRecentPurchases] = useState<Purchase[]>([])

  // Моковые данные для демонстрации
  useEffect(() => {
    const mockPurchases: Purchase[] = [
      {
        id: '1',
        title: 'Поставка офисной мебели для администрации города',
        description: 'Комплексная поставка офисной мебели включая столы, стулья, шкафы и аксессуары',
        price: 1800000,
        region: 'Москва',
        customer: 'Администрация города Москвы',
        status: 'published',
        procurementMethod: 'electronic_auction',
        okpd2: '31.01.10',
        deadline: '2024-02-15',
        documents: [
          { id: '1', name: 'Техническое задание.pdf', url: '#', type: 'pdf', size: 1024, uploadedAt: '2024-01-01' }
        ],
        createdAt: '2024-01-01',
        updatedAt: '2024-01-01',
        isFavorite: false,
      },
      {
        id: '2',
        title: 'Услуги по техническому обслуживанию ИТ-инфраструктуры',
        description: 'Комплексное техническое обслуживание серверов, сетевого оборудования и программного обеспечения',
        price: 3200000,
        region: 'Санкт-Петербург',
        customer: 'ГБУ "Центр информационных технологий"',
        status: 'bidding',
        procurementMethod: 'tender',
        okpd2: '62.01.11',
        deadline: '2024-02-20',
        documents: [
          { id: '2', name: 'Техническое задание.docx', url: '#', type: 'docx', size: 2048, uploadedAt: '2024-01-02' },
          { id: '3', name: 'Форма заявки.xlsx', url: '#', type: 'xlsx', size: 512, uploadedAt: '2024-01-02' }
        ],
        createdAt: '2024-01-02',
        updatedAt: '2024-01-02',
        isFavorite: true,
      },
      {
        id: '3',
        title: 'Проведение обучающих семинаров по работе с ЕИС',
        description: 'Организация и проведение обучающих мероприятий для государственных служащих',
        price: 950000,
        region: 'Новосибирск',
        customer: 'Министерство цифрового развития',
        status: 'evaluation',
        procurementMethod: 'request_proposals',
        okpd2: '85.59.11',
        deadline: '2024-02-10',
        documents: [
          { id: '4', name: 'Программа обучения.pdf', url: '#', type: 'pdf', size: 1536, uploadedAt: '2024-01-03' }
        ],
        createdAt: '2024-01-03',
        updatedAt: '2024-01-03',
        isFavorite: false,
      },
    ]

    dispatch({ type: 'SET_PURCHASES', payload: mockPurchases })
    setRecentPurchases(mockPurchases.slice(0, 5))
  }, [dispatch])

  const quickActions = [
    { icon: Search, label: 'Поиск закупок', action: () => navigate('/search') },
    { icon: Star, label: 'Избранное', action: () => navigate('/favorites') },
    { icon: Clock, label: 'Срочные', action: () => navigate('/search?status=bidding') },
    { icon: TrendingUp, label: 'Популярные', action: () => navigate('/search?sort=popular') },
  ]

  return (
    <div className="px-4 py-6 space-y-6">
      {/* Приветствие */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Добро пожаловать в ГосЗакупки
        </h2>
        <p className="text-gray-600">
          Найдите интересующие вас закупки и следите за их статусом
        </p>
      </div>

      {/* Быстрые действия */}
      <div className="grid grid-cols-2 gap-3">
        {quickActions.map(({ icon: Icon, label, action }) => (
          <button
            key={label}
            onClick={action}
            className="flex flex-col items-center p-4 bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-sm transition-all"
          >
            <Icon size={24} className="text-primary-600 mb-2" />
            <span className="text-sm font-medium text-gray-700">{label}</span>
          </button>
        ))}
      </div>

      {/* Поиск */}
      <div className="relative">
        <input
          type="text"
          placeholder="Поиск закупок..."
          className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          onClick={() => navigate('/search')}
          readOnly
        />
        <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
      </div>

      {/* Последние закупки */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Последние закупки</h3>
          <button
            onClick={() => navigate('/search')}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Все закупки →
          </button>
        </div>
        
        <div className="space-y-3">
          {recentPurchases.map((purchase) => (
            <PurchaseCard key={purchase.id} purchase={purchase} />
          ))}
        </div>
      </div>

      {/* Статистика */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Статистика</h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">{state.purchases.length}</div>
            <div className="text-sm text-gray-600">Всего закупок</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{state.favorites.length}</div>
            <div className="text-sm text-gray-600">В избранном</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage
