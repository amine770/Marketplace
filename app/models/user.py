from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String,  unique=True, index=True ,nullable=False)
    hashed_password = Column(String, nullable=False)

    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True, index=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate= func.now(),
                        nullable=False)
    
    #relationships
    listings = relationship("Listing", back_populates="seller", cascade="all delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all delete-orphan")
    sent_messages = relationship("Message", back_populates="sender", cascade="all delete-orphan")
    conversation_as_buyer = relationship("Conversation", 
                                         back_populates="buyer", 
                                         foreign_keys= "Conversation.buyer_id",
                                         cascade="all delete-orphan"),
    
    conversation_as_seller = relationship("Conversation",
                                          back_populates="seller",
                                          foreign_keys="Conversation.seller_id",
                                          cascade="all delete_orphan"
                                          )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

    