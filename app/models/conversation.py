from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    seller_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="cascade"), nullable=False, index=True)
    
    last_message_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now, nullable=False)

    __table_args__ = (
        UniqueConstraint("listing_id", "buyer_id", name="unique_conversation"),
        CheckConstraint("buyer_id!=seller_id", name="check_different_users")

    )

    #relationships
    listing = relationship("Listing", back_populates="conversations")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="conversation_as_seller")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="conversation_as_buyer")
    messages = relationship("Message", back_populates="conversation", cascade="all delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, listing_id={self.listing_id}, buyer_id={self.buyer_id})>"