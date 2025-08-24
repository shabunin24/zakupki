import React from 'react'
import { Heart, Trash2, Share2, Calendar } from 'lucide-react'
import { usePurchase } from '../contexts/PurchaseContext'
import PurchaseCard from '../components/PurchaseCard'

const FavoritesPage: React.FC = () => {
  const { getFavoritePurchases, state } = usePurchase()
  const favoritePurchases = getFavoritePurchases()

  const handleRemoveAllFavorites = () => {
    // В реальном приложении здесь будет API вызов
    favoritePurchases.forEach(purchase => {
      // dispatch({ type: 'TOGGLE_FAVORITE', payload: purchase.id })
    })
  }

  const handleShareFavorites = () => {
    // В реальном приложении здесь будет логика шаринга
    if (navigator.share) {
      navigator.share({
        title: 'Мои избранные закупки',
        text: `У меня ${favoritePurchases.length} избранных закупок в приложении ГосЗакупки`,
        url: window.location.href,
      })
    }
  }

  if (favoritePurchases.length === 0) {
    return (
      <div className="px-4 py-12 text-center">
        <Heart size={64} className="mx-auto text-gray-300 mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          У вас пока нет избранных закупок
        </h2>
        <p className="text-gray-600 mb-6">
          Добавляйте интересующие закупки в избранное, чтобы следить за их статусом
        </p>
        <button
          onClick={() => window.history.back()}
          className="btn-primary"
        >
          Найти закупки
        </button>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 space-y-4">
      {/* Заголовок */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Избранное</h1>
          <p className="text-gray-600">
            {favoritePurchases.length} закупок в избранном
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleShareFavorites}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            title="Поделиться"
          >
            <Share2 size={20} />
          </button>
          <button
            onClick={handleRemoveAllFavorites}
            className="p-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
            title="Убрать все из избранного"
          >
            <Trash2 size={20} />
          </button>
        </div>
      </div>

      {/* Статистика */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h3 className="font-semibold text-gray-900 mb-3">Статистика избранного</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-primary-600">{favoritePurchases.length}</div>
            <div className="text-sm text-gray-600">Всего</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-yellow-600">
              {favoritePurchases.filter(p => p.status === 'bidding').length}
            </div>
            <div className="text-sm text-gray-600">Активные</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">
              {favoritePurchases.filter(p => p.status === 'awarded').length}
            </div>
            <div className="text-sm text-gray-600">Завершенные</div>
          </div>
        </div>
      </div>

      {/* Срочные закупки */}
      {favoritePurchases.filter(p => p.status === 'bidding').length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Calendar size={20} className="text-yellow-600" />
            <h3 className="font-semibold text-yellow-800">Срочные закупки</h3>
          </div>
          <p className="text-yellow-700 text-sm">
            У вас есть {favoritePurchases.filter(p => p.status === 'bidding').length} закупок в статусе "Подача заявок"
          </p>
        </div>
      )}

      {/* Список избранных закупок */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Избранные закупки
        </h3>
        <div className="space-y-3">
          {favoritePurchases.map((purchase) => (
            <PurchaseCard key={purchase.id} purchase={purchase} />
          ))}
        </div>
      </div>

      {/* Действия */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h3 className="font-semibold text-gray-900 mb-3">Действия</h3>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => window.history.back()}
            className="btn-secondary"
          >
            Найти еще закупки
          </button>
          <button
            onClick={handleShareFavorites}
            className="btn-primary"
          >
            Поделиться
          </button>
        </div>
      </div>
    </div>
  )
}

export default FavoritesPage
