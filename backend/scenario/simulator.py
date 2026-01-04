from typing import Dict, List, Tuple
import numpy as np
from copy import deepcopy

class ScenarioSimulator:
    """
    Simulates urban planning scenarios and calculates impact metrics
    """
    
    def __init__(self, baseline_indicators: Dict):
        self.baseline = baseline_indicators
    
    def simulate_scenario(self, scenario_config: Dict) -> Dict:
        """
        Simulate a planning scenario and return projected indicators
        
        Args:
            scenario_config: {
                'name': str,
                'description': str,
                'interventions': [
                    {'type': 'hospital', 'location': 'Kibera', 'capacity': 150, 'cost': 3000000},
                    {'type': 'brt', 'route': 'CBD-Eastleigh', 'length_km': 15, 'cost': 50000000},
                    etc.
                ]
            }
        """
        simulated = deepcopy(self.baseline)
        interventions = scenario_config.get('interventions', [])
        
        total_cost = 0
        total_beneficiaries = 0
        accessibility_gain = 0
        implementation_time_months = 0
        equity_impact_score = 0
        
        for intervention in interventions:
            cost, beneficiaries, access_gain, time, equity = self._simulate_intervention(intervention)
            total_cost += cost
            total_beneficiaries += beneficiaries
            accessibility_gain += access_gain
            implementation_time_months = max(implementation_time_months, time)  # Parallel execution
            equity_impact_score += equity
        
        # Calculate derived metrics
        cost_per_beneficiary = total_cost / total_beneficiaries if total_beneficiaries > 0 else float('inf')
        
        # Update simulated indicators
        if 'service_accessibility' in simulated:
            simulated['service_accessibility']['accessibility_score'] = min(
                simulated['service_accessibility']['accessibility_score'] + accessibility_gain,
                100
            )
        
        return {
            'name': scenario_config['name'],
            'description': scenario_config['description'],
            'interventions': interventions,
            'metrics': {
                'total_cost_usd': total_cost,
                'people_benefited': total_beneficiaries,
                'accessibility_gain': accessibility_gain,
                'cost_per_beneficiary': cost_per_beneficiary,
                'equity_impact_score': equity_impact_score,
                'implementation_time_months': implementation_time_months,
                'confidence_level': self._calculate_confidence(interventions)
            },
            'projected_indicators': simulated
        }
    
    def _simulate_intervention(self, intervention: Dict) -> Tuple[float, int, float, int, float]:
        """
        Simulate single intervention and return (cost, beneficiaries, access_gain, time_months, equity_score)
        """
        int_type = intervention.get('type', '').lower()
        
        if int_type == 'hospital':
            capacity = intervention.get('capacity', 150)
            location = intervention.get('location', '')
            cost = intervention.get('cost', 3000000)
            
            # Estimate beneficiaries: 5km service radius, avg 10,000 ppl/km2
            beneficiaries = int(np.pi * (5**2) * 10000)  # ~785,000 people
            
            # Accessibility gain depends on current deficit
            current_score = self.baseline.get('service_accessibility', {}).get('accessibility_score', 0)
            access_gain = min(15.0, (100 - current_score) * 0.2)  # Up to 15 points
            
            # Implementation time
            time_months = 24  # 2 years for Level 4 hospital
            
            # Equity impact: higher in underserved areas
            equity = 8.0 if current_score < 5 else 5.0
            
            return (cost, beneficiaries, access_gain, time_months, equity)
        
        elif int_type == 'brt':
            length_km = intervention.get('length_km', 15)
            cost = intervention.get('cost', 50000000)
            
            # Beneficiaries: corridor population + commuters
            beneficiaries = 150000  # Daily commuters
            
            # Accessibility gain (mobility improvement)
            access_gain = 8.0
            
            # Implementation time
            time_months = 36  # 3 years for BRT
            
            # Equity: moderate (serves multiple zones)
            equity = 6.0
            
            return (cost, beneficiaries, access_gain, time_months, equity)
        
        elif int_type == 'park':
            area_hectares = intervention.get('area_hectares', 8)
            cost = intervention.get('cost', 3000000)
            
            # Beneficiaries: 2km radius
            beneficiaries = int(np.pi * (2**2) * 12000)  # ~150,000
            
            # Accessibility gain (quality of life)
            access_gain = 3.0
            
            # Implementation time
            time_months = 18  # 1.5 years
            
            # Equity: high in dense areas
            equity = 7.0
            
            return (cost, beneficiaries, access_gain, time_months, equity)
        
        elif int_type == 'school':
            capacity = intervention.get('capacity', 1000)
            cost = intervention.get('cost', 5000000)
            
            # Beneficiaries: students + families
            beneficiaries = capacity * 4  # Students + family members
            
            # Accessibility gain
            access_gain = 10.0
            
            # Implementation time
            time_months = 30
            
            # Equity
            equity = 9.0  # Education critical for equity
            
            return (cost, beneficiaries, access_gain, time_months, equity)
        
        elif int_type == 'road':
            length_km = intervention.get('length_km', 5)
            cost = intervention.get('cost', 10000000)
            
            # Beneficiaries
            beneficiaries = 80000
            
            # Accessibility gain
            access_gain = 5.0
            
            # Implementation time
            time_months = 24
            
            # Equity
            equity = 4.0
            
            return (cost, beneficiaries, access_gain, time_months, equity)
        
        else:
            # Unknown intervention type - conservative estimates
            return (intervention.get('cost', 1000000), 10000, 2.0, 12, 3.0)
    
    def _calculate_confidence(self, interventions: List[Dict]) -> str:
        """
        Calculate confidence level based on intervention types and data quality
        """
        if len(interventions) == 0:
            return 'LOW'
        
        # Known intervention types have higher confidence
        known_types = {'hospital', 'brt', 'park', 'school', 'road'}
        known_count = sum(1 for i in interventions if i.get('type', '').lower() in known_types)
        
        confidence_ratio = known_count / len(interventions)
        
        if confidence_ratio >= 0.8:
            return 'HIGH'
        elif confidence_ratio >= 0.5:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def compare_scenarios(self, scenarios: List[Dict]) -> Dict:
        """
        Compare multiple scenarios and identify best options
        """
        if not scenarios:
            return {'error': 'No scenarios provided'}
        
        simulated_scenarios = [self.simulate_scenario(s) for s in scenarios]
        
        # Extract metrics for comparison
        metrics = [s['metrics'] for s in simulated_scenarios]
        
        # Find best in each category
        best_roi_idx = min(range(len(metrics)), 
                          key=lambda i: metrics[i]['cost_per_beneficiary'])
        
        best_equity_idx = max(range(len(metrics)), 
                             key=lambda i: metrics[i]['equity_impact_score'])
        
        fastest_idx = min(range(len(metrics)), 
                         key=lambda i: metrics[i]['implementation_time_months'])
        
        # Calculate total beneficiaries and costs
        total_beneficiaries = sum(m['people_benefited'] for m in metrics)
        total_cost = sum(m['total_cost_usd'] for m in metrics)
        
        return {
            'scenarios': simulated_scenarios,
            'comparison': {
                'best_roi': {
                    'scenario_name': simulated_scenarios[best_roi_idx]['name'],
                    'cost_per_beneficiary': metrics[best_roi_idx]['cost_per_beneficiary']
                },
                'best_equity': {
                    'scenario_name': simulated_scenarios[best_equity_idx]['name'],
                    'equity_score': metrics[best_equity_idx]['equity_impact_score']
                },
                'fastest': {
                    'scenario_name': simulated_scenarios[fastest_idx]['name'],
                    'months': metrics[fastest_idx]['implementation_time_months']
                }
            },
            'summary': {
                'total_scenarios': len(scenarios),
                'total_beneficiaries': total_beneficiaries,
                'total_cost_usd': total_cost,
                'avg_confidence': self._avg_confidence(metrics)
            }
        }
    
    def _avg_confidence(self, metrics: List[Dict]) -> str:
        """
        Calculate average confidence across scenarios
        """
        confidence_map = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        scores = [confidence_map.get(m['confidence_level'], 1) for m in metrics]
        avg_score = sum(scores) / len(scores) if scores else 1
        
        if avg_score >= 2.5:
            return 'HIGH'
        elif avg_score >= 1.5:
            return 'MEDIUM'
        else:
            return 'LOW'
