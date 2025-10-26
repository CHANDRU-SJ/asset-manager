import os
import pytest
from pathlib import Path
from datetime import date

@pytest.mark.asyncio(loop_scope="session")
async def test_generate_pdf_report(client):
    # Ensure at least one asset exists
    await client.post("/assets/", json={
        "name": "MacBook Pro",
        "category": "Electronics",
        "purchase_date": str(date.today()),
        "serial_number": "SN-123455"
    })

    response = await client.get("/assets/report/pdf")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "file_path" in data
    assert data["message"] == "Report generation started"

    # Verify the file path (exists or pending creation)
    path = Path(data["file_path"])
    assert path.parent.name == "reports"
    
     # Clean up the file if it exists
    try:
        if path.exists():
            path.unlink()  # deletes the file
    except Exception as e:
        pytest.fail(f"Failed to clean up generated PDF file: {e}")
