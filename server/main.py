#!/usr/bin/env python3
"""
BGS Geology 50K MCP Server using FastMCP 2.0
Provides access to British Geological Survey 1:50,000 scale geological maps via WMS service
"""

import httpx
from urllib.parse import urlencode
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("BGS Geology 50K")

# BGS Geology WMS Configuration
BGS_GEOLOGY_WMS_URL = "https://map.bgs.ac.uk/arcgis/services/BGS_Detailed_Geology/MapServer/WMSServer"

# Geological layer mappings from BGS service
GEOLOGY_LAYERS = {
    "bedrock": "BGS.50k.Bedrock",
    "superficial_deposits": "BGS.50k.Superficial.deposits", 
    "artificial_ground": "BGS.50k.Artificial.ground",
    "mass_movement": "BGS.50k.Mass.movement",
    "linear_features": "BGS.50k.Linear.features"
}

async def get_geology_data(layer: str, lat: float, lon: float, format_type: str = "text/html") -> str:
    """Get geological data from BGS WMS service"""
    # WMS 1.3.0 with CRS:84 (lon,lat order) - bbox format: lon,lat,lon,lat
    buffer = 0.002  # ~200m buffer for geological features
    bbox = f"{lon-buffer},{lat-buffer},{lon+buffer},{lat+buffer}"
    
    params = {
        "service": "WMS",
        "request": "GetFeatureInfo",
        "version": "1.3.0",
        "layers": layer,
        "query_layers": layer,
        "styles": "default",
        "bbox": bbox,
        "crs": "CRS:84",
        "width": 450,
        "height": 450,
        "i": 225,  # center point
        "j": 225,
        "info_format": format_type,
        "radius": 0
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(BGS_GEOLOGY_WMS_URL, params=params)
        response.raise_for_status()
        return response.text

@mcp.tool
def get_available_geology_layers() -> dict:
    """Get available geological data layers from the BGS WMS service"""
    descriptions = {
        "bedrock": "Bedrock geology - solid rocks beneath superficial deposits",
        "superficial_deposits": "Superficial deposits - unconsolidated sediments above bedrock", 
        "artificial_ground": "Artificial ground - made ground, worked ground, infilled ground",
        "mass_movement": "Mass movement deposits - landslides, rockfall, debris flows",
        "linear_features": "Linear geological features - faults, dykes, mineral veins"
    }
    
    return {
        key: {
            "layer_name": layer_name,
            "description": descriptions[key]
        }
        for key, layer_name in GEOLOGY_LAYERS.items()
    }

@mcp.tool
async def get_geology_at_location(
    latitude: float,
    longitude: float, 
    geology_type: str = "bedrock",
    format_type: str = "text/html"
) -> str:
    """
    Get geological information at a specific geographic location from BGS data.
    
    Args:
        latitude: Latitude in decimal degrees (WGS84)
        longitude: Longitude in decimal degrees (WGS84)
        geology_type: Geological data type - bedrock, superficial_deposits, artificial_ground, mass_movement, linear_features
        format_type: Response format - text/html, text/xml, or text/plain
        
    Returns:
        Geological information for the specified location
    """
    # Validate inputs
    if not (49.0 <= latitude <= 61.0 and -8.0 <= longitude <= 2.0):
        return f"Coordinates outside UK bounds: {latitude}, {longitude}"
    
    if geology_type not in GEOLOGY_LAYERS:
        available = ", ".join(GEOLOGY_LAYERS.keys())
        return f"Invalid geology type. Available: {available}"
    
    valid_formats = ["text/html", "text/xml", "text/plain"]
    if format_type not in valid_formats:
        return f"Invalid format_type. Use: {', '.join(valid_formats)}"
    
    try:
        layer_name = GEOLOGY_LAYERS[geology_type]
        result = await get_geology_data(layer_name, latitude, longitude, format_type)
        
        if result.strip():
            return f"Geological data at {latitude:.4f}, {longitude:.4f}:\n\n{result}"
        else:
            return f"No geological data available at {latitude:.4f}, {longitude:.4f}"
            
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool
async def get_capabilities() -> str:
    """Get WMS capabilities document showing all available geological layers and metadata"""
    params = {
        "service": "WMS",
        "request": "GetCapabilities",
        "version": "1.3.0"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BGS_GEOLOGY_WMS_URL, params=params)
            response.raise_for_status()
            return response.text
    except Exception as e:
        return f"Error getting capabilities: {str(e)}"

@mcp.tool
def get_geology_map_url(
    layer: str,
    min_lat: float,
    min_lon: float,
    max_lat: float, 
    max_lon: float,
    width: int = 450,
    height: int = 450,
    format_type: str = "image/png"
) -> str:
    """Generate WMS GetMap URL for geological visualization
    
    Args:
        layer: Layer name (use get_available_geology_layers() to see options)
        min_lat: Minimum latitude (south boundary)
        min_lon: Minimum longitude (west boundary)
        max_lat: Maximum latitude (north boundary)  
        max_lon: Maximum longitude (east boundary)
        width: Image width in pixels
        height: Image height in pixels
        format_type: Image format (image/png, image/gif, image/jpeg)
        
    Note:
        Use small areas (0.05-0.15 degree boxes) for visible maps.
        Data is only visible between 1:100,000 and 1:25,000 scale.
        
    Returns:
        WMS GetMap URL for the specified geological layer and area
    """
    # Validate bbox values
    if min_lat >= max_lat:
        return "Error: min_lat must be less than max_lat"
    if min_lon >= max_lon:
        return "Error: min_lon must be less than max_lon"
    
    # WMS 1.3.0 with CRS:84 bbox format: min_lon,min_lat,max_lon,max_lat
    bbox = f"{min_lon},{min_lat},{max_lon},{max_lat}"
    
    params = {
        "service": "WMS",
        "request": "GetMap",
        "version": "1.3.0",
        "layers": layer,
        "styles": "default",
        "bbox": bbox,
        "crs": "CRS:84",
        "width": width,
        "height": height,
        "format": format_type
    }
    
    return f"{BGS_GEOLOGY_WMS_URL}?{urlencode(params)}"

@mcp.tool
def get_service_info() -> str:
    """Get information about the BGS Geology 50K WMS service"""
    return """BGS Geology 50K MCP Server

Provides access to British Geological Survey 1:50,000 scale geological maps via WMS.

Coverage: Great Britain (England, Wales, Scotland)
Scale: 1:50,000 (visible between 1:100,000 and 1:25,000 scale)
Coordinate systems: WGS84 (CRS:84) and British National Grid
Data source: BGS/UKRI under Open Government Licence

Geological Layers:
- bedrock: Solid rocks beneath superficial deposits
- superficial_deposits: Unconsolidated sediments above bedrock
- artificial_ground: Made ground, worked ground, infilled ground  
- mass_movement: Landslides, rockfall, debris flows
- linear_features: Faults, dykes, mineral veins

Tools:
- get_geology_at_location(lat, lon, geology_type, format) - Get geological data at point
- get_available_geology_layers() - List available geological data types
- get_capabilities() - Get full WMS capabilities document
- get_geology_map_url(layer, min_lat, min_lon, max_lat, max_lon, width, height, format) - Generate map visualization URL

Example: get_geology_at_location(51.5074, -0.1278, "bedrock", "text/html")
Map example: get_geology_map_url("BGS.50k.Bedrock", 51.0, -1.0, 51.1, -0.9)

Note: For visible maps, use smaller areas (0.05-0.15 degree boxes) as data is only visible at 1:25,000 to 1:100,000 scale.
Try bedrock or superficial_deposits layers first as they have better coverage than mass_movement.

Working examples:
- London bedrock: get_geology_map_url("BGS.50k.Bedrock", 51.45, -0.15, 51.55, -0.05)
- BGS test area: get_geology_map_url("BGS.50k.Superficial.deposits", 50.991, -2.215, 51.051, -2.155)"""

if __name__ == "__main__":
    # Run in HTTP mode for web access via Cloudflare Tunnel
    mcp.run(
        transport="http",
        host="127.0.0.1", 
        port=8083,
        path="/mcp"
    )
