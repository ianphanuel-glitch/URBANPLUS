import numpy as np
import geopandas as gpd
from shapely.geometry import Point, box
from typing import Dict, List

def calculate_population_density(residential_gdf: gpd.GeoDataFrame) -> Dict:
    """
    Calculate population density metrics
    """
    if residential_gdf.empty:
        return {'total_population': 0, 'avg_density': 0, 'zones': []}
    
    total_pop = residential_gdf['population'].sum()
    total_area = residential_gdf['area_km2'].sum()
    avg_density = total_pop / total_area if total_area > 0 else 0
    
    # Get zone-level metrics
    zones = []
    for _, row in residential_gdf.iterrows():
        zones.append({
            'name': row['name'],
            'density': float(row['density']),
            'population': int(row['population']),
            'area_km2': float(row['area_km2'])
        })
    
    return {
        'total_population': int(total_pop),
        'avg_density': round(avg_density, 2),
        'total_area_km2': round(total_area, 2),
        'zones': sorted(zones, key=lambda x: x['density'], reverse=True)
    }

def calculate_land_use_ratio(residential_gdf: gpd.GeoDataFrame, 
                            commercial_gdf: gpd.GeoDataFrame) -> Dict:
    """
    Calculate built-up vs open land ratio
    """
    residential_area = residential_gdf['area_km2'].sum() if not residential_gdf.empty else 0
    commercial_area = commercial_gdf['area_km2'].sum() if not commercial_gdf.empty else 0
    
    # Nairobi metro approximate area
    total_metro_area = 696  # km²
    
    built_up = residential_area + commercial_area
    open_land = total_metro_area - built_up
    
    built_up_pct = (built_up / total_metro_area) * 100 if total_metro_area > 0 else 0
    
    return {
        'residential_area_km2': round(residential_area, 2),
        'commercial_area_km2': round(commercial_area, 2),
        'built_up_area_km2': round(built_up, 2),
        'open_land_km2': round(open_land, 2),
        'built_up_percentage': round(built_up_pct, 2),
        'total_metro_area_km2': total_metro_area
    }

def calculate_road_density(roads_gdf: gpd.GeoDataFrame) -> Dict:
    """
    Calculate road density and connectivity metrics
    """
    if roads_gdf.empty:
        return {'total_length_km': 0, 'road_density': 0, 'roads': []}
    
    # Calculate total road length
    # Convert to meters, then to km
    roads_projected = roads_gdf.to_crs("EPSG:32737")  # UTM Zone 37S for Nairobi
    total_length = roads_projected.geometry.length.sum() / 1000  # to km
    
    # Approximate Nairobi metro area
    metro_area = 696  # km²
    road_density = total_length / metro_area
    
    roads_list = []
    for _, row in roads_gdf.iterrows():
        roads_list.append({
            'name': row['name'],
            'type': row['type']
        })
    
    return {
        'total_length_km': round(total_length, 2),
        'road_density_km_per_km2': round(road_density, 3),
        'major_roads_count': len(roads_gdf),
        'roads': roads_list
    }

def calculate_service_accessibility(facilities_gdf: gpd.GeoDataFrame, 
                                   residential_gdf: gpd.GeoDataFrame) -> Dict:
    """
    Calculate service accessibility index
    Based on proximity of healthcare and education to residential areas
    """
    if facilities_gdf.empty or residential_gdf.empty:
        return {'accessibility_score': 0, 'coverage': {}}
    
    hospitals = facilities_gdf[facilities_gdf['type'] == 'hospital']
    schools = facilities_gdf[facilities_gdf['type'] == 'school']
    
    # Simple accessibility: count facilities within 5km of each residential zone
    service_radius = 5000  # 5km in meters
    
    # Project to metric CRS
    facilities_proj = facilities_gdf.to_crs("EPSG:32737")
    residential_proj = residential_gdf.to_crs("EPSG:32737")
    
    access_scores = []
    for _, res_zone in residential_proj.iterrows():
        centroid = res_zone.geometry.centroid
        
        # Count nearby facilities
        nearby_hospitals = sum(facilities_proj[facilities_proj['type'] == 'hospital'].geometry.distance(centroid) <= service_radius)
        nearby_schools = sum(facilities_proj[facilities_proj['type'] == 'school'].geometry.distance(centroid) <= service_radius)
        
        # Simple score: normalized by population
        pop = res_zone['population']
        hospital_ratio = (nearby_hospitals * 1000) / pop if pop > 0 else 0
        school_ratio = (nearby_schools * 1000) / pop if pop > 0 else 0
        
        zone_score = (hospital_ratio * 0.6 + school_ratio * 0.4) * 100
        access_scores.append(zone_score)
    
    avg_score = np.mean(access_scores) if access_scores else 0
    
    return {
        'accessibility_score': round(min(avg_score, 100), 2),
        'total_hospitals': len(hospitals),
        'total_schools': len(schools),
        'hospital_capacity': int(hospitals['capacity'].sum()) if not hospitals.empty else 0,
        'school_capacity': int(schools['capacity'].sum()) if not schools.empty else 0,
        'coverage': {
            'hospitals_per_100k': round((len(hospitals) * 100000) / residential_gdf['population'].sum(), 2) if not residential_gdf.empty else 0,
            'schools_per_100k': round((len(schools) * 100000) / residential_gdf['population'].sum(), 2) if not residential_gdf.empty else 0
        }
    }

def calculate_green_space_coverage() -> Dict:
    """
    Estimate green space coverage for Nairobi
    (Using approximate data for demo)
    """
    # Known green spaces in Nairobi
    green_spaces = [
        {'name': 'Karura Forest', 'area_km2': 10.2},
        {'name': 'Nairobi Arboretum', 'area_km2': 0.3},
        {'name': 'Uhuru Park', 'area_km2': 0.13},
        {'name': 'Central Park', 'area_km2': 0.04},
        {'name': 'City Park', 'area_km2': 0.6},
    ]
    
    total_green = sum(space['area_km2'] for space in green_spaces)
    metro_area = 696  # km²
    green_percentage = (total_green / metro_area) * 100
    
    return {
        'total_green_space_km2': round(total_green, 2),
        'green_space_percentage': round(green_percentage, 2),
        'spaces': green_spaces,
        'per_capita_m2': round((total_green * 1000000) / 4500000, 2)  # Approx Nairobi pop: 4.5M
    }

def calculate_all_indicators(data: Dict) -> Dict:
    """
    Calculate all urban indicators
    """
    return {
        'population_density': calculate_population_density(data['residential']),
        'land_use': calculate_land_use_ratio(data['residential'], data['commercial']),
        'road_network': calculate_road_density(data['roads']),
        'service_accessibility': calculate_service_accessibility(data['facilities'], data['residential']),
        'green_space': calculate_green_space_coverage()
    }