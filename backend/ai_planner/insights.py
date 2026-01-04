from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import json
from typing import Dict, List

async def generate_planning_insights(indicators: Dict, model: str = "gpt-5.2") -> Dict:
    """
    Generate AI-powered urban planning insights using emergentintegrations
    """
    api_key = os.environ.get('EMERGENT_LLM_KEY')
    
    if not api_key:
        return {
            'error': 'EMERGENT_LLM_KEY not configured',
            'insights': [],
            'recommendations': []
        }
    
    # Prepare context for AI
    try:
        # Safely extract values with defaults
        pop_density = indicators.get('population_density', {})
        land_use = indicators.get('land_use', {})
        road_network = indicators.get('road_network', {})
        service_access = indicators.get('service_accessibility', {})
        green_space = indicators.get('green_space', {})
        
        # Get most dense zone safely
        zones = pop_density.get('zones', [])
        most_dense_zone = f"{zones[0]['name']} ({zones[0]['density']:,} people/km²)" if zones else 'N/A'
        
        # Get coverage data safely
        coverage = service_access.get('coverage', {})
        hospitals_per_100k = coverage.get('hospitals_per_100k', 0)
        
        context = f"""
You are an expert urban planner analyzing data for Nairobi, Kenya.

Current Urban Indicators:

1. Population Density:
   - Total Population: {pop_density.get('total_population', 0):,}
   - Average Density: {pop_density.get('avg_density', 0):.2f} people/km²
   - Most Dense Zone: {most_dense_zone}

2. Land Use:
   - Built-up Area: {land_use.get('built_up_percentage', 0):.2f}%
   - Residential: {land_use.get('residential_area_km2', 0):.2f} km²
   - Commercial: {land_use.get('commercial_area_km2', 0):.2f} km²

3. Road Network:
   - Road Density: {road_network.get('road_density_km_per_km2', 0):.3f} km/km²
   - Total Roads: {road_network.get('total_length_km', 0):.2f} km

4. Service Accessibility:
   - Accessibility Score: {service_access.get('accessibility_score', 0):.2f}/100
   - Hospitals: {service_access.get('total_hospitals', 0)}
   - Schools: {service_access.get('total_schools', 0)}
   - Hospitals per 100k: {hospitals_per_100k:.2f}

5. Green Space:
   - Green Space Coverage: {green_space.get('green_space_percentage', 0):.2f}%
   - Per Capita: {green_space.get('per_capita_m2', 0):.2f} m²/person

Based on this data, provide:
1. 3-5 critical planning issues or concerns
2. 3-5 specific, actionable recommendations for urban planners

Respond ONLY with valid JSON in this exact format:
{{
  "issues": [
    {{
      "title": "Issue title",
      "severity": "high|medium|low",
      "description": "Detailed description",
      "affected_metric": "population_density|service_accessibility|etc"
    }}
  ],
  "recommendations": [
    {{
      "title": "Recommendation title",
      "priority": "high|medium|low",
      "description": "Specific action to take",
      "target_area": "Specific zone or citywide",
      "estimated_impact": "Expected outcome"
    }}
  ]
}}
"""
    except Exception as e:
        return {
            'error': f'Error preparing context: {str(e)}',
            'issues': [],
            'recommendations': []
        }
    
    try:
        # Initialize chat
        chat = LlmChat(
            api_key=api_key,
            session_id="urban_planning_nairobi",
            system_message="You are an expert urban planner with deep knowledge of African cities, rapid urbanization, and infrastructure planning. You provide data-driven, actionable insights."
        )
        
        # Select model/provider
        if "gpt" in model.lower():
            chat.with_model("openai", model)
        elif "claude" in model.lower():
            chat.with_model("anthropic", model)
        elif "gemini" in model.lower():
            chat.with_model("gemini", model)
        
        # Send message
        user_message = UserMessage(text=context)
        response = await chat.send_message(user_message)
        
        # Parse response
        try:
            insights_data = json.loads(response)
            return {
                'issues': insights_data.get('issues', []),
                'recommendations': insights_data.get('recommendations', []),
                'model_used': model
            }
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                insights_data = json.loads(json_str)
                return {
                    'issues': insights_data.get('issues', []),
                    'recommendations': insights_data.get('recommendations', []),
                    'model_used': model
                }
            else:
                return {
                    'error': 'Failed to parse AI response',
                    'raw_response': response[:500],
                    'issues': [],
                    'recommendations': []
                }
    
    except Exception as e:
        return {
            'error': str(e),
            'issues': [],
            'recommendations': []
        }