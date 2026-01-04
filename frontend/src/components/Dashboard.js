import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapPin, Activity, Building2, Route, Trees, Sparkles, AlertTriangle, TrendingUp, X } from 'lucide-react';
import UrbanMap from './UrbanMap';
import MetricCard from './MetricCard';
import LayerToggle from './LayerToggle';
import IndicatorCharts from './IndicatorCharts';
import AIInsightsPanel from './AIInsightsPanel';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const [cityData, setCityData] = useState(null);
  const [indicators, setIndicators] = useState(null);
  const [aiInsights, setAiInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeLayers, setActiveLayers] = useState({
    residential: true,
    commercial: true,
    facilities: true,
    roads: true
  });
  const [selectedCity] = useState('nairobi');
  const [showAIPanel, setShowAIPanel] = useState(false);
  const [generatingInsights, setGeneratingInsights] = useState(false);

  useEffect(() => {
    loadCityData();
  }, [selectedCity]);

  const loadCityData = async () => {
    try {
      setLoading(true);
      
      // Load spatial data
      const dataResponse = await axios.get(`${API}/city/${selectedCity}/data`);
      setCityData(dataResponse.data);
      
      // Load indicators
      const indicatorsResponse = await axios.get(`${API}/city/${selectedCity}/indicators`);
      setIndicators(indicatorsResponse.data.indicators);
      
      setLoading(false);
      toast.success('City data loaded successfully');
    } catch (error) {
      console.error('Error loading city data:', error);
      toast.error('Failed to load city data');
      setLoading(false);
    }
  };

  const generateAIInsights = async () => {
    if (!indicators) return;
    
    try {
      setGeneratingInsights(true);
      const response = await axios.post(`${API}/ai/insights`, {
        indicators: indicators,
        model: 'gpt-5.2'
      });
      
      setAiInsights(response.data);
      setShowAIPanel(true);
      toast.success('AI insights generated');
    } catch (error) {
      console.error('Error generating insights:', error);
      toast.error('Failed to generate AI insights');
    } finally {
      setGeneratingInsights(false);
    }
  };

  const toggleLayer = (layer) => {
    setActiveLayers(prev => ({
      ...prev,
      [layer]: !prev[layer]
    }));
  };

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-slate-950">
        <div className="text-center">
          <Activity className="w-12 h-12 text-cyan-500 animate-spin mx-auto mb-4" />
          <p className="text-slate-300 font-rajdhani text-lg">Loading Urban Intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500 to-emerald-500 flex items-center justify-center">
              <MapPin className="w-6 h-6 text-slate-950" />
            </div>
            <div>
              <h1 className="text-2xl font-bold font-rajdhani tracking-tight uppercase text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-emerald-400" data-testid="app-title">
                UrbanPulse AI
              </h1>
              <p className="text-xs text-slate-500 font-rajdhani uppercase tracking-wider">Nairobi Urban Intelligence</p>
            </div>
          </div>
          
          <button
            onClick={generateAIInsights}
            disabled={generatingInsights}
            className="flex items-center gap-2 px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-rajdhani font-bold uppercase tracking-wider rounded-sm shadow-[0_0_15px_rgba(6,182,212,0.4)] hover:scale-105 transition-all disabled:opacity-50 disabled:hover:scale-100"
            data-testid="generate-insights-btn"
          >
            <Sparkles className="w-4 h-4" />
            {generatingInsights ? 'Analyzing...' : 'AI Insights'}
          </button>
        </div>
      </header>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-12 gap-4 h-[calc(100vh-5rem)] p-4 overflow-hidden">
        {/* Sidebar - Layer Controls */}
        <aside className="col-span-2 h-full flex flex-col gap-4" data-testid="layer-controls-sidebar">
          <div className="glass-card rounded-lg p-4">
            <h3 className="text-xs font-rajdhani font-bold uppercase tracking-widest text-slate-500 mb-3">Map Layers</h3>
            <div className="space-y-2">
              <LayerToggle
                icon={<Building2 />}
                label="Residential"
                active={activeLayers.residential}
                color="#06b6d4"
                onClick={() => toggleLayer('residential')}
              />
              <LayerToggle
                icon={<Building2 />}
                label="Commercial"
                active={activeLayers.commercial}
                color="#10b981"
                onClick={() => toggleLayer('commercial')}
              />
              <LayerToggle
                icon={<Activity />}
                label="Facilities"
                active={activeLayers.facilities}
                color="#f59e0b"
                onClick={() => toggleLayer('facilities')}
              />
              <LayerToggle
                icon={<Route />}
                label="Roads"
                active={activeLayers.roads}
                color="#8b5cf6"
                onClick={() => toggleLayer('roads')}
              />
            </div>
          </div>

          {indicators && (
            <div className="glass-card rounded-lg p-4 flex-1 overflow-y-auto">
              <h3 className="text-xs font-rajdhani font-bold uppercase tracking-widest text-slate-500 mb-3">Quick Stats</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-xs text-slate-500 font-rajdhani uppercase">Population</p>
                  <p className="text-lg font-mono text-cyan-400">{indicators.population_density.total_population.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-xs text-slate-500 font-rajdhani uppercase">Built-up Area</p>
                  <p className="text-lg font-mono text-emerald-400">{indicators.land_use.built_up_percentage}%</p>
                </div>
                <div>
                  <p className="text-xs text-slate-500 font-rajdhani uppercase">Accessibility</p>
                  <p className="text-lg font-mono text-amber-400">{indicators.service_accessibility.accessibility_score}/100</p>
                </div>
              </div>
            </div>
          )}
        </aside>

        {/* Main Map */}
        <main className="col-span-7 h-full relative rounded-xl overflow-hidden border border-slate-800" data-testid="main-map-container">
          {cityData && (
            <UrbanMap
              data={cityData.layers}
              activeLayers={activeLayers}
            />
          )}
        </main>

        {/* Right Panel - Analytics */}
        <aside className="col-span-3 h-full flex flex-col gap-4 overflow-y-auto pr-2" data-testid="analytics-panel">
          {indicators && (
            <>
              <MetricCard
                icon={<Activity />}
                title="Population Density"
                value={indicators.population_density.avg_density.toLocaleString()}
                unit="people/km²"
                trend="+2.3%"
                color="cyan"
              />
              
              <MetricCard
                icon={<Building2 />}
                title="Land Use Balance"
                value={indicators.land_use.built_up_percentage}
                unit="%"
                trend="+1.2%"
                color="emerald"
              />
              
              <MetricCard
                icon={<Route />}
                title="Road Density"
                value={indicators.road_network.road_density_km_per_km2.toFixed(2)}
                unit="km/km²"
                trend="+0.5%"
                color="purple"
              />
              
              <MetricCard
                icon={<Trees />}
                title="Green Space"
                value={indicators.green_space.green_space_percentage}
                unit="%"
                trend="-0.3%"
                color="green"
              />

              <div className="glass-card rounded-lg p-4">
                <h3 className="text-sm font-rajdhani font-bold uppercase tracking-wider text-slate-300 mb-3">Indicator Trends</h3>
                <IndicatorCharts indicators={indicators} />
              </div>
            </>
          )}
        </aside>
      </div>

      {/* AI Insights Panel - Sliding from Right */}
      {showAIPanel && aiInsights && (
        <div className="fixed inset-0 z-50 flex items-center justify-end">
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setShowAIPanel(false)}
          />
          <div className="relative w-full max-w-2xl h-full bg-slate-950 border-l border-slate-800 shadow-2xl animate-fadeIn overflow-y-auto">
            <div className="sticky top-0 bg-slate-950/95 backdrop-blur-xl border-b border-slate-800 p-6 flex items-center justify-between z-10">
              <div className="flex items-center gap-3">
                <Sparkles className="w-6 h-6 text-cyan-500" />
                <h2 className="text-xl font-rajdhani font-bold uppercase tracking-tight">AI Planning Insights</h2>
              </div>
              <button
                onClick={() => setShowAIPanel(false)}
                className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
                data-testid="close-insights-btn"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <AIInsightsPanel insights={aiInsights} />
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;