# Upsonic Framework Features Overview

This document summarizes the key features and concepts of the Upsonic framework based on publicly available documentation (primarily docs.upsonic.ai and the GitHub repository) as of the time of writing.

## Core Concepts

1.  **Task-Centric Design:**
    *   The `Task` object is the fundamental unit of work.
    *   Tasks define the job, description, context (data, other tasks), tools, knowledge bases, and desired response format.
    *   Decouples specific jobs from agents, allowing agents to handle multiple, varied tasks.
    *   Enhances programmability by defining dependencies externally rather than embedding them in agents.
    *   [Source: Task Docs](https://docs.upsonic.ai/concepts/task)

2.  **Agent:**
    *   The entity that executes `Task` objects.
    *   Can be assigned roles (e.g., "Product Manager", "Coder") which influences behavior (Automatic Characterization).
    *   Can be configured with specific LLM models (`model=...`).
    *   Supports **Memory** for context continuity (requires explicit activation `memory=True` and potentially `agent_id_` for persistence).
    *   Supports **Reflection** (`reflection=True`) for self-monitoring and quality assurance.
    *   Can be given a persona (`name`, `contact`, `company_url`, `company_objective`) to act more like a human.
    *   [Source: Agent Docs](https://docs.upsonic.ai/concepts/agent)

3.  **Reliability Layer:**
    *   A key focus of the framework, designed to improve the accuracy and consistency of LLM outputs.
    *   Features include Verifier Agents (validate outputs), Editor Agents (refine based on feedback), Rounds (iterative verification), and Loops (feedback checkpoints).
    *   Activated via `reliability_layer` parameter in `Agent`.
    *   [Source: GitHub Readme](https://github.com/Upsonic/Upsonic), [Docs Nav](https://docs.upsonic.ai/)

4.  **Memory:**
    *   Provides contextual continuity for agents.
    *   Requires explicit enabling (`memory=True` in `Agent`).
    *   Uses disk-based persistence tied to a unique `agent_id_` for continuity across sessions/restarts.
    *   [Source: Memory Docs](https://docs.upsonic.ai/concepts/memory), [Agent Docs](https://docs.upsonic.ai/concepts/agent)

5.  **Knowledge Base:**
    *   Mentioned as a concept that can be added to `Task` objects, likely for providing domain-specific information.
    *   Details on implementation, data sources, or persistence mechanism require further investigation in the docs.
    *   [Source: Docs Nav](https://docs.upsonic.ai/)

6.  **LLM Support:**
    *   Integrates with multiple LLM providers (OpenAI, Anthropic, Azure, AWS Bedrock, DeepSeek).
    *   Configuration typically via environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.) loaded from `.env` or the environment.
    *   Specific model selected using the `model` parameter in `Agent` or `Direct` calls (e.g., `openai/gpt-4o`, `claude/claude-3-5-sonnet`).
    *   [Source: LLM Support Docs](https://docs.upsonic.ai/concepts/llm_support)

7.  **Direct LLM Call:**
    *   Allows making calls directly to LLMs without the full agent abstraction.
    *   Useful for simpler tasks, potentially faster and cheaper.
    *   Uses the `Direct` class.
    *   Can still utilize tools and structured responses.
    *   [Source: GitHub Readme](https://github.com/Upsonic/Upsonic), [Intro Docs](https://docs.upsonic.ai/introduction)

8.  **Graph:**
    *   Mentioned as a concept for orchestrating more complex workflows involving multiple tasks and potentially agents.
    *   Likely enables defining dependencies, sequences, and potentially parallel execution.
    *   Details require further investigation in the docs.
    *   [Source: Docs Nav](https://docs.upsonic.ai/)

## Tool Integration

9.  **MCP Tools (Model Context Protocol):**
    *   Primary way to integrate external tools and data sources.
    *   Upsonic supports running and connecting to MCP Servers (uvx, npx, docker based).
    *   MCP tools are defined in Upsonic using Python classes containing `command`, `args`, and optional `env` attributes.
    *   These tool classes are passed to the `Task` object via the `tools=[...]` list.
    *   [Source: MCP Tools Docs](https://docs.upsonic.ai/concepts/mcp_tools), [GitHub Readme](https://github.com/Upsonic/Upsonic)

10. **Custom Tools:**
    *   Supports using standard Python functions within classes as tools, providing another integration method.
    *   [Source: GitHub Readme](https://github.com/Upsonic/Upsonic), [Docs Nav - Tools](https://docs.upsonic.ai/)

## Output & Deployment

11. **Object as Response:**
    *   Allows defining a desired output structure using Pydantic-like classes (inheriting `ObjectResponse`).
    *   The LLM's output is formatted into an instance of this class, enabling programmatic use.
    *   Passed to the `Task` via the `response_format=...` parameter.
    *   [Source: GitHub Readme](https://github.com/Upsonic/Upsonic), [Intro Docs](https://docs.upsonic.ai/introduction)

12. **Scalability & Deployment:**
    *   Designed with scalability in mind; core components can run server-side (e.g., via Docker).
    *   Supports local deployment.
    *   Allows for lightweight client integration.
    *   [Source: Intro Docs](https://docs.upsonic.ai/introduction), [Docs Nav - Deploy Locally](https://docs.upsonic.ai/)

13. **Secure Runtime:**
    *   Provides an isolated environment for running agents (options: On-prem, Cloud).
    *   [Source: Intro Docs](https://docs.upsonic.ai/introduction)

## Other Features

14. **Integrations (Browser/Computer Use):**
    *   Specific capabilities mentioned for agents interacting directly with browsers or desktop environments (details need investigation).
    *   [Source: Docs Nav - Integrations](https://docs.upsonic.ai/), [GitHub Readme](https://github.com/Upsonic/Upsonic)

15. **Debugging:**
    *   Mentioned as a concept, specific tools/methods need investigation.
    *   [Source: Docs Nav - Debugging](https://docs.upsonic.ai/)

16. **Parallel Task Execution:**
    *   Mentioned as a capability, likely related to Graph execution.
    *   [Source: Docs Nav](https://docs.upsonic.ai/)

17. **Telemetry:**
    *   Collects anonymous usage data (can be disabled via `UPSONIC_TELEMETRY=False` env var).
    *   [Source: GitHub Readme](https://github.com/Upsonic/Upsonic)

18. **Canvas:**
    *   Mentioned in documentation navigation, purpose unclear from snippets.
    *   [Source: Docs Nav](https://docs.upsonic.ai/) 