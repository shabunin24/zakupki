import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useTelegramApp } from './hooks/useTelegramApp'
import { PurchaseProvider } from './contexts/PurchaseContext'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import SearchPage from './pages/SearchPage'
import FavoritesPage from './pages/FavoritesPage'
import PurchaseDetailPage from './pages/PurchaseDetailPage'
import ProfilePage from './pages/ProfilePage'
import BottomNavigation from './components/BottomNavigation'

function App() {
  const { initApp } = useTelegramApp()

  useEffect(() => {
    initApp()
  }, [initApp])

  return (
    <PurchaseProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header />
          <main className="pb-20">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/favorites" element={<FavoritesPage />} />
              <Route path="/purchase/:id" element={<PurchaseDetailPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </main>
          <BottomNavigation />
        </div>
      </Router>
    </PurchaseProvider>
  )
}

export default App
