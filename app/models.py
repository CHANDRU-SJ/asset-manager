from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func
from app.database import Base


class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    purchase_date = Column(Date, nullable=False)
    serial_number = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())