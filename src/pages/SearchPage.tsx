import React, { useState, useEffect } from 'react'
import { Search, Filter, X, ChevronDown } from 'lucide-react'
import { usePurchase } from '../contexts/PurchaseContext'
import PurchaseCard from '../components/PurchaseCard'
import { SearchFilters, PurchaseStatus, ProcurementMethod } from '../types'

const SearchPage: React.FC = () => {
  const { state, dispatch } = usePurchase()
  const [searchQuery, setSearchQuery] = useState('')
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState<SearchFilters>({})
  const [filteredPurchases, setFilteredPurchases] = useState(state.purchases)

  useEffect(() => {
    applyFilters()
  }, [filters, state.purchases])

  const applyFilters = () => {
    let filtered = [...state.purchases]

    // Поиск по тексту
    if (filters.query) {
      const query = filters.query.toLowerCase()
      filtered = filtered.filter(purchase =>
        purchase.title.toLowerCase().includes(query) ||
        purchase.description.toLowerCase().includes(query) ||
        purchase.customer.toLowerCase().includes(query)
      )
    }

    // Фильтр по региону
    if (filters.region) {
      filtered = filtered.filter(purchase => purchase.region === filters.region)
    }

    // Фильтр по цене
    if (filters.priceMin !== undefined) {
      filtered = filtered.filter(purchase => purchase.price >= filters.priceMin!)
    }
    if (filters.priceMax !== undefined) {
      filtered = filtered.filter(purchase => purchase.price <= filters.priceMax!)
    }

    // Фильтр по статусу
    if (filters.status && filters.status.length > 0) {
      filtered = filtered.filter(purchase => filters.status!.includes(purchase.status))
    }

    // Фильтр по способу закупки
    if (filters.procurementMethod && filters.procurementMethod.length > 0) {
      filtered = filtered.filter(purchase => 
        filters.procurementMethod!.includes(purchase.procurementMethod)
      )
    }

    setFilteredPurchases(filtered)
  }

  const handleSearch = () => {
    setFilters(prev => ({ ...prev, query: searchQuery }))
  }

  const clearFilters = () => {
    setFilters({})
    setSearchQuery('')
  }

  const regions = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']
  const statuses: PurchaseStatus[] = ['draft', 'published', 'bidding', 'evaluation', 'awarded', 'completed', 'cancelled']
  const methods: ProcurementMethod[] = ['electronic_auction', 'tender', 'request_quotes', 'request_proposals', 'limited_competition']

  const getStatusText = (status: PurchaseStatus) => {
    const texts = {
      draft: 'Черновик',
      published: 'Опубликовано',
      bidding: 'Подача заявок',
      evaluation: 'Рассмотрение',
      awarded: 'Присуждено',
      completed: 'Завершено',
      cancelled: 'Отменено',
    }
    return texts[status]
  }

  const getMethodText = (method: ProcurementMethod) => {
    const texts = {
      electronic_auction: 'Электронный аукцион',
      tender: 'Открытый конкурс',
      request_quotes: 'Запрос котировок',
      request_proposals: 'Запрос предложений',
      limited_competition: 'Конкурс с ограниченным участием',
    }
    return texts[method]
  }

  return (
    <div className="px-4 py-6 space-y-4">
      {/* Заголовок */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Поиск закупок</h1>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`p-2 rounded-lg transition-colors ${
            showFilters ? 'bg-primary-100 text-primary-700' : 'bg-gray-100 text-gray-600'
          }`}
        >
          <Filter size={20} />
        </button>
      </div>

      {/* Поиск */}
      <div className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Поиск по названию, описанию, заказчику..."
          className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <button
          onClick={handleSearch}
          className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-primary-600 text-white px-4 py-1 rounded-md text-sm font-medium hover:bg-primary-700"
        >
          Найти
        </button>
      </div>

      {/* Фильтры */}
      {showFilters && (
        <div className="bg-white rounded-lg border border-gray-200 p-4 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-900">Фильтры</h3>
            <button
              onClick={clearFilters}
              className="text-sm text-gray-500 hover:text-gray-700 flex items-center"
            >
              <X size={16} className="mr-1" />
              Очистить
            </button>
          </div>

          {/* Регион */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Регион</label>
            <select
              value={filters.region || ''}
              onChange={(e) => setFilters(prev => ({ ...prev, region: e.target.value || undefined }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Все регионы</option>
              {regions.map(region => (
                <option key={region} value={region}>{region}</option>
              ))}
            </select>
          </div>

          {/* Цена */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Цена от (₽)</label>
              <input
                type="number"
                value={filters.priceMin || ''}
                onChange={(e) => setFilters(prev => ({ ...prev, priceMin: e.target.value ? Number(e.target.value) : undefined }))}
                placeholder="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Цена до (₽)</label>
              <input
                type="number"
                value={filters.priceMax || ''}
                onChange={(e) => setFilters(prev => ({ ...prev, priceMax: e.target.value ? Number(e.target.value) : undefined }))}
                placeholder="∞"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          {/* Статус */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Статус</label>
            <div className="grid grid-cols-2 gap-2">
              {statuses.map(status => (
                <label key={status} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={filters.status?.includes(status) || false}
                    onChange={(e) => {
                      const currentStatuses = filters.status || []
                      if (e.target.checked) {
                        setFilters(prev => ({ ...prev, status: [...currentStatuses, status] }))
                      } else {
                        setFilters(prev => ({ ...prev, status: currentStatuses.filter(s => s !== status) }))
                      }
                    }}
                    className="mr-2 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="text-sm text-gray-700">{getStatusText(status)}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Способ закупки */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Способ закупки</label>
            <div className="grid grid-cols-1 gap-2">
              {methods.map(method => (
                <label key={method} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={filters.procurementMethod?.includes(method) || false}
                    onChange={(e) => {
                      const currentMethods = filters.procurementMethod || []
                      if (e.target.checked) {
                        setFilters(prev => ({ ...prev, procurementMethod: [...currentMethods, method] }))
                      } else {
                        setFilters(prev => ({ ...prev, procurementMethod: currentMethods.filter(m => m !== method) }))
                      }
                    }}
                    className="mr-2 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="text-sm text-gray-700">{getMethodText(method)}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Результаты */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Результаты поиска ({filteredPurchases.length})
          </h3>
          {Object.keys(filters).length > 0 && (
            <button
              onClick={clearFilters}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Очистить фильтры
            </button>
          )}
        </div>

        {filteredPurchases.length === 0 ? (
          <div className="text-center py-12">
            <Search size={48} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Ничего не найдено</h3>
            <p className="text-gray-500">
              Попробуйте изменить параметры поиска или фильтры
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredPurchases.map((purchase) => (
              <PurchaseCard key={purchase.id} purchase={purchase} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchPage
