from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    customer = Column(String(200), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    procurement_method = Column(String(100), nullable=False)
    okpd2 = Column(String(20), nullable=True)
    deadline = Column(DateTime, nullable=False)
    
    # Метаданные
    source_url = Column(String(500), nullable=True)
    source_name = Column(String(100), nullable=False)  # ЕИС, госзакупки.ру и т.д.
    external_id = Column(String(100), nullable=True)  # ID в исходной системе
    
    # Дополнительные поля
    contact_info = Column(JSON, nullable=True)
    requirements = Column(Text, nullable=True)
    evaluation_criteria = Column(Text, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Связи
    documents = relationship("Document", back_populates="purchase", cascade="all,delete-orphan")
    favorites = relationship("Favorite", back_populates="purchase", cascade="all,delete-orphan")
    
    def __repr__(self):
        return f"<Purchase(id={self.id}, title='{self.title[:50]}...', price={self.price})>"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    purchase_id = Column(String, ForeignKey("purchases.id"), nullable=False)
    name = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    purchase = relationship("Purchase", back_populates="documents")
    
    def __repr__(self):
        return f"<Document(id={self.id}, name='{self.name}')>"

class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)  # Telegram user ID
    purchase_id = Column(String, ForeignKey("purchases.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    purchase = relationship("Purchase", back_populates="favorites")
    
    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, purchase_id={self.purchase_id})>"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)  # Telegram user ID
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    language_code = Column(String(10), nullable=True)
    is_premium = Column(Boolean, default=False)
    
    # Настройки
    notification_settings = Column(JSON, default=dict)
    search_filters = Column(JSON, default=dict)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class ParserLog(Base):
    __tablename__ = "parser_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # success, error, running
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    items_processed = Column(Integer, default=0)
    items_added = Column(Integer, default=0)
    items_updated = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<ParserLog(source='{self.source_name}', status='{self.status}')>"
