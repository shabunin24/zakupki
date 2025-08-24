import { useEffect, useState } from 'react'
import { TelegramWebApp, User } from '../types'

declare global {
  interface Window {
    Telegram: {
      WebApp: TelegramWebApp
    }
  }
}

export const useTelegramApp = () => {
  const [webApp, setWebApp] = useState<TelegramWebApp | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [isReady, setIsReady] = useState(false)

  const initApp = () => {
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp
      setWebApp(tg)
      
      // Инициализация приложения
      tg.ready()
      tg.expand()
      
      // Получение данных пользователя
      if (tg.initDataUnsafe?.user) {
        setUser(tg.initDataUnsafe.user)
      }
      
      setIsReady(true)
      
      console.log('Telegram WebApp инициализирован:', tg)
    } else {
      console.warn('Telegram WebApp не найден, запуск в режиме разработки')
      setIsReady(true)
    }
  }

  const showMainButton = (text: string, callback: () => void) => {
    if (webApp) {
      webApp.mainButton.setText(text)
      webApp.mainButton.onClick(callback)
      webApp.mainButton.show()
    }
  }

  const hideMainButton = () => {
    if (webApp) {
      webApp.mainButton.hide()
    }
  }

  const showBackButton = (callback: () => void) => {
    if (webApp) {
      webApp.backButton.onClick(callback)
      webApp.backButton.isVisible = true
    }
  }

  const hideBackButton = () => {
    if (webApp) {
      webApp.backButton.isVisible = false
    }
  }

  const closeApp = () => {
    if (webApp) {
      webApp.close()
    }
  }

  return {
    webApp,
    user,
    isReady,
    initApp,
    showMainButton,
    hideMainButton,
    showBackButton,
    hideBackButton,
    closeApp,
  }
}
