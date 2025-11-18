import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Client, Trainer, Waitlist, Review

app = FastAPI(title="Athly Global API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Athly Global Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ---------------- Athly Global Endpoints ----------------

# Seed featured trainers (for demo)
FEATURED_SEED: List[dict] = [
    {
        "full_name": "Ava Kim",
        "email": "ava.kim@example.com",
        "password": "hashed",
        "specializations": ["HIIT", "Strength"],
        "bio": "Former national sprinter turned elite HIIT coach.",
        "certifications": ["NASM-CPT"],
        "verified": True,
        "languages": ["English", "Korean"],
        "timezone": "Asia/Seoul",
        "price_30": 35,
        "price_60": 60,
        "rating": 4.9,
        "reviews_count": 128,
        "photo_url": "https://images.unsplash.com/photo-1554151228-14d9def656e4",
    },
    {
        "full_name": "Luca Moretti",
        "email": "luca.moretti@example.com",
        "password": "hashed",
        "specializations": ["Strength", "Hypertrophy"],
        "bio": "Evidence-based strength programming for busy pros.",
        "certifications": ["ACE-CPT"],
        "verified": True,
        "languages": ["English", "Italian"],
        "timezone": "Europe/Rome",
        "price_30": 30,
        "price_60": 55,
        "rating": 4.9,
        "reviews_count": 204,
        "photo_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c",
    },
    {
        "full_name": "Priya Desai",
        "email": "priya.desai@example.com",
        "password": "hashed",
        "specializations": ["Yoga", "Mobility"],
        "bio": "200-hr RYT with a focus on mindful mobility.",
        "certifications": ["RYT-200"],
        "verified": True,
        "languages": ["English", "Hindi"],
        "timezone": "Asia/Kolkata",
        "price_30": 25,
        "price_60": 45,
        "rating": 5.0,
        "reviews_count": 312,
        "photo_url": "https://images.unsplash.com/photo-1544717305-2782549b5136",
    },
    {
        "full_name": "Diego Ramirez",
        "email": "diego.ramirez@example.com",
        "password": "hashed",
        "specializations": ["Functional", "Conditioning"],
        "bio": "High performance conditioning for athletes.",
        "certifications": ["NSCA-CSCS"],
        "verified": True,
        "languages": ["English", "Spanish"],
        "timezone": "America/Mexico_City",
        "price_30": 28,
        "price_60": 50,
        "rating": 4.8,
        "reviews_count": 167,
        "photo_url": "https://images.unsplash.com/photo-1556157382-97eda2d62296",
    },
    {
        "full_name": "Sofia Petrova",
        "email": "sofia.petrova@example.com",
        "password": "hashed",
        "specializations": ["Pilates", "Core"],
        "bio": "Pilates-focused core strength and posture.",
        "certifications": ["STOTT"],
        "verified": True,
        "languages": ["English", "Russian"],
        "timezone": "Europe/Sofia",
        "price_30": 27,
        "price_60": 48,
        "rating": 4.9,
        "reviews_count": 190,
        "photo_url": "https://images.unsplash.com/photo-1552374196-c4e7ffc6e126",
    },
]

class WaitlistIn(BaseModel):
    email: str

@app.post("/waitlist")
def join_waitlist(payload: WaitlistIn):
    try:
        doc_id = create_document("waitlist", Waitlist(email=payload.email))
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ClientSignup(BaseModel):
    full_name: str
    email: str
    password: str
    goals: List[str] = []
    timezone: Optional[str] = None

@app.post("/client/signup")
def client_signup(data: ClientSignup):
    try:
        doc = Client(
            full_name=data.full_name,
            email=data.email,
            password=data.password,
            goals=data.goals,
            timezone=data.timezone,
        )
        doc_id = create_document("client", doc)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TrainerSignupStep1(BaseModel):
    full_name: str
    email: str
    password: str

class TrainerSignupStep2(BaseModel):
    certifications: List[str]
    verified: bool = False

class TrainerSignupStep3(BaseModel):
    specializations: List[str]
    bio: Optional[str] = None

class TrainerSignupStep4(BaseModel):
    price_30: Optional[float] = None
    price_60: Optional[float] = None
    timezone: Optional[str] = None

@app.post("/trainer/signup")
def trainer_signup(
    step1: TrainerSignupStep1,
    step2: TrainerSignupStep2,
    step3: TrainerSignupStep3,
    step4: TrainerSignupStep4,
):
    try:
        trainer = Trainer(
            full_name=step1.full_name,
            email=step1.email,
            password=step1.password,
            certifications=step2.certifications,
            verified=step2.verified,
            specializations=step3.specializations,
            bio=step3.bio,
            price_30=step4.price_30,
            price_60=step4.price_60,
            timezone=step4.timezone,
        )
        doc_id = create_document("trainer", trainer)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SearchQuery(BaseModel):
    specialization: str
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    min_rating: float = 4.5

@app.post("/trainers/search")
def search_trainers(filters: SearchQuery):
    try:
        q = {"specializations": {"$in": [filters.specialization]}}
        if filters.price_min is not None or filters.price_max is not None:
            price_cond = {}
            if filters.price_min is not None:
                price_cond["$gte"] = filters.price_min
            if filters.price_max is not None:
                price_cond["$lte"] = filters.price_max
            # check both price_60 and price_30
            q["$or"] = [{"price_60": price_cond}, {"price_30": price_cond}]
        if filters.timezone:
            q["timezone"] = filters.timezone
        if filters.language:
            q["languages"] = {"$in": [filters.language]}
        if filters.min_rating:
            q["rating"] = {"$gte": filters.min_rating}

        results = get_documents("trainer", q, limit=20)
        # If DB empty, return seed
        if not results:
            return {"items": FEATURED_SEED}
        for r in results:
            r["_id"] = str(r["_id"])  # stringify ids
        return {"items": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trainers/featured")
def featured_trainers():
    try:
        # Try DB, fallback to seed
        items = get_documents("trainer", {"rating": {"$gte": 4.8}}, limit=5)
        if not items:
            return {"items": FEATURED_SEED}
        for r in items:
            r["_id"] = str(r["_id"])  # stringify ids
        return {"items": items}
    except Exception:
        return {"items": FEATURED_SEED}

@app.get("/schema")
def get_schema():
    # Expose schemas to the database viewer if needed
    return {
        "collections": [
            "client",
            "trainer",
            "review",
            "waitlist",
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
