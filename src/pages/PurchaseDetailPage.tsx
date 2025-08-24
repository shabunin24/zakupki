import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useTelegramApp } from '../hooks/useTelegramApp'
import { usePurchase } from '../contexts/PurchaseContext'
import { Heart, MapPin, Calendar, DollarSign, Building, FileText, Download, Share2, ArrowLeft } from 'lucide-react'
import { Purchase } from '../types'

const PurchaseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { showBackButton, hideBackButton } = useTelegramApp()
  const { state, dispatch, isFavorite } = usePurchase()
  const [purchase, setPurchase] = useState<Purchase | null>(null)

  useEffect(() => {
    if (id) {
      const foundPurchase = state.purchases.find(p => p.id === id)
      if (foundPurchase) {
        setPurchase(foundPurchase)
      }
    }
  }, [id, state.purchases])

  useEffect(() => {
    showBackButton(() => navigate(-1))
    return () => hideBackButton()
  }, [showBackButton, hideBackButton, navigate])

  if (!purchase) {
    return (
      <div className="px-4 py-12 text-center">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          Закупка не найдена
        </h2>
        <button
          onClick={() => navigate(-1)}
          className="btn-primary"
        >
          Назад
        </button>
      </div>
    )
  }

  const formatPrice = (price: number) => {
    if (price >= 1000000) {
      return `${(price / 1000000).toFixed(1)} млн ₽`
    } else if (price >= 1000) {
      return `${(price / 1000).toFixed(0)} тыс ₽`
    }
    return `${price} ₽`
  }

  const getStatusColor = (status: string) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-700',
      published: 'bg-blue-100 text-blue-700',
      bidding: 'bg-yellow-100 text-yellow-700',
      evaluation: 'bg-purple-100 text-purple-700',
      awarded: 'bg-green-100 text-green-700',
      completed: 'bg-green-100 text-green-700',
      cancelled: 'bg-red-100 text-red-700',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-700'
  }

  const getStatusText = (status: string) => {
    const texts = {
      draft: 'Черновик',
      published: 'Опубликовано',
      bidding: 'Подача заявок',
      evaluation: 'Рассмотрение',
      awarded: 'Присуждено',
      completed: 'Завершено',
      cancelled: 'Отменено',
    }
    return texts[status as keyof typeof texts] || status
  }

  const getMethodText = (method: string) => {
    const texts = {
      electronic_auction: 'Электронный аукцион',
      tender: 'Открытый конкурс',
      request_quotes: 'Запрос котировок',
      request_proposals: 'Запрос предложений',
      limited_competition: 'Конкурс с ограниченным участием',
    }
    return texts[method as keyof typeof texts] || method
  }

  const handleToggleFavorite = () => {
    dispatch({ type: 'TOGGLE_FAVORITE', payload: purchase.id })
  }

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: purchase.title,
        text: `Закупка: ${purchase.title}`,
        url: window.location.href,
      })
    }
  }

  const handleDownloadDocument = (document: any) => {
    // В реальном приложении здесь будет логика скачивания
    console.log('Скачивание документа:', document.name)
  }

  return (
    <div className="pb-20">
      {/* Заголовок */}
      <div className="bg-white border-b border-gray-200 px-4 py-4">
        <div className="flex items-center space-x-3 mb-3">
          <button
            onClick={() => navigate(-1)}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft size={20} />
          </button>
          <div className="flex-1">
            <h1 className="text-lg font-semibold text-gray-900 line-clamp-2">
              {purchase.title}
            </h1>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleShare}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Share2 size={20} />
            </button>
            <button
              onClick={handleToggleFavorite}
              className={`p-2 rounded-lg transition-colors ${
                isFavorite(purchase.id)
                  ? 'text-red-500 hover:text-red-600 bg-red-50'
                  : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Heart size={20} fill={isFavorite(purchase.id) ? 'currentColor' : 'none'} />
            </button>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(purchase.status)}`}>
            {getStatusText(purchase.status)}
          </span>
          <span className="text-sm text-gray-500">
            ID: {purchase.id}
          </span>
        </div>
      </div>

      <div className="px-4 py-6 space-y-6">
        {/* Основная информация */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Основная информация</h2>
          
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <DollarSign size={20} className="text-primary-600 mt-0.5" />
              <div>
                <div className="text-sm text-gray-600">Начальная цена</div>
                <div className="text-lg font-semibold text-gray-900">{formatPrice(purchase.price)}</div>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <MapPin size={20} className="text-primary-600 mt-0.5" />
              <div>
                <div className="text-sm text-gray-600">Регион</div>
                <div className="font-medium text-gray-900">{purchase.region}</div>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <Building size={20} className="text-primary-600 mt-0.5" />
              <div>
                <div className="text-sm text-gray-600">Заказчик</div>
                <div className="font-medium text-gray-900">{purchase.customer}</div>
              </div>
            </div>
            
            <div className="flex items-start space-x-3">
              <Calendar size={20} className="text-primary-600 mt-0.5" />
              <div>
                <div className="text-sm text-gray-600">Дедлайн подачи заявок</div>
                <div className="font-medium text-gray-900">
                  {new Date(purchase.deadline).toLocaleDateString('ru-RU', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Детали закупки */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Детали закупки</h2>
          
          <div className="space-y-4">
            <div>
              <div className="text-sm text-gray-600 mb-1">Способ закупки</div>
              <div className="font-medium text-gray-900">{getMethodText(purchase.procurementMethod)}</div>
            </div>
            
            <div>
              <div className="text-sm text-gray-600 mb-1">ОКПД2</div>
              <div className="font-medium text-gray-900">{purchase.okpd2}</div>
            </div>
            
            <div>
              <div className="text-sm text-gray-600 mb-1">Описание</div>
              <div className="text-gray-900">{purchase.description}</div>
            </div>
          </div>
        </div>

        {/* Документы */}
        {purchase.documents.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Документы</h2>
            
            <div className="space-y-3">
              {purchase.documents.map((document) => (
                <div key={document.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <FileText size={20} className="text-primary-600" />
                    <div>
                      <div className="font-medium text-gray-900">{document.name}</div>
                      <div className="text-sm text-gray-500">
                        {(document.size / 1024).toFixed(1)} КБ • {document.type.toUpperCase()}
                      </div>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => handleDownloadDocument(document)}
                    className="p-2 text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition-colors"
                  >
                    <Download size={20} />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Действия */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Действия</h2>
          
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={handleToggleFavorite}
              className={`p-3 rounded-lg font-medium transition-colors ${
                isFavorite(purchase.id)
                  ? 'bg-red-50 text-red-700 border border-red-200 hover:bg-red-100'
                  : 'bg-gray-50 text-gray-700 border border-gray-200 hover:bg-gray-100'
              }`}
            >
              {isFavorite(purchase.id) ? 'Убрать из избранного' : 'Добавить в избранное'}
            </button>
            
            <button
              onClick={handleShare}
              className="p-3 bg-primary-50 text-primary-700 border border-primary-200 rounded-lg font-medium hover:bg-primary-100 transition-colors"
            >
              Поделиться
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PurchaseDetailPage
