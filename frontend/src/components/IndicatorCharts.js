import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const IndicatorCharts = ({ indicators }) => {
  // Prepare density data
  const densityData = indicators.population_density.zones.slice(0, 5).map(zone => ({
    name: zone.name,
    density: zone.density
  }));

  // Prepare land use data
  const landUseData = [
    { name: 'Residential', value: indicators.land_use.residential_area_km2, color: '#06b6d4' },
    { name: 'Commercial', value: indicators.land_use.commercial_area_km2, color: '#10b981' },
    { name: 'Open Land', value: indicators.land_use.open_land_km2, color: '#64748b' }
  ];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-card rounded-lg p-3">
          <p className="text-xs text-slate-400 mb-1">{label || payload[0].name}</p>
          <p className="text-sm font-mono text-cyan-400">
            {typeof payload[0].value === 'number' ? payload[0].value.toLocaleString() : payload[0].value}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* Population Density Bar Chart */}
      <div>
        <h4 className="text-xs font-rajdhani uppercase tracking-wider text-slate-500 mb-3">Top 5 Dense Zones</h4>
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={densityData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#94a3b8', fontSize: 10 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="density" fill="#06b6d4" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Land Use Pie Chart */}
      <div>
        <h4 className="text-xs font-rajdhani uppercase tracking-wider text-slate-500 mb-3">Land Use Distribution</h4>
        <ResponsiveContainer width="100%" height={150}>
          <PieChart>
            <Pie
              data={landUseData}
              cx="50%"
              cy="50%"
              innerRadius={30}
              outerRadius={60}
              paddingAngle={2}
              dataKey="value"
            >
              {landUseData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
        <div className="flex justify-center gap-4 mt-2">
          {landUseData.map((item, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
              <span className="text-xs text-slate-500">{item.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default IndicatorCharts;