"""Revenue Holdings — unified CLI for all developer tools."""

__version__ = "0.2.0"

# Tool registry: name -> (package, description, icon, pricing)
TOOLS = {
    "guard": {
        "package": "api-contract-guardian",
        "description": "OpenAPI breaking change detection and CI gating",
        "icon": "⚡",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/api-contract-guardian",
    },
    "sql": {
        "package": "json2sql",
        "description": "Convert JSON datasets to SQL INSERT statements",
        "icon": "↻",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/json2sql",
    },
    "deploy": {
        "package": "deploydiff",
        "description": "Infrastructure change preview with cost impact",
        "icon": "☁",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/deploydiff",
    },
    "drift": {
        "package": "configdrift",
        "description": "Detect configuration file drift across environments",
        "icon": "⌘",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/configdrift",
    },
    "ghost": {
        "package": "apighost",
        "description": "Mock API server from OpenAPI specs with VCR recording",
        "icon": "👻",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/apighost",
    },
    "auth": {
        "package": "apiauth",
        "description": "API key and JWT lifecycle management with encrypted store",
        "icon": "🔑",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/apiauth",
    },
    "envault": {
        "package": "envault",
        "description": "Env variable syncing, diffing, and secret rotation",
        "icon": "🔒",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/envault",
    },
    "schema": {
        "package": "schemaforge",
        "description": "Bidirectional ORM schema converter (11 formats)",
        "icon": "🔄",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/schemaforge",
    },
    "mcp": {
        "package": "click-to-mcp",
        "description": "Auto-wrap any Click/typer CLI as an MCP server",
        "icon": "🔌",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/click-to-mcp",
    },
    "deadcode": {
        "package": "deadcode",
        "description": "Detect unused exports, dead routes, orphaned CSS in TS/React",
        "icon": "🧹",
        "pricing": "Free / Pro",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/deadcode",
    },
}
