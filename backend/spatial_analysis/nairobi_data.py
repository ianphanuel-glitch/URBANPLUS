import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString, MultiPolygon
import numpy as np
import geojson

def generate_nairobi_sample_data():
    """
    Generate sample urban data for Nairobi, Kenya.
    Returns GeoDataFrames for different urban layers.
    """
    
    # Nairobi center coordinates
    nairobi_center = (-1.2864, 36.8172)
    
    # Generate residential zones
    residential_zones = [
        {'name': 'Westlands', 'center': (-1.2675, 36.8078), 'density': 8500, 'area_km2': 12.5},
        {'name': 'Kibera', 'center': (-1.3133, 36.7894), 'density': 45000, 'area_km2': 2.5},
        {'name': 'Eastleigh', 'center': (-1.2752, 36.8421), 'density': 35000, 'area_km2': 3.2},
        {'name': 'Karen', 'center': (-1.3167, 36.7014), 'density': 2500, 'area_km2': 15.8},
        {'name': 'Parklands', 'center': (-1.2583, 36.8264), 'density': 12000, 'area_km2': 8.3},
        {'name': 'Embakasi', 'center': (-1.3197, 36.8933), 'density': 28000, 'area_km2': 5.7},
        {'name': 'Lavington', 'center': (-1.2808, 36.7686), 'density': 5500, 'area_km2': 6.2},
        {'name': 'Kasarani', 'center': (-1.2231, 36.8989), 'density': 15000, 'area_km2': 9.1},
    ]
    
    residential_features = []
    for zone in residential_zones:
        # Create polygon around center
        size = np.sqrt(zone['area_km2']) / 111  # rough degree conversion
        polygon = Polygon([
            (zone['center'][1] - size/2, zone['center'][0] - size/2),
            (zone['center'][1] + size/2, zone['center'][0] - size/2),
            (zone['center'][1] + size/2, zone['center'][0] + size/2),
            (zone['center'][1] - size/2, zone['center'][0] + size/2),
        ])
        residential_features.append({
            'geometry': polygon,
            'name': zone['name'],
            'type': 'residential',
            'density': zone['density'],
            'area_km2': zone['area_km2'],
            'population': int(zone['density'] * zone['area_km2'])
        })
    
    # Commercial zones
    commercial_zones = [
        {'name': 'CBD', 'center': (-1.2864, 36.8172), 'area_km2': 4.2, 'businesses': 8500},
        {'name': 'Westlands Business District', 'center': (-1.2650, 36.8050), 'area_km2': 3.5, 'businesses': 4200},
        {'name': 'Industrial Area', 'center': (-1.3197, 36.8347), 'area_km2': 6.8, 'businesses': 1200},
        {'name': 'Kilimani', 'center': (-1.2892, 36.7850), 'area_km2': 2.8, 'businesses': 3100},
    ]
    
    commercial_features = []
    for zone in commercial_zones:
        size = np.sqrt(zone['area_km2']) / 111
        polygon = Polygon([
            (zone['center'][1] - size/2, zone['center'][0] - size/2),
            (zone['center'][1] + size/2, zone['center'][0] - size/2),
            (zone['center'][1] + size/2, zone['center'][0] + size/2),
            (zone['center'][1] - size/2, zone['center'][0] + size/2),
        ])
        commercial_features.append({
            'geometry': polygon,
            'name': zone['name'],
            'type': 'commercial',
            'area_km2': zone['area_km2'],
            'businesses': zone['businesses']
        })
    
    # Public facilities (schools, hospitals)
    facilities = [
        {'name': 'Kenyatta National Hospital', 'type': 'hospital', 'coords': (-1.3008, 36.8072), 'capacity': 2000},
        {'name': 'Nairobi Hospital', 'type': 'hospital', 'coords': (-1.2889, 36.8086), 'capacity': 500},
        {'name': 'Aga Khan University Hospital', 'type': 'hospital', 'coords': (-1.2536, 36.8114), 'capacity': 350},
        {'name': 'University of Nairobi', 'type': 'school', 'coords': (-1.2794, 36.8158), 'capacity': 35000},
        {'name': 'Strathmore University', 'type': 'school', 'coords': (-1.3100, 36.8117), 'capacity': 5000},
        {'name': 'Alliance High School', 'type': 'school', 'coords': (-1.2456, 36.8989), 'capacity': 1200},
        {'name': 'Karura Forest Health Center', 'type': 'hospital', 'coords': (-1.2436, 36.8372), 'capacity': 150},
    ]
    
    facility_features = []
    for facility in facilities:
        facility_features.append({
            'geometry': Point(facility['coords'][1], facility['coords'][0]),
            'name': facility['name'],
            'type': facility['type'],
            'capacity': facility['capacity']
        })
    
    # Road network (simplified major roads)
    roads = [
        {'name': 'Uhuru Highway', 'coords': [(-1.2864, 36.8172), (-1.3200, 36.8400)]},
        {'name': 'Mombasa Road', 'coords': [(-1.2864, 36.8172), (-1.3400, 36.8800)]},
        {'name': 'Thika Road', 'coords': [(-1.2864, 36.8172), (-1.2200, 36.9000)]},
        {'name': 'Waiyaki Way', 'coords': [(-1.2864, 36.8172), (-1.2600, 36.7400)]},
        {'name': 'Ngong Road', 'coords': [(-1.2864, 36.8172), (-1.3200, 36.7600)]},
    ]
    
    road_features = []
    for road in roads:
        line_coords = [(c[1], c[0]) for c in road['coords']]
        road_features.append({
            'geometry': LineString(line_coords),
            'name': road['name'],
            'type': 'major_road'
        })
    
    # Convert to GeoDataFrames
    residential_gdf = gpd.GeoDataFrame(residential_features, crs="EPSG:4326")
    commercial_gdf = gpd.GeoDataFrame(commercial_features, crs="EPSG:4326")
    facilities_gdf = gpd.GeoDataFrame(facility_features, crs="EPSG:4326")
    roads_gdf = gpd.GeoDataFrame(road_features, crs="EPSG:4326")
    
    return {
        'residential': residential_gdf,
        'commercial': commercial_gdf,
        'facilities': facilities_gdf,
        'roads': roads_gdf
    }

def convert_to_geojson(gdf):
    """Convert GeoDataFrame to GeoJSON dict"""
    return geojson.loads(gdf.to_json())