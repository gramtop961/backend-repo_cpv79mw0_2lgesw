import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from schemas import Inquiry
from database import create_document

app = FastAPI(title="NOVA LUBRICANTS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "NOVA LUBRICANTS backend is running"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/company")
def company_profile():
    return {
        "name": "NOVA LUBRICANTS",
        "tagline": "Premium Oils & Greases for Every Machine",
        "about": (
            "NOVA LUBRICANTS manufactures high‑performance engine oils, industrial lubricants "
            "and specialty greases for cars, bikes, scooters, trucks, and heavy machinery like JCB."
        ),
        "years_in_business": 10,
        "certifications": ["ISO 9001:2015", "OEM Grade Approvals"],
        "locations": ["Manufacturing Unit", "PAN-India Dealer Network"],
    }

@app.get("/api/products")
def products():
    return {
        "categories": [
            {
                "key": "car",
                "title": "Car Engine Oils",
                "items": [
                    {"name": "5W-30 Fully Synthetic", "spec": "API SN/CF", "pack": "1L | 3.5L | 5L"},
                    {"name": "10W-40 Semi Synthetic", "spec": "API SN", "pack": "1L | 3L | 4L"},
                ],
            },
            {
                "key": "bike",
                "title": "Bike & 2T Oils",
                "items": [
                    {"name": "10W-30 4T", "spec": "JASO MA2", "pack": "900ml | 1L"},
                    {"name": "20W-40 4T", "spec": "JASO MA", "pack": "900ml | 1L"},
                ],
            },
            {
                "key": "activa",
                "title": "Scooter Oils",
                "items": [
                    {"name": "10W-30 Scooter Oil", "spec": "JASO MB", "pack": "800ml | 1L"}
                ],
            },
            {
                "key": "truck",
                "title": "Truck & Diesel Oils",
                "items": [
                    {"name": "15W-40 Diesel Engine Oil", "spec": "API CI-4+", "pack": "5L | 7.5L | 15L"},
                    {"name": "20W-50 Diesel Oil", "spec": "API CH-4", "pack": "5L | 15L | 50L"},
                ],
            },
            {
                "key": "jcb",
                "title": "Heavy Equipment & Greases",
                "items": [
                    {"name": "Lithium EP-2 Grease", "spec": "NLGI 2", "pack": "500g | 1kg | 18kg"},
                    {"name": "Hydraulic Oil AW-68", "spec": "Anti-wear", "pack": "5L | 20L | 210L"},
                ],
            },
        ]
    }

@app.post("/api/inquiries")
def create_inquiry(inquiry: Inquiry):
    try:
        doc_id = create_document("inquiry", inquiry)
        return {"success": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
