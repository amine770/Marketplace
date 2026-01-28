from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("User.id", ondelete="cascade"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("Category.id", ondelete="cascade"), nullable=False, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False, index=True)
    location = Column(String, nullable=False, index=True)

    status = Column(String, default="active", nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), 
                        server_default=func.now(),
                        onupdate=func.now(),
                        nullable=False)
    
    __table_args__ = (
        CheckConstraint("price > 0 ", name="check_price_positive"),
        CheckConstraint("status IN ('active', 'sold', 'deleted')", name="check_status_valid")
    )

    #relationships
    seller = relationship("User", back_populates="listings")
    category = relationship("Category", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all delete-orphan")
    conversations = relationship("Conversation", back_populates="listing", cascade="all delete-orphan")
    favorites = relationship("Favorite", back_populates="listing", cascade="all delete-orphan")

    def __repr__(self):
        return f"<Listing(id={self.id}, title={self.title})>"