# UrbanPulse AI

### 🏙️ Urban & Regional Planning Intelligence Platform

**From urban analysis to investment decisions.**

UrbanPulse AI is a **decision-support system for urban and regional planning** that combines **geospatial analysis, AI reasoning, and policy-aware analytics** to help cities **plan smarter, invest better, and justify infrastructure decisions with confidence**.

The platform is designed for **rapidly urbanizing cities**, with a strong focus on **African urban contexts**, where data gaps, infrastructure pressure, and equity challenges demand transparent and explainable planning tools.

---

## Why UrbanPulse AI?

Urban planning decisions involve complex **trade-offs between cost, impact, equity, and time**.  
Most tools stop at visualization or static analysis.

UrbanPulse AI goes further by enabling planners to:

- Compare multiple infrastructure investment scenarios
- Understand trade-offs between planning options
- Quantify cost, beneficiaries, and accessibility gains
- Generate **policy-ready PDF reports**
- Maintain accountability through **explainable AI**

---

![Urban Planning Dashboard](https://images.unsplash.com/photo-1693902997450-7e912c0d3554?w=1200&h=400&fit=crop)

## 🎯 Key Features

### 1. Interactive Urban Map
- **Multi-layer visualization** with OpenStreetMap data
- Toggle layers: Residential, Commercial, Industrial, Roads, Public Facilities
- Dark-mode optimized CartoDB tiles
- Smooth pan, zoom, and hover interactions
- Real-time spatial data rendering

### 2. Urban Indicators Engine
Automatically computes critical planning metrics:
- **Population Density**: Real-time density calculations by zone
- **Land Use Ratio**: Built-up vs open land distribution
- **Road Density & Connectivity**: Infrastructure mapping
- **Service Accessibility Index**: Healthcare and education proximity
- **Green Space Coverage**: Environmental sustainability metrics

### 3. AI Planning Insights 🤖
Powered by GPT-5.2 (OpenAI), Claude Sonnet 4.5, or Gemini 3 Flash:
- Interprets spatial indicators with urban planning expertise
- Flags critical issues: over-concentration, infrastructure stress, service inequality
- Generates actionable recommendations with priority levels
- Context-aware analysis for African urbanization patterns

### 4. Professional Futuristic UI/UX
- **Midnight Command** design theme
- Glassmorphism effects with backdrop blur
- Data-first dashboard with grid-based layouts
- Rajdhani typography for technical aesthetic
- Cyan/Emerald neon accents on deep blue/charcoal base
- Responsive charts and visualizations

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **GeoPandas & Shapely**: Spatial analysis and GIS operations
- **Motor (AsyncIO MongoDB)**: Database for future data persistence
- **emergentintegrations**: Universal LLM integration (OpenAI/Claude/Gemini)
- **Modular Architecture**: Separate modules for spatial analysis, indicators, and AI planning

### Frontend
- **React 19**: Modern UI library
- **Leaflet & react-leaflet**: Interactive mapping
- **Recharts**: Data visualization
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Icon system
- **Sonner**: Toast notifications

### Data
- **Nairobi Sample Dataset**: Real urban zones, facilities, and infrastructure
- Configurable for other cities

## 📁 Project Structure

```
urbanpulse-ai/
├── backend/
│   ├── server.py                  # Main FastAPI application
│   ├── spatial_analysis/
│   │   ├── __init__.py
│   │   └── nairobi_data.py       # GeoJSON data generation
│   ├── indicators/
│   │   ├── __init__.py
│   │   └── urban_metrics.py      # Indicator calculations
│   ├── ai_planner/
│   │   ├── __init__.py
│   │   └── insights.py           # AI insights generation
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.css             # Global styles + design system
│   │   ├── App.css
│   │   └── components/
│   │       ├── Dashboard.js      # Main dashboard controller
│   │       ├── UrbanMap.js       # Leaflet map component
│   │       ├── MetricCard.js     # Indicator display cards
│   │       ├── LayerToggle.js    # Map layer controls
│   │       ├── IndicatorCharts.js # Recharts visualizations
│   │       └── AIInsightsPanel.js # AI recommendations panel
│   ├── package.json
│   └── .env
├── design_guidelines.json         # Complete design system
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ & Yarn
- MongoDB (provided in environment)

### Installation

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd frontend
yarn install
```

3. **Environment Variables**

Backend `.env`:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CORS_ORIGINS=*
EMERGENT_LLM_KEY=sk-emergent-XXXXXX
```

Frontend `.env`:
```
REACT_APP_BACKEND_URL=https://your-domain.com
```

### Running the Application

**Backend:**
```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend:**
```bash
cd frontend
yarn start
```

Access the dashboard at `http://localhost:3000`

## 📊 API Endpoints

### City Data
- `GET /api/cities` - List available cities
- `GET /api/city/{city_id}/data` - Get spatial GeoJSON data
- `GET /api/city/{city_id}/indicators` - Get calculated urban indicators

### AI Insights
- `POST /api/ai/insights` - Generate AI planning recommendations
  ```json
  {
    "indicators": { /* indicator data */ },
    "model": "gpt-5.2" // or "claude-sonnet-4-5-20250929" or "gemini-3-flash-preview"
  }
  ```

## 🧠 Urban Planning Concepts

### Population Density
Measures people per square kilometer. Critical for:
- Infrastructure planning
- Resource allocation
- Service distribution

**Nairobi Context**: Ranges from 2,500 (Karen) to 45,000 (Kibera) people/km²

### Service Accessibility Index
Proximity-based score (0-100) measuring access to:
- Healthcare facilities (60% weight)
- Educational institutions (40% weight)

Calculated using 5km service radius and population-weighted ratios.

### Land Use Balance
Percentage of built-up area (residential + commercial) vs. open land.
- Optimal: 40-60% built-up for sustainable urban growth
- Nairobi: ~11.58% (room for planned development)

### Road Density
Kilometers of roads per square kilometer of city area.
- Indicates connectivity and mobility
- Critical for economic activity

### Green Space Coverage
Percentage of area designated for parks, forests, and recreational spaces.
- WHO recommends 9m² per capita minimum
- Critical for air quality, mental health, and climate resilience

## 🤖 AI Insights System

### How It Works
1. **Data Aggregation**: Collects all urban indicators
2. **Context Building**: Formats data with urban planning context
3. **LLM Analysis**: Sends to GPT-5.2/Claude/Gemini with expert system prompt
4. **Issue Detection**: AI identifies critical planning challenges
5. **Recommendation Generation**: Creates actionable, prioritized solutions

### Example Insights

**Issue:**
> "Kibera shows population density of 45,000 people/km² with accessibility score of 0.89/100, indicating severe healthcare infrastructure deficit."

**Recommendation:**
> "Establish 2-3 community health centers within Kibera's core zones. Target locations within 1.5km of highest density clusters. Estimated impact: +15 accessibility score, serving 112,500 residents."

## 🌍 Nairobi Dataset

### Included Zones
- **Residential**: Westlands, Kibera, Eastleigh, Karen, Parklands, Embakasi, Lavington, Kasarani
- **Commercial**: CBD, Westlands Business District, Industrial Area, Kilimani
- **Facilities**: Hospitals (Kenyatta, Nairobi, Aga Khan), Universities, Schools
- **Infrastructure**: Major roads (Uhuru Highway, Mombasa Road, Thika Road, Waiyaki Way, Ngong Road)

### Data Sources
- Population estimates: Kenya National Bureau of Statistics
- Facility locations: OpenStreetMap contributors
- Zone boundaries: Simplified polygons for demo purposes

## 🔄 Extending to Other Cities

1. **Create city data module**:
```python
# spatial_analysis/city_name_data.py
def generate_city_data():
    # Return GeoDataFrames for residential, commercial, facilities, roads
    pass
```

2. **Update API endpoints** in `server.py`
3. **Add city to frontend selector** in `Dashboard.js`

## 🎨 Design System

Complete design guidelines available in `/design_guidelines.json`:
- Typography: Rajdhani (headings), Inter (body), JetBrains Mono (data)
- Colors: Slate 950 background, Cyan (#06b6d4) primary, Emerald (#10b981) secondary
- Components: Glassmorphic cards, neon glows, hover micro-animations
- Layout: Control Room grid (sidebar + map + analytics panel)

## 📈 Future Roadmap

### Phase 1.1 - Enhanced Analysis
- [ ] Real-time data integration (traffic, weather, air quality)
- [ ] PDF report generation
- [ ] Historical trend analysis
- [ ] Comparative city benchmarking

### Phase 2.0 - Collaboration
- [ ] Multi-user support
- [ ] Annotation and commenting system
- [ ] Project workspace management
- [ ] Role-based access control

### Phase 3.0 - Advanced AI
- [ ] Scenario modeling ("what-if" analysis)
- [ ] Predictive analytics for urban growth
- [ ] Automated zoning recommendations
- [ ] Integration with city planning databases

## 🤝 Contributing

This is a smart-city research platform. Contributions welcome:
- City datasets for African metropoles
- Additional urban indicators
- UI/UX improvements
- Performance optimizations

## 📝 License

MIT License - Built for urban planners and policymakers worldwide.

## 🙏 Acknowledgments

- OpenStreetMap contributors
- Kenya National Bureau of Statistics
- CartoDB for dark map tiles
- Emergent Labs for LLM infrastructure

---

**Built with ❤️ for Africa's urban future**

*UrbanPulse AI - The City's Central Nervous System*
