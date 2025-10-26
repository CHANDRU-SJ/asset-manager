from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models import Asset
from app.schemas import AssetCreate


async def create_asset_db(db: AsyncSession, asset: AssetCreate):
    db_obj = Asset(**asset.model_dump())
    db.add(db_obj)

    try:
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except IntegrityError as e:
        await db.rollback()
        # Handle duplicate serial_number
        if "Duplicate entry" in str(e.orig) and "serial_number" in str(e.orig):
            raise HTTPException(
                status_code=400,
                detail=f"Asset with serial number '{asset.serial_number}' already exists."
            )
        # re-raise other integrity errors
        raise HTTPException(
            status_code=400,
            detail="Integrity error while updating asset."
        )


async def get_asset_db(db: AsyncSession, asset_id: int):
    return await db.get(Asset, asset_id)


async def list_assets_db(db: AsyncSession):
    result = await db.execute(select(Asset))
    return result.scalars().all()


async def update_asset_db(db: AsyncSession, asset_id: int, data: dict):
    obj = await db.get(Asset, asset_id)
    if not obj:
        return None
    
    for k, v in data.items():
        if v is not None:
            setattr(obj, k, v)

    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except IntegrityError as e:
        await db.rollback()
        # Handle duplicate serial_number
        if "Duplicate entry" in str(e.orig) and "serial_number" in str(e.orig):
            raise HTTPException(
                status_code=400,
                detail=f"Asset with serial number '{data.get('serial_number')}' already exists."
            )
        # re-raise other integrity errors
        raise HTTPException(
            status_code=400,
            detail="Integrity error while updating asset."
        )



async def delete_asset_db(db: AsyncSession, asset_id: int):
    obj = await db.get(Asset, asset_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True