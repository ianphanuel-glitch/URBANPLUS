import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const UrbanMap = ({ data, activeLayers }) => {
  const mapRef = useRef(null);

  const getLayerStyle = (layerType) => {
    const styles = {
      residential: {
        fillColor: '#06b6d4',
        fillOpacity: 0.3,
        color: '#06b6d4',
        weight: 2
      },
      commercial: {
        fillColor: '#10b981',
        fillOpacity: 0.3,
        color: '#10b981',
        weight: 2
      },
      facilities: {
        radius: 8,
        fillColor: '#f59e0b',
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
      },
      roads: {
        color: '#8b5cf6',
        weight: 3,
        opacity: 0.7
      }
    };
    return styles[layerType] || {};
  };

  const onEachFeature = (feature, layer) => {
    if (feature.properties) {
      const props = feature.properties;
      let popupContent = `<div class="font-rajdhani">`;
      
      if (props.name) {
        popupContent += `<h3 class="font-bold text-cyan-400 mb-2">${props.name}</h3>`;
      }
      
      if (props.type) {
        popupContent += `<p><span class="text-slate-400">Type:</span> ${props.type}</p>`;
      }
      
      if (props.density) {
        popupContent += `<p><span class="text-slate-400">Density:</span> ${props.density.toLocaleString()} ppl/km²</p>`;
      }
      
      if (props.population) {
        popupContent += `<p><span class="text-slate-400">Population:</span> ${props.population.toLocaleString()}</p>`;
      }
      
      if (props.businesses) {
        popupContent += `<p><span class="text-slate-400">Businesses:</span> ${props.businesses.toLocaleString()}</p>`;
      }
      
      if (props.capacity) {
        popupContent += `<p><span class="text-slate-400">Capacity:</span> ${props.capacity.toLocaleString()}</p>`;
      }
      
      popupContent += '</div>';
      layer.bindPopup(popupContent);
    }
  };

  const pointToLayer = (feature, latlng) => {
    return L.circleMarker(latlng, getLayerStyle('facilities'));
  };

  return (
    <MapContainer
      center={[-1.2864, 36.8172]}
      zoom={11}
      style={{ width: '100%', height: '100%' }}
      zoomControl={true}
      ref={mapRef}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | <a href="https://carto.com/">CartoDB</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      
      {data && activeLayers.residential && data.residential && (
        <GeoJSON
          data={data.residential}
          style={getLayerStyle('residential')}
          onEachFeature={onEachFeature}
        />
      )}
      
      {data && activeLayers.commercial && data.commercial && (
        <GeoJSON
          data={data.commercial}
          style={getLayerStyle('commercial')}
          onEachFeature={onEachFeature}
        />
      )}
      
      {data && activeLayers.roads && data.roads && (
        <GeoJSON
          data={data.roads}
          style={getLayerStyle('roads')}
          onEachFeature={onEachFeature}
        />
      )}
      
      {data && activeLayers.facilities && data.facilities && (
        <GeoJSON
          data={data.facilities}
          pointToLayer={pointToLayer}
          onEachFeature={onEachFeature}
        />
      )}
    </MapContainer>
  );
};

export default UrbanMap;