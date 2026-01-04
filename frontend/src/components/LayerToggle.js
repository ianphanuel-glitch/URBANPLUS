import React from 'react';

const LayerToggle = ({ icon, label, active, color, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`layer-toggle w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-all ${
        active ? 'active bg-slate-900/50' : 'bg-transparent hover:bg-slate-900/30'
      }`}
      style={{
        borderLeft: active ? `2px solid ${color}` : '2px solid transparent'
      }}
      data-testid={`layer-toggle-${label.toLowerCase()}`}
    >
      <div className="text-slate-400" style={{ color: active ? color : undefined }}>
        {React.cloneElement(icon, { className: 'w-4 h-4' })}
      </div>
      <span className={`text-sm font-rajdhani uppercase tracking-wide ${
        active ? 'text-slate-200' : 'text-slate-500'
      }`}>{label}</span>
    </button>
  );
};

export default LayerToggle;