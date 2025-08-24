import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Heart, MapPin, Calendar, DollarSign, Building } from 'lucide-react'
import { Purchase } from '../types'
import { usePurchase } from '../contexts/PurchaseContext'

interface PurchaseCardProps {
  purchase: Purchase
}

const PurchaseCard: React.FC<PurchaseCardProps> = ({ purchase }) => {
  const navigate = useNavigate()
  const { dispatch, isFavorite } = usePurchase()
  const favorite = isFavorite(purchase.id)

  const handleToggleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation()
    dispatch({ type: 'TOGGLE_FAVORITE', payload: purchase.id })
  }

  const handleCardClick = () => {
    navigate(`/purchase/${purchase.id}`)
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

  return (
    <div 
      className="card cursor-pointer hover:shadow-md transition-shadow"
      onClick={handleCardClick}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 text-sm leading-tight mb-2 line-clamp-2">
            {purchase.title}
          </h3>
          
          <div className="space-y-2">
            <div className="flex items-center text-xs text-gray-600">
              <MapPin size={14} className="mr-1" />
              <span>{purchase.region}</span>
            </div>
            
            <div className="flex items-center text-xs text-gray-600">
              <Building size={14} className="mr-1" />
              <span className="truncate">{purchase.customer}</span>
            </div>
            
            <div className="flex items-center text-xs text-gray-600">
              <DollarSign size={14} className="mr-1" />
              <span className="font-medium text-gray-700">{formatPrice(purchase.price)}</span>
            </div>
            
            <div className="flex items-center text-xs text-gray-600">
              <Calendar size={14} className="mr-1" />
              <span>До {new Date(purchase.deadline).toLocaleDateString('ru-RU')}</span>
            </div>
          </div>
        </div>
        
        <button
          onClick={handleToggleFavorite}
          className={`ml-2 p-1 rounded-full transition-colors ${
            favorite 
              ? 'text-red-500 hover:text-red-600' 
              : 'text-gray-400 hover:text-gray-600'
          }`}
        >
          <Heart size={16} fill={favorite ? 'currentColor' : 'none'} />
        </button>
      </div>
      
      <div className="flex items-center justify-between">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(purchase.status)}`}>
          {getStatusText(purchase.status)}
        </span>
        
        <span className="text-xs text-gray-500">
          {purchase.documents.length} документов
        </span>
      </div>
    </div>
  )
}

export default PurchaseCard
