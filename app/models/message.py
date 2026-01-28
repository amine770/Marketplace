from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="cascade"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False, index=True)

    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("length(trim(content)) > 0 ", name="check_content_not_empty")
    )

    #relationships
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")

    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, sender_id={self.sender_id})>"


    