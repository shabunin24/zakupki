import React, { createContext, useContext, useReducer, ReactNode } from 'react'
import { Purchase, SearchFilters } from '../types'

interface PurchaseState {
  purchases: Purchase[]
  favorites: string[]
  searchFilters: SearchFilters
  isLoading: boolean
  error: string | null
}

type PurchaseAction =
  | { type: 'SET_PURCHASES'; payload: Purchase[] }
  | { type: 'ADD_PURCHASE'; payload: Purchase }
  | { type: 'UPDATE_PURCHASE'; payload: Purchase }
  | { type: 'REMOVE_PURCHASE'; payload: string }
  | { type: 'TOGGLE_FAVORITE'; payload: string }
  | { type: 'SET_FAVORITES'; payload: string[] }
  | { type: 'SET_SEARCH_FILTERS'; payload: SearchFilters }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }

const initialState: PurchaseState = {
  purchases: [],
  favorites: [],
  searchFilters: {},
  isLoading: false,
  error: null,
}

const purchaseReducer = (state: PurchaseState, action: PurchaseAction): PurchaseState => {
  switch (action.type) {
    case 'SET_PURCHASES':
      return {
        ...state,
        purchases: action.payload,
        isLoading: false,
        error: null,
      }
    case 'ADD_PURCHASE':
      return {
        ...state,
        purchases: [...state.purchases, action.payload],
      }
    case 'UPDATE_PURCHASE':
      return {
        ...state,
        purchases: state.purchases.map(p => 
          p.id === action.payload.id ? action.payload : p
        ),
      }
    case 'REMOVE_PURCHASE':
      return {
        ...state,
        purchases: state.purchases.filter(p => p.id !== action.payload),
        favorites: state.favorites.filter(id => id !== action.payload),
      }
    case 'TOGGLE_FAVORITE':
      const isFavorite = state.favorites.includes(action.payload)
      return {
        ...state,
        favorites: isFavorite
          ? state.favorites.filter(id => id !== action.payload)
          : [...state.favorites, action.payload],
        purchases: state.purchases.map(p =>
          p.id === action.payload
            ? { ...p, isFavorite: !isFavorite }
            : p
        ),
      }
    case 'SET_FAVORITES':
      return {
        ...state,
        favorites: action.payload,
      }
    case 'SET_SEARCH_FILTERS':
      return {
        ...state,
        searchFilters: action.payload,
      }
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      }
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      }
    default:
      return state
  }
}

interface PurchaseContextType {
  state: PurchaseState
  dispatch: React.Dispatch<PurchaseAction>
  getFavoritePurchases: () => Purchase[]
  isFavorite: (id: string) => boolean
}

const PurchaseContext = createContext<PurchaseContextType | undefined>(undefined)

export const PurchaseProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(purchaseReducer, initialState)

  const getFavoritePurchases = () => {
    return state.purchases.filter(p => state.favorites.includes(p.id))
  }

  const isFavorite = (id: string) => {
    return state.favorites.includes(id)
  }

  const value: PurchaseContextType = {
    state,
    dispatch,
    getFavoritePurchases,
    isFavorite,
  }

  return (
    <PurchaseContext.Provider value={value}>
      {children}
    </PurchaseContext.Provider>
  )
}

export const usePurchase = () => {
  const context = useContext(PurchaseContext)
  if (context === undefined) {
    throw new Error('usePurchase must be used within a PurchaseProvider')
  }
  return context
}
