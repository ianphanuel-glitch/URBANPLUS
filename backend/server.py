from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
import uuid
from datetime import datetime, timezone
import sys

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from spatial_analysis.nairobi_data import generate_nairobi_sample_data, convert_to_geojson
from indicators.urban_metrics import calculate_all_indicators
from ai_planner.insights import generate_planning_insights
from ai_planner.recommendations import generate_specific_recommendations
from reports.pdf_generator import generate_city_report

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="UrbanPulse AI")

# Create router with /api prefix
api_router = APIRouter(prefix="/api")

# Models
class CityData(BaseModel):
    city_name: str
    layers: Dict[str, Dict]
    
class IndicatorsResponse(BaseModel):
    indicators: Dict
    city: str

class AIInsightsRequest(BaseModel):
    indicators: Dict
    model: Optional[str] = "gpt-5.2"

# Routes
@api_router.get("/")
async def root():
    return {"message": "UrbanPulse AI - Urban Planning Intelligence Platform"}

@api_router.get("/cities")
async def get_available_cities():
    """Get list of available cities"""
    return {
        "cities": [
            {
                "id": "nairobi",
                "name": "Nairobi, Kenya",
                "population": 4500000,
                "area_km2": 696,
                "available": True
            }
        ]
    }

@api_router.get("/city/{city_id}/data")
async def get_city_data(city_id: str):
    """Get spatial data for a city"""
    if city_id != "nairobi":
        raise HTTPException(status_code=404, detail="City not found")
    
    # Generate Nairobi data
    data = generate_nairobi_sample_data()
    
    # Convert to GeoJSON
    return {
        "city": "nairobi",
        "layers": {
            "residential": convert_to_geojson(data['residential']),
            "commercial": convert_to_geojson(data['commercial']),
            "facilities": convert_to_geojson(data['facilities']),
            "roads": convert_to_geojson(data['roads'])
        }
    }

@api_router.get("/city/{city_id}/indicators")
async def get_city_indicators(city_id: str):
    """Calculate urban indicators for a city"""
    if city_id != "nairobi":
        raise HTTPException(status_code=404, detail="City not found")
    
    # Generate data and calculate indicators
    data = generate_nairobi_sample_data()
    indicators = calculate_all_indicators(data)
    
    return {
        "city": "nairobi",
        "indicators": indicators
    }

@api_router.post("/ai/insights")
async def get_ai_insights(request: AIInsightsRequest):
    """Generate AI-powered planning insights"""
    try:
        insights = await generate_planning_insights(
            indicators=request.indicators,
            model=request.model
        )
        return insights
    except Exception as e:
        logging.error(f"Error generating AI insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)