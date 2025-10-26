from pydantic import BaseModel
from datetime import date
from typing import Optional


class AssetBase(BaseModel):
    name: str
    category: str
    purchase_date: date
    serial_number: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    purchase_date: Optional[date] = None
    serial_number: Optional[str] = None


class AssetOut(AssetBase):
    id: int
    class Config:
        from_attributes = True