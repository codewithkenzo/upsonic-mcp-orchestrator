# Technical Context

## 1. Technologies Used
- **Language:** Python (3.10+ required by Upsonic)
- **Core Framework:** Upsonic
- **API Framework:** FastAPI
- **Web Server (for FastAPI):** Uvicorn (with standard dependencies for performance)
- **Package Manager:** `uv`
- **LLM Interface:** OpenRouter (via Upsonic integration)
- **Tool Protocol:** Model Context Protocol (MCP)
- **Configuration:** python-dotenv

## 2. Development Setup
- **Project Root:** `/home/kenzo/Documents/Projects/upsonic-beta2/`
- **Backend Code:** `upsonic_backend/` within the project root.
- **Virtual Environment:** Located at `upsonic_backend/.venv/`, managed by `uv`.
- **Activation:** `source .venv/bin/activate` (or `.fish` depending on shell) within `upsonic_backend/`.
- **Dependencies:** Defined in `requirements.txt` (to be generated/maintained by `uv pip freeze`).
- **Configuration Files:**
    - `upsonic_backend/.env`: Stores API keys, file paths (`PROJECT_DIR="/home/kenzo/Documents/Projects/upsonic-beta2/"`, `MCP_CONFIG_PATH="./mcp-config.json"`).
    - `upsonic_backend/mcp-config.json`: Defines MCP servers accessible to the Upsonic client.

## 3. Technical Constraints
- Must adhere to Upsonic framework's API and documented usage patterns.
- All MCP interactions *must* go through the Upsonic client mechanism.
- File paths in MCP calls need careful handling to be relative to `PROJECT_DIR` or absolute as required by the specific MCP tool/server.
- Network access required for OpenRouter and potentially remote MCP servers.
- Initial state management for API tasks is in-memory; requires consideration for persistence (e.g., Redis, DB) if scaling beyond development.

## 4. Dependencies & Libraries (Initial)
```
# requirements.txt (Example - managed by uv)
upsonic
python-dotenv
fastapi
uvicorn[standard]
# Potentially others as features are added
```

## 5. Tool Usage Patterns
- **`uv`:** Used for all Python package management (install, freeze, environment creation).
- **`git`:** (Implied) For version control.
- **Cursor IDE:** Development environment, provides integrated terminal, potential MCP server hosting (like Steel tools), and AI assistance.
- **MCP Servers:** External processes invoked via Upsonic's MCP client. Configuration dictates how Upsonic finds and interacts with them (e.g., launching `uvx`, `npx`, `docker` commands based on `mcp-config.json`). 