import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const MetricCard = ({ icon, title, value, unit, trend, color = 'cyan' }) => {
  const colorClasses = {
    cyan: {
      border: 'border-cyan-500/30',
      text: 'text-cyan-400',
      glow: 'shadow-[0_0_20px_-5px_rgba(6,182,212,0.3)]'
    },
    emerald: {
      border: 'border-emerald-500/30',
      text: 'text-emerald-400',
      glow: 'shadow-[0_0_20px_-5px_rgba(16,185,129,0.3)]'
    },
    purple: {
      border: 'border-purple-500/30',
      text: 'text-purple-400',
      glow: 'shadow-[0_0_20px_-5px_rgba(139,92,246,0.3)]'
    },
    green: {
      border: 'border-green-500/30',
      text: 'text-green-400',
      glow: 'shadow-[0_0_20px_-5px_rgba(34,197,94,0.3)]'
    },
    amber: {
      border: 'border-amber-500/30',
      text: 'text-amber-400',
      glow: 'shadow-[0_0_20px_-5px_rgba(245,158,11,0.3)]'
    }
  };

  const colors = colorClasses[color] || colorClasses.cyan;
  const isTrendPositive = trend && trend.startsWith('+');

  return (
    <div className={`glass-card rounded-lg p-4 metric-card ${colors.glow} hover:${colors.glow} transition-all group`} data-testid={`metric-card-${title.toLowerCase().replace(/\s+/g, '-')}`}>
      <div className="flex items-start justify-between mb-3">
        <div className={`p-2 rounded-lg bg-slate-900/50 ${colors.text} group-hover:scale-110 transition-transform`}>
          {React.cloneElement(icon, { className: 'w-5 h-5' })}
        </div>
        {trend && (
          <div className={`flex items-center gap-1 text-xs font-mono ${isTrendPositive ? 'text-emerald-400' : 'text-red-400'}`}>
            {isTrendPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
            <span>{trend}</span>
          </div>
        )}
      </div>
      
      <h3 className="text-xs font-rajdhani uppercase tracking-wider text-slate-500 mb-2">{title}</h3>
      
      <div className="flex items-baseline gap-2">
        <span className={`text-3xl font-bold font-mono ${colors.text}`} data-testid={`metric-value-${title.toLowerCase().replace(/\s+/g, '-')}`}>{value}</span>
        <span className="text-sm text-slate-500 font-rajdhani">{unit}</span>
      </div>
    </div>
  );
};

export default MetricCard;