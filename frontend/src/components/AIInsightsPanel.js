import React from 'react';
import { AlertTriangle, TrendingUp, CheckCircle2, XCircle, AlertCircle, MapPin, DollarSign, Calendar, Users, Info } from 'lucide-react';

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
    switch (priority?.toUpperCase()) {
      case 'HIGH':
        return 'border-red-500/30 bg-red-500/5';
      case 'MEDIUM':
        return 'border-amber-500/30 bg-amber-500/5';
      case 'LOW':
        return 'border-emerald-500/30 bg-emerald-500/5';
      default:
        return 'border-slate-500/30 bg-slate-500/5';
    }
  };

  const getPriorityBadgeColor = (priority) => {
    switch (priority?.toUpperCase()) {
      case 'HIGH':
        return 'bg-red-500/20 text-red-400';
      case 'MEDIUM':
        return 'bg-amber-500/20 text-amber-400';
      case 'LOW':
        return 'bg-emerald-500/20 text-emerald-400';
      default:
        return 'bg-slate-500/20 text-slate-400';
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
      {/* Model and Explainability Info */}
      <div className="glass-card rounded-lg p-4 border-cyan-500/30" data-testid="explainability-section">
        <div className="flex items-start gap-3">
          <Info className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-1" />
          <div className="flex-1">
            <h4 className="text-sm font-rajdhani font-bold text-cyan-400 mb-2">Analysis Transparency</h4>
            {insights.model_used && (
              <p className="text-xs text-slate-400 mb-2" data-testid="ai-model-info">
                <span className="text-slate-500">Model:</span> <span className="text-cyan-400 font-mono">{insights.model_used}</span>
              </p>
            )}
            {insights.explainability && (
              <div className="space-y-2 text-xs">
                <div>
                  <span className="text-slate-500">Indicators Analyzed:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {insights.explainability.indicators_analyzed?.map((indicator, idx) => (
                      <span key={idx} className="px-2 py-1 bg-slate-800 text-slate-300 rounded-sm font-mono text-xs">
                        {indicator}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <span className="text-slate-500">Key Assumptions:</span>
                  <ul className="text-slate-400 mt-1 space-y-1 ml-4">
                    {insights.explainability.assumptions?.map((assumption, idx) => (
                      <li key={idx} className="list-disc">{assumption}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

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

      {/* Planning Recommendations (Detailed) */}
      {insights.planning_recommendations && insights.planning_recommendations.length > 0 && (
        <section data-testid="planning-recommendations-section">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            <h3 className="text-lg font-rajdhani font-bold uppercase tracking-wide">Planning Recommendations</h3>
          </div>
          
          <div className="space-y-4">
            {insights.planning_recommendations.map((rec, idx) => (
              <div key={idx} className={`glass-card rounded-lg p-5 border ${getPriorityColor(rec.priority)}`} data-testid={`planning-rec-card-${idx}`}>
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <span className="text-xs font-rajdhani uppercase text-slate-500">{rec.category}</span>
                    <h4 className="font-rajdhani font-bold text-slate-200 text-lg mt-1">{rec.title}</h4>
                  </div>
                  <span className={`text-xs px-3 py-1 rounded-full font-rajdhani uppercase font-bold shrink-0 ml-2 ${getPriorityBadgeColor(rec.priority)}`}>
                    {rec.priority}
                  </span>
                </div>
                
                <p className="text-sm text-slate-400 mb-4">{rec.description}</p>
                
                {/* Specific Action */}
                {rec.specific_action && (
                  <div className="bg-slate-900/50 rounded-lg p-4 mb-4">
                    <h5 className="text-xs font-rajdhani font-bold uppercase text-cyan-400 mb-3">Specific Action Plan</h5>
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      {Object.entries(rec.specific_action).map(([key, value]) => (
                        <div key={key}>
                          <span className="text-slate-500 font-rajdhani uppercase block mb-1">{key.replace(/_/g, ' ')}</span>
                          {Array.isArray(value) ? (
                            <ul className="text-slate-300 space-y-1">
                              {value.map((item, i) => (
                                <li key={i} className="flex items-start gap-1">
                                  <span className="text-cyan-400 mt-1">•</span>
                                  <span>{item}</span>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="text-slate-300">{value}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Expected Impact */}
                {rec.expected_impact && (
                  <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-lg p-4 mb-4">
                    <h5 className="text-xs font-rajdhani font-bold uppercase text-emerald-400 mb-3 flex items-center gap-2">
                      <Users className="w-4 h-4" />
                      Expected Impact
                    </h5>
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      {Object.entries(rec.expected_impact).map(([key, value]) => (
                        <div key={key}>
                          <span className="text-slate-500 font-rajdhani uppercase block mb-1">{key.replace(/_/g, ' ')}</span>
                          <p className="text-emerald-300 font-medium">{value}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Explainability Footer */}
                <div className="flex items-start gap-2 pt-3 border-t border-slate-700">
                  <Info className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
                  <div className="text-xs text-slate-500">
                    <p className="mb-1">
                      <span className="font-rajdhani uppercase font-bold">Confidence:</span> {rec.confidence}
                    </p>
                    {rec.assumptions && rec.assumptions.length > 0 && (
                      <div>
                        <span className="font-rajdhani uppercase font-bold">Assumptions:</span>
                        <ul className="mt-1 space-y-0.5 ml-4">
                          {rec.assumptions.map((assumption, i) => (
                            <li key={i} className="list-disc">{assumption}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* AI Recommendations (Simple) */}
      {insights.ai_recommendations && insights.ai_recommendations.length > 0 && (
        <section data-testid="ai-recommendations-section">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
            <h3 className="text-lg font-rajdhani font-bold uppercase tracking-wide">Additional AI Suggestions</h3>
          </div>
          
          <div className="space-y-3">
            {insights.ai_recommendations.map((rec, idx) => (
              <div key={idx} className={`glass-card rounded-lg p-4 border ${getPriorityColor(rec.priority)}`} data-testid={`ai-rec-card-${idx}`}>
                <div className="flex items-start justify-between mb-3">
                  <h4 className="font-rajdhani font-bold text-slate-200">{rec.title}</h4>
                  <span className={`text-xs px-2 py-1 rounded-full font-rajdhani uppercase shrink-0 ml-2 ${getPriorityBadgeColor(rec.priority)}`}>
                    {rec.priority}
                  </span>
                </div>
                
                <p className="text-sm text-slate-400 mb-3">{rec.description}</p>
                
                {(rec.target_area || rec.estimated_impact) && (
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
                )}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default AIInsightsPanel;