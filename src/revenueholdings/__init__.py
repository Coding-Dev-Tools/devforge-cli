"""Revenue Holdings — unified CLI for all developer tools."""

__version__ = "0.1.0"

# Tool registry: name -> (package, description, icon, pricing)
TOOLS = {
    "guard": {
        "package": "api-contract-guardian",
        "description": "OpenAPI breaking change detection and CI gating",
        "icon": "⚡",
        "pricing": "Free / Pro $29/mo / Team $99/mo",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/api-contract-guardian",
    },
    "sql": {
        "package": "json2sql",
        "description": "Convert JSON datasets to SQL INSERT statements",
        "icon": "↻",
        "pricing": "Free / Pro $19/mo",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/json2sql",
    },
    "deploy": {
        "package": "deploydiff",
        "description": "Infrastructure change preview with cost impact",
        "icon": "☁",
        "pricing": "Free / Pro $25/mo / Team $79/mo",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/deploydiff",
    },
    "drift": {
        "package": "configdrift",
        "description": "Detect configuration file drift across environments",
        "icon": "⌘",
        "pricing": "Free / Team $49/mo / Enterprise $199/mo",
        "status": "ready",
        "url": "https://github.com/Coding-Dev-Tools/configdrift",
    },
}
