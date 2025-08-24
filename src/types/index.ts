export interface Purchase {
  id: string
  title: string
  description: string
  price: number
  region: string
  customer: string
  status: PurchaseStatus
  procurementMethod: ProcurementMethod
  okpd2: string
  deadline: string
  documents: Document[]
  createdAt: string
  updatedAt: string
  isFavorite: boolean
}

export type PurchaseStatus = 
  | 'draft'
  | 'published'
  | 'bidding'
  | 'evaluation'
  | 'awarded'
  | 'completed'
  | 'cancelled'

export type ProcurementMethod = 
  | 'electronic_auction'
  | 'tender'
  | 'request_quotes'
  | 'request_proposals'
  | 'limited_competition'

export interface Document {
  id: string
  name: string
  url: string
  type: string
  size: number
  uploadedAt: string
}

export interface SearchFilters {
  query?: string
  region?: string
  okpd2?: string
  priceMin?: number
  priceMax?: number
  status?: PurchaseStatus[]
  procurementMethod?: ProcurementMethod[]
  customer?: string
}

export interface User {
  id: number
  username?: string
  firstName: string
  lastName?: string
  languageCode: string
  isPremium?: boolean
  allowsWriteToPm?: boolean
}

export interface TelegramWebApp {
  initData: string
  initDataUnsafe: {
    query_id: string
    user: User
    receiver: User
    chat: any
    chat_type: string
    chat_instance: string
    start_param: string
    can_send_after: number
    auth_date: number
    hash: string
  }
  version: string
  platform: string
  colorScheme: 'light' | 'dark'
  themeParams: {
    bg_color: string
    text_color: string
    hint_color: string
    link_color: string
    button_color: string
    button_text_color: string
  }
  isExpanded: boolean
  viewportHeight: number
  viewportStableHeight: number
  headerColor: string
  backgroundColor: string
  isClosingConfirmationEnabled: boolean
  backButton: {
    isVisible: boolean
    onClick: (callback: () => void) => void
  }
  mainButton: {
    text: string
    color: string
    textColor: string
    isVisible: boolean
    isProgressVisible: boolean
    isActive: boolean
    onClick: (callback: () => void) => void
    show: () => void
    hide: () => void
    enable: () => void
    disable: () => void
    showProgress: (leaveActive?: boolean) => void
    hideProgress: () => void
    setText: (text: string) => void
    setParams: (params: any) => void
  }
  ready: () => void
  expand: () => void
  close: () => void
}
