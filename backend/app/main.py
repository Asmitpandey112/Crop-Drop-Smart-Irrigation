from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import fields, predictions

app = FastAPI(
    title="CropDrop API",
    description="AI-Powered Smart Irrigation & Water Optimization",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fields.router, prefix="/api/fields", tags=["Fields"])
app.include_router(predictions.router, prefix="/api", tags=["Predictions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CropDrop API prototype"}
