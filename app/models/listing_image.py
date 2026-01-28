from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class ListingImage(Base):
    __tablename__ = "listing_images"

    id = Column(Integer, primary_key=True, index=True)

    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="cascade"), nullable=False, index=True)

    image_url = Column(String, unique=True, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("listing_id", "display_order", name="unique_image_order"),
    )

    #relationships
    listing = relationship("Listing", back_populates="images")

    def __repr__(self):
        return f"<ListingImage(id={self.id}, image_url={self.image_url})>"