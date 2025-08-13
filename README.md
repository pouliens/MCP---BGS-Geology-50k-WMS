# BGS Geology 50K MCP Server

A FastMCP 2.0 server providing access to British Geological Survey 1:50,000 scale geological maps via WMS.

## Overview

This MCP server enables AI assistants to query comprehensive UK geological data including bedrock, superficial deposits, artificial ground, mass movement, and linear geological features. Data is sourced from the BGS under the Open Government Licence.

## One-Click Installer for VS Code

1. Click to Install to VS Code

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_BGS_Sensor_Data_Local-0098FF?style=flat-square&logo=visualstudiocode&logoColor=ffffff)](vscode:mcp/install?%7B%22name%22%3A%22BGS%20Sensor%20Data%20Local%22%2C%22type%22%3A%22stdio%22%2C%22command%22%3A%22cmd%22%2C%22args%22%3A%5B%22%2Fc%22%2C%22python%22%2C%22%25USERPROFILE%25%5C%5Cmcp%5C%5Cbgs-senor-data-mcp-server.py%22%2C%22--stdio%22%5D%7D)

2. Open VS Code toggle Co-Pilot on
3. Switch to Agent Mode
4. (optional) Check if you're connected to the MCP
5. Start asking questions about UK geology! If you want the data to be visualised or captured somewhere ask AI to create an HTML file, jupyter notebook, or store the data in CSV file.

## Features

- **Point-specific geological data queries** at any UK coordinate
- **5 geological layers**: bedrock, superficial deposits, artificial ground, mass movement, linear features
- **High-resolution mapping**: 1:50,000 scale (visible 1:100,000 to 1:25,000 scale)
- **Multiple coordinate systems**: WGS84 (CRS:84) and British National Grid
- **3 output formats**: HTML, XML, and plain text
- **Map visualization**: Generate WMS GetMap URLs for GIS applications

## Available Geological Layers

| Layer | Description |
|-------|-------------|
| `bedrock` | Solid rocks beneath superficial deposits |
| `superficial_deposits` | Unconsolidated sediments above bedrock |
| `artificial_ground` | Made ground, worked ground, infilled ground |
| `mass_movement` | Landslides, rockfall, debris flows |
| `linear_features` | Faults, dykes, mineral veins |

## Installation

```bash
# Install dependencies
pip install fastmcp httpx
# or using uv:
uv sync

# Run the server
python server/main.py
```

## Example Queries

### 🗺️ **Guaranteed Visible Maps**

**London bedrock geology:**
```python
get_geology_map_url("BGS.50k.Bedrock", 51.45, -0.15, 51.55, -0.05, 450, 450, "image/gif")
```

**Southwest England superficial deposits (BGS example area):**
```python
get_geology_map_url("BGS.50k.Superficial.deposits", 50.991, -2.215, 51.051, -2.155)
```

**Edinburgh bedrock:**
```python
get_geology_map_url("BGS.50k.Bedrock", 55.90, -3.25, 56.00, -3.15)
```

**Peak District geology:**
```python
get_geology_map_url("BGS.50k.Bedrock", 53.25, -1.85, 53.35, -1.75)
```

**Lake District artificial ground:**
```python
get_geology_map_url("BGS.50k.Artificial.ground", 54.40, -3.10, 54.50, -3.00)
```

### 🔍 **Point-Specific Geological Queries**

**London geological analysis:**
```python
get_geology_at_location(51.5074, -0.1278, "bedrock", "text/html")
get_geology_at_location(51.5074, -0.1278, "superficial_deposits", "text/xml")
get_geology_at_location(51.5074, -0.1278, "artificial_ground", "text/plain")
```

**Scottish Highlands geology:**
```python
get_geology_at_location(57.1, -4.2, "bedrock", "text/html")
get_geology_at_location(57.1, -4.2, "mass_movement", "text/plain")
```

**Welsh valleys:**
```python
get_geology_at_location(51.75, -3.25, "bedrock")
get_geology_at_location(51.75, -3.25, "superficial_deposits")
```

**Geological hazard assessment:**
```python
get_geology_at_location(50.8, -4.1, "mass_movement")      # Devon coast
get_geology_at_location(54.4, -3.2, "mass_movement")      # Lake District
get_geology_at_location(53.3, -1.8, "mass_movement")      # Peak District
```

### 🏗️ **Engineering & Construction Queries**

**Urban development sites:**
```python
get_geology_at_location(53.4808, -2.2426, "artificial_ground")    # Manchester
get_geology_at_location(52.4862, -1.8904, "artificial_ground")    # Birmingham
get_geology_at_location(51.4816, -3.1791, "artificial_ground")    # Cardiff
```

**Foundation analysis:**
```python
get_geology_at_location(54.9783, -1.6178, "bedrock", "text/plain")     # Newcastle
get_geology_at_location(55.8642, -4.2518, "bedrock", "text/plain")     # Glasgow
get_geology_at_location(53.7967, -1.5492, "bedrock", "text/plain")     # Leeds
```

### ⛰️ **Geological Structure Analysis**

**Fault systems and linear features:**
```python
get_geology_at_location(54.2, -2.8, "linear_features")    # Yorkshire Dales
get_geology_at_location(52.1, -3.5, "linear_features")    # Mid Wales
get_geology_at_location(56.8, -5.1, "linear_features")    # Scottish Highlands
```

**Multi-layer geological profiling:**
```python
# Complete geological profile at one location
lat, lon = 53.2058, -0.5417  # Lincoln area
get_geology_at_location(lat, lon, "bedrock")
get_geology_at_location(lat, lon, "superficial_deposits") 
get_geology_at_location(lat, lon, "artificial_ground")
get_geology_at_location(lat, lon, "mass_movement")
get_geology_at_location(lat, lon, "linear_features")
```

### 🎯 **Regional Geological Mapping**

**Southern England chalk downs:**
```python
get_geology_map_url("BGS.50k.Bedrock", 50.8, -0.3, 50.9, -0.2)      # South Downs
get_geology_map_url("BGS.50k.Bedrock", 51.2, -1.8, 51.3, -1.7)      # North Wessex Downs
```

**Scottish geology:**
```python
get_geology_map_url("BGS.50k.Bedrock", 56.8, -5.2, 56.9, -5.1)      # Isle of Skye
get_geology_map_url("BGS.50k.Superficial.deposits", 57.6, -4.0, 57.7, -3.9)  # Moray Firth
```

**Welsh mining districts:**
```python
get_geology_map_url("BGS.50k.Artificial.ground", 53.1, -4.1, 53.2, -4.0)  # Snowdonia
get_geology_map_url("BGS.50k.Bedrock", 51.6, -3.4, 51.7, -3.3)             # Rhondda Valley
```

### 📊 **Service Discovery**

**Discover geological layers:**
```python
get_available_geology_layers()
```

**Get service capabilities:**
```python
get_capabilities()
```

**Service information:**
```python
get_service_info()
```

### 💡 **Geology Visualization Tips**

1. **Use small areas** (0.05-0.15° boxes) for visible maps at 1:50K scale
2. **Bedrock and superficial deposits** have the best coverage
3. **Mass movement** data is sparse - use in known landslide areas
4. **Linear features** show faults, dykes - try mountainous regions
5. **Artificial ground** is concentrated in urban/industrial areas
6. **Try GIF format** for better geological color representation

## API Reference

### Tools

#### `get_geology_at_location(latitude, longitude, geology_type, format_type)`
Get geological information at a specific geographic location.

**Parameters:**
- `latitude` (float): Latitude in decimal degrees (WGS84)
- `longitude` (float): Longitude in decimal degrees (WGS84)
- `geology_type` (str): Geological data type - bedrock, superficial_deposits, artificial_ground, mass_movement, linear_features
- `format_type` (str): Response format - text/html, text/xml, or text/plain

#### `get_available_geology_layers()`
Get available geological data layers from the BGS WMS service.

#### `get_capabilities()`
Get WMS capabilities document showing all available geological layers and metadata.

#### `get_geology_map_url(layer, min_lat, min_lon, max_lat, max_lon, width, height, format_type)`
Generate WMS GetMap URL for geological visualization.

**Parameters:**
- `layer` (str): Layer name (use get_available_geology_layers() to see options)
- `min_lat` (float): Minimum latitude (south boundary)
- `min_lon` (float): Minimum longitude (west boundary)
- `max_lat` (float): Maximum latitude (north boundary)
- `max_lon` (float): Maximum longitude (east boundary)
- `width` (int): Image width in pixels
- `height` (int): Image height in pixels
- `format_type` (str): Image format (image/png, image/gif, image/jpeg)

#### `get_service_info()`
Get information about the BGS Geology 50K WMS service.

## Data Source

- **Provider**: British Geological Survey (BGS) / UK Research and Innovation (UKRI)
- **License**: Open Government Licence
- **Attribution**: "Contains British Geological Survey materials © UKRI [year]"
- **Service URL**: https://map.bgs.ac.uk/arcgis/services/BGS_Detailed_Geology/MapServer/WMSServer

## Technical Details

- **WMS Version**: 1.3.0
- **Coordinate System**: WGS84 (CRS:84)
- **Coverage**: Great Britain (England, Wales, Scotland)
- **Scale**: 1:50,000 (visible between 1:100,000 and 1:25,000 scale)
- **Built with**: FastMCP 2.0, httpx

## Use Cases

- **Geological surveys**: Understand bedrock and surface geology
- **Engineering projects**: Foundation analysis and site investigation
- **Environmental planning**: Assess geological hazards and stability
- **Education**: Explore UK geological diversity and formation
- **Mining and quarrying**: Identify mineral resources and extraction sites
- **GIS applications**: Generate geological maps for spatial analysis

## Contributing

This MCP server provides a foundation for UK geological data access. Contributions welcome for additional BGS services, improved error handling, or extended dataset integration.