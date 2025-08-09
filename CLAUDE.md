# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Running the geology 50K MCP server:**
```bash
python server/main.py
```

**Installing dependencies:**
```bash
pip install fastmcp httpx
# or if using uv:
uv sync
```

## Architecture Overview

This repository contains a **FastMCP 2.0 server** providing access to British Geological Survey (BGS) 1:50,000 scale geological maps via Web Map Service (WMS).

## Core Components

- **`BGS_GEOLOGY_WMS_URL`** - BGS WMS service endpoint
- **`GEOLOGY_LAYERS`** dictionary - Maps user-friendly geological layer names to BGS WMS layer names
- **`get_geology_data()`** function - Core WMS client for geological GetFeatureInfo requests
- **5 tools** for geological data access and visualization

## BGS Geology WMS Integration

Service: `https://map.bgs.ac.uk/arcgis/services/BGS_Detailed_Geology/MapServer/WMSServer`

**WMS Protocol Details:**
- Uses WMS 1.3.0 specification  
- CRS:84 coordinate system (lon,lat order)
- Supports `text/html`, `text/xml`, and `text/plain` response formats
- GetFeatureInfo requests use `i/j` pixel coordinates
- Bbox format: `west,south,east,north` for CRS:84
- **Scale constraints**: Data visible only between 1:100,000 and 1:25,000 scale

## Tool Architecture

### Available Tools
1. **`get_geology_at_location()`** - Point geological queries using GetFeatureInfo
2. **`get_available_geology_layers()`** - Geological layer discovery
3. **`get_capabilities()`** - WMS GetCapabilities request
4. **`get_geology_map_url()`** - GetMap URL generation for geological visualization
5. **`get_service_info()`** - Usage documentation

### Key Implementation Notes

- **Coordinate validation**: UK bounds (49.0°N-61.0°N, -8.0°W-2.0°E)
- **Bbox parameter handling**: Critical for GetMap requests - must validate min < max for both lat/lon
- **Layer name mapping**: User-friendly names map to BGS technical layer names
- **Error handling**: Simple string returns rather than exceptions for MCP compatibility
- **Async support**: Only `get_geology_at_location()` and `get_capabilities()` are async due to HTTP requests

## Available Geological Layers  

- `bedrock` → `"BGS.50k.Bedrock"`
- `superficial_deposits` → `"BGS.50k.Superficial.deposits"`
- `artificial_ground` → `"BGS.50k.Artificial.ground"`
- `mass_movement` → `"BGS.50k.Mass.movement"`
- `linear_features` → `"BGS.50k.Linear.features"`

## Development Notes

### FastMCP Patterns
- Use `@mcp.tool` decorator, type hints required, docstrings for descriptions
- Error handling returns strings rather than exceptions for MCP compatibility
- HTTP server mode configured for Cloudflare Tunnel access

### WMS Debugging
- Ensure small areas (0.05-0.15° boxes) for visible maps due to scale constraints
- Coordinate system: Uses CRS:84 (lon,lat order)
- For map visualization, try bedrock or superficial_deposits layers first for best coverage

### BGS Service Specifics
- **Geological data**: 1:50K scale with visibility constraints, sparse coverage for some layers (mass_movement)
- **No explicit rate limiting**: Use reasonable request sizes and frequencies
- **Map visualization**: Requires smaller areas for visible output due to scale constraints
- **Buffer size**: Uses 0.002° (~200m) buffer for GetFeatureInfo requests

### Critical Features
- **Scale sensitivity**: Strict scale visibility requirements (1:100,000 to 1:25,000)
- **Format options**: Supports XML format in addition to HTML and plain text
- **Coordinate order**: Uses CRS:84 (lon,lat order) throughout