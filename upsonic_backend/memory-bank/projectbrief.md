# Project Brief: Upsonic Orchestrator

## 1. Project Goal
Develop a Python-based backend application leveraging the Upsonic framework to orchestrate complex workflows. These workflows involve interaction with LLMs via OpenRouter and execution of tasks via MCP tools. The system aims to integrate existing technologies rather than reinventing core components, focusing on the orchestration logic within our codebase. It should be designed for future integration with a Next.js frontend via a dedicated API.

## 2. Core Problem
Need a reliable and structured way to chain LLM interactions (for planning and analysis) with task execution using standardized tools (MCP), managed by a robust framework (Upsonic).

## 3. High-Level Requirements
- Python backend using Upsonic.
- LLM interaction via OpenRouter.
- Task execution via MCP tools configured locally.
- FastAPI-based API for external interaction (future).
- Adherence to Upsonic documentation for its features (Memory, Knowledge, Graph, MCP Client).
- Emphasis on using existing, well-defined protocols and tools (MCP, OpenRouter).

## 4. Scope
- Initial focus on backend orchestration logic.
- Development environment setup (`uv`, Python).
- Core workflow implementation (LLM -> Plan -> MCP Execution via Upsonic).
- Basic API layer for task initiation and status checks.
- Frontend integration is out of scope for the initial phase. 