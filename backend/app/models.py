from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    message = Column(String(2000), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
