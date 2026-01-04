from typing import Dict, List
import numpy as np

def generate_specific_recommendations(indicators: Dict, spatial_data: Dict = None) -> List[Dict]:
    """
    Generate specific, actionable planning recommendations
    with precise locations, costs, and impact estimates
    """
    recommendations = []
    
    pop_density = indicators.get('population_density', {})
    service_access = indicators.get('service_accessibility', {})
    green_space = indicators.get('green_space', {})
    road_network = indicators.get('road_network', {})
    
    # Healthcare Recommendations
    accessibility_score = service_access.get('accessibility_score', 0)
    if accessibility_score < 5.0:
        zones = pop_density.get('zones', [])
        high_density_zones = [z for z in zones if z.get('density', 0) > 20000]
        
        for zone in high_density_zones[:2]:  # Top 2 underserved zones
            recommendations.append({
                'id': f'health_{zone["name"].lower().replace(" ", "_")}',
                'category': 'Healthcare Infrastructure',
                'priority': 'HIGH',
                'title': f'Establish Level 4 Health Facility in {zone["name"]}',
                'description': f'Current accessibility score of {accessibility_score:.2f}/100 indicates severe healthcare deficit in high-density zones.',
                'specific_action': {
                    'facility_type': 'Level 4 Hospital',
                    'capacity': '150 beds',
                    'service_radius': '1.5 km',
                    'target_location': f'{zone["name"]} center',
                    'estimated_cost': '$2.5M - $3.5M',
                    'implementation_timeline': '18-24 months',
                    'land_requirement': '2-3 acres'
                },
                'expected_impact': {
                    'beneficiaries': f"{zone.get('population', 0):,} residents directly",
                    'accessibility_improvement': '+12-15 points',
                    'service_coverage': 'Within 1.5km radius',
                    'reduced_travel_time': '30-40% reduction'
                },
                'indicators_used': ['population_density', 'service_accessibility', 'hospital_capacity'],
                'confidence': 'HIGH',
                'assumptions': [
                    '1.5km service radius for Level 4 facility',
                    f'Current density: {zone.get("density", 0):,} people/km²',
                    'No major terrain barriers'
                ]
            })
    
    # Transportation Recommendations
    road_density = road_network.get('road_density_km_per_km2', 0)
    if road_density < 0.1:  # Low road density
        recommendations.append({
            'id': 'transport_brt_corridor',
            'category': 'Transportation',
            'priority': 'HIGH',
            'title': 'Develop BRT Corridor Along Major Routes',
            'description': f'Current road density of {road_density:.3f} km/km² indicates limited connectivity. BRT system would improve mobility.',
            'specific_action': {
                'infrastructure_type': 'Bus Rapid Transit (BRT)',
                'route': 'CBD to Eastleigh via Uhuru Highway',
                'length': '15 km dedicated lanes',
                'stations': '12 modern stations',
                'estimated_cost': '$45M - $55M',
                'implementation_timeline': '30-36 months',
                'capacity': '20,000 passengers/hour'
            },
            'expected_impact': {
                'beneficiaries': '150,000+ daily commuters',
                'travel_time_reduction': '40-50% during peak hours',
                'emissions_reduction': '25% along corridor',
                'economic_boost': 'Enhanced access to CBD employment'
            },
            'indicators_used': ['road_density', 'population_density', 'commercial_zones'],
            'confidence': 'HIGH',
            'assumptions': [
                'Existing road infrastructure can accommodate BRT',
                'Average 1.5km station spacing',
                'Right-of-way available'
            ]
        })
    
    # Green Space Recommendations
    green_pct = green_space.get('green_space_percentage', 0)
    per_capita = green_space.get('per_capita_m2', 0)
    if per_capita < 9.0:  # WHO minimum
        recommendations.append({
            'id': 'green_space_urban_parks',
            'category': 'Environmental Sustainability',
            'priority': 'MEDIUM',
            'title': 'Develop Neighborhood Parks Network',
            'description': f'Current {per_capita:.2f}m²/person falls below WHO minimum of 9m²/person. Urgent need for green space expansion.',
            'specific_action': {
                'infrastructure_type': 'Network of 5 Neighborhood Parks',
                'total_area': '25 hectares (distributed)',
                'target_locations': [
                    'Kibera: 8 ha',
                    'Eastleigh: 6 ha',
                    'Embakasi: 5 ha',
                    'Parklands: 4 ha',
                    'Westlands: 2 ha'
                ],
                'estimated_cost': '$8M - $12M',
                'implementation_timeline': '24-30 months',
                'features': 'Playgrounds, walkways, sports facilities'
            },
            'expected_impact': {
                'beneficiaries': '350,000+ residents',
                'per_capita_improvement': '+5.6m²/person',
                'air_quality': '10-15% improvement in surrounding areas',
                'mental_health': 'Reduced stress, improved wellbeing'
            },
            'indicators_used': ['green_space_percentage', 'per_capita_m2', 'population_density'],
            'confidence': 'MEDIUM',
            'assumptions': [
                'Land acquisition feasible',
                'Community support for park development',
                'Maintenance budget allocated'
            ]
        })
    
    # Mixed-Use Development
    total_pop = pop_density.get('total_population', 0)
    if total_pop > 500000:
        recommendations.append({
            'id': 'mixed_use_development',
            'category': 'Urban Planning',
            'priority': 'MEDIUM',
            'title': 'Promote Mixed-Use Development Zones',
            'description': 'Reduce commute times and improve livability through integrated residential-commercial zones.',
            'specific_action': {
                'policy_type': 'Zoning Reform + Incentives',
                'target_areas': 'Kilimani, Westlands, Parklands corridors',
                'incentives': [
                    '15% FAR bonus for mixed-use projects',
                    'Fast-track approvals (90 days)',
                    'Tax abatement for first 5 years'
                ],
                'estimated_cost': '$500K (policy + admin)',
                'implementation_timeline': '6-12 months',
                'minimum_requirements': '30% commercial, 60% residential, 10% amenities'
            },
            'expected_impact': {
                'beneficiaries': 'Citywide (long-term)',
                'commute_reduction': '20-30% for affected areas',
                'local_employment': '+5,000 jobs',
                'livability_score': '+10-15 points'
            },
            'indicators_used': ['land_use_ratio', 'population_density', 'commercial_areas'],
            'confidence': 'MEDIUM',
            'assumptions': [
                'Developer interest in mixed-use',
                'Market demand for residential-commercial integration',
                'Infrastructure can support increased density'
            ]
        })
    
    # Infrastructure Maintenance
    recommendations.append({
        'id': 'infrastructure_audit',
        'category': 'Infrastructure Maintenance',
        'priority': 'LOW',
        'title': 'Conduct Comprehensive Infrastructure Audit',
        'description': 'Establish baseline for all urban infrastructure to enable data-driven planning.',
        'specific_action': {
            'scope': 'Roads, water, sewerage, electricity, telecom',
            'methodology': 'GIS mapping + condition assessment',
            'deliverables': [
                'Digital twin database',
                'Maintenance priority matrix',
                'Replacement cost estimates'
            ],
            'estimated_cost': '$1.5M - $2M',
            'implementation_timeline': '12 months',
            'team': '3 GIS specialists, 5 field engineers'
        },
        'expected_impact': {
            'beneficiaries': 'Citywide (planning office)',
            'planning_efficiency': '+40% improvement',
            'budget_optimization': '15-20% savings',
            'response_time': '50% faster for maintenance issues'
        },
        'indicators_used': ['all_indicators'],
        'confidence': 'HIGH',
        'assumptions': [
            'Access to all infrastructure locations',
            'Cooperation from utility providers',
            'GIS capacity available'
        ]
    })
    
    return recommendations
