from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from fastapi import Body

from app.utils.config import PDF_TITLE, REPORTS_DIR
from app.models import Asset
from app.schemas import AssetCreate, AssetUpdate, AssetOut
from app.crud import create_asset_db, get_asset_db, list_assets_db, update_asset_db, delete_asset_db
from app.database import get_db
from app.utils.pdf_generator import generate_table_pdf

router = APIRouter(prefix="/assets", tags=["assets"])

@router.post('/', response_model=AssetOut)
async def create_asset(asset: AssetCreate, db: AsyncSession = Depends(get_db)):
    return await create_asset_db(db, asset)


@router.get('/', response_model=list[AssetOut])
async def list_assets(db: AsyncSession = Depends(get_db)):
    return await list_assets_db(db)


@router.get('/{asset_id}', response_model=AssetOut)
async def get_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    asset = await get_asset_db(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.put('/{asset_id}', response_model=AssetOut)
async def update_asset(asset_id: int, payload: AssetUpdate = Body(..., embed=False), db: AsyncSession = Depends(get_db)):
    updated = await update_asset_db(db, asset_id, payload.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated


@router.delete('/{asset_id}')
async def delete_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_asset_db(db, asset_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"status": "deleted"}


@router.get('/report/pdf')
async def assets_report_pdf(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    assets = await list_assets_db(db)
    
    # generate PDF file path
    now = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    filepath = REPORTS_DIR / f"assets_report_{now}.pdf"
    
    exludes = ['serial_number', 'created_at']
    columns = [column.name for column in Asset.__table__.columns if column.name not in exludes]
    report_title = PDF_TITLE

    background_tasks.add_task(
        generate_table_pdf, 
        assets, 
        columns, 
        filepath,
        report_title
    )
    
    return {"message": "Report generation started", "file_path": str(filepath)}