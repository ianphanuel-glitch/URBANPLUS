import React from 'react';
import { AlertTriangle, TrendingUp, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';

const AIInsightsPanel = ({ insights }) => {
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'high':
        return <XCircle className="w-5 h-5 text-red-400" />;
      case 'medium':
        return <AlertCircle className="w-5 h-5 text-amber-400" />;
      case 'low':
        return <AlertTriangle className="w-5 h-5 text-yellow-400" />;
      default:
        return <AlertCircle className="w-5 h-5 text-slate-400" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'border-red-500/30 bg-red-500/5';
      case 'medium':
        return 'border-amber-500/30 bg-amber-500/5';
      case 'low':
        return 'border-emerald-500/30 bg-emerald-500/5';
      default:
        return 'border-slate-500/30 bg-slate-500/5';
    }
  };

  if (insights.error) {
    return (
      <div className="p-6">
        <div className="glass-card rounded-lg p-6 border-red-500/30">
          <div className="flex items-start gap-3">
            <XCircle className="w-6 h-6 text-red-400 flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-rajdhani font-bold text-red-400 mb-2">Error Generating Insights</h3>
              <p className="text-sm text-slate-400">{insights.error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Model Info */}
      {insights.model_used && (
        <div className="text-xs text-slate-500 font-mono" data-testid="ai-model-info">
          Generated using {insights.model_used}
        </div>
      )}

      {/* Critical Issues */}
      <section data-testid="critical-issues-section">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-5 h-5 text-red-400" />
          <h3 className="text-lg font-rajdhani font-bold uppercase tracking-wide">Critical Issues</h3>
        </div>
        
        <div className="space-y-3">
          {insights.issues && insights.issues.length > 0 ? (
            insights.issues.map((issue, idx) => (
              <div key={idx} className="glass-card rounded-lg p-4 border-l-2" style={{ borderLeftColor: issue.severity === 'high' ? '#ef4444' : issue.severity === 'medium' ? '#f59e0b' : '#eab308' }} data-testid={`issue-card-${idx}`}>
                <div className="flex items-start gap-3">
                  {getSeverityIcon(issue.severity)}
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-rajdhani font-bold text-slate-200">{issue.title}</h4>
                      <span className={`text-xs px-2 py-1 rounded-full font-rajdhani uppercase ${issue.severity === 'high' ? 'bg-red-500/20 text-red-400' : issue.severity === 'medium' ? 'bg-amber-500/20 text-amber-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                        {issue.severity}
                      </span>
                    </div>
                    <p className="text-sm text-slate-400 mb-2">{issue.description}</p>
                    {issue.affected_metric && (
                      <span className="text-xs text-slate-500 font-mono">Affects: {issue.affected_metric}</span>
                    )}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="glass-card rounded-lg p-4 text-center text-slate-500">
              <CheckCircle2 className="w-8 h-8 mx-auto mb-2 text-emerald-400" />
              <p className="text-sm">No critical issues detected</p>
            </div>
          )}
        </div>
      </section>

      {/* Recommendations */}
      <section data-testid="recommendations-section">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-emerald-400" />
          <h3 className="text-lg font-rajdhani font-bold uppercase tracking-wide">Planning Recommendations</h3>
        </div>
        
        <div className="space-y-3">
          {insights.recommendations && insights.recommendations.length > 0 ? (
            insights.recommendations.map((rec, idx) => (
              <div key={idx} className={`glass-card rounded-lg p-4 border ${getPriorityColor(rec.priority)}`} data-testid={`recommendation-card-${idx}`}>
                <div className="flex items-start justify-between mb-3">
                  <h4 className="font-rajdhani font-bold text-slate-200">{rec.title}</h4>
                  <span className={`text-xs px-2 py-1 rounded-full font-rajdhani uppercase shrink-0 ml-2 ${
                    rec.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                    rec.priority === 'medium' ? 'bg-amber-500/20 text-amber-400' :
                    'bg-emerald-500/20 text-emerald-400'
                  }`}>
                    {rec.priority} priority
                  </span>
                </div>
                
                <p className="text-sm text-slate-400 mb-3">{rec.description}</p>
                
                <div className="grid grid-cols-2 gap-3 text-xs">
                  {rec.target_area && (
                    <div>
                      <span className="text-slate-500 font-rajdhani uppercase">Target:</span>
                      <p className="text-slate-300 mt-1">{rec.target_area}</p>
                    </div>
                  )}
                  {rec.estimated_impact && (
                    <div>
                      <span className="text-slate-500 font-rajdhani uppercase">Impact:</span>
                      <p className="text-slate-300 mt-1">{rec.estimated_impact}</p>
                    </div>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="glass-card rounded-lg p-4 text-center text-slate-500">
              <p className="text-sm">No recommendations available</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default AIInsightsPanel;