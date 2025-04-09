# Product Context

## 1. Problem Solved
Provides a structured, reliable, and extensible backend system for automating complex tasks that require both LLM intelligence (planning, analysis, content generation) and concrete actions via tools (file manipulation, web interaction, API calls). It bridges the gap between high-level requests and step-by-step execution.

## 2. Core Functionality
- **Orchestration:** Manages the flow of information and actions between LLMs and MCP tools using Upsonic's framework.
- **LLM Interaction:** Leverages OpenRouter for flexible access to various LLMs.
- **Tool Execution:** Uses the Model Context Protocol (MCP) standard for interacting with a diverse set of tools, configured via a local `mcp-config.json`.
- **Workflow Management:** Employs Upsonic Graphs to define, execute, and monitor multi-step workflows, including potential parallelization and conditional logic.
- **State & Memory:** Utilizes Upsonic's built-in features for managing task context and short-term memory.

## 3. Target Users (Initial)
- Developers building applications requiring LLM-driven automation.
- Internal tools requiring complex backend processing.

## 4. User Experience Goals (Backend Focus)
- **Reliability:** Ensure workflows execute predictably and handle errors gracefully.
- **Extensibility:** Easily add new MCP tools and define new Upsonic Graphs/workflows.
- **Configurability:** Simple configuration via `.env` and `mcp-config.json`.
- **Observability:** Provide mechanisms (API endpoints) to monitor task status.
- **Adherence to Standards:** Strictly follow Upsonic documentation and MCP specifications. 