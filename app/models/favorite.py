from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="cascade"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("listing_id", "user_id", name="unique_favorite"),
    )

    #relationships
    user = relationship("User", back_populates="favorites")
    listing = relationship("Listing", back_populates="favorites")

    def __repr__(self):
        return f"<Favortie(user_id={self.user_id}, listing_id={self.listing_id})>"