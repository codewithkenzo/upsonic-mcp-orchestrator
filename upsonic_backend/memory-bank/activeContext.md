# Active Context

## 1. Current Focus
- Designing the prompt and logic for LLM-driven MCP task planning.
- Modifying the `/interact` endpoint to handle the planning phase and subsequent tool execution based on the LLM's plan.
- Preparing for initial Git repository creation and push.

## 2. Recent Changes
- Successfully tested direct execution of the loaded `filesystem` MCP tool via `agent.do()` running in a separate thread (`asyncio.to_thread`).
- Confirmed Upsonic correctly invokes the `npx` command defined for the tool class and the agent receives the result.
- Refined tool selection logic in `/interact` for explicit testing.

## 3. Next Steps (Immediate)
1.  **Git Repository Setup:** Initialize git, add files, make initial commit(s), create remote repository using `gh cli`, and push.
2.  **LLM Planning Prompt:** Design a prompt to instruct the agent (e.g., Claude 3.7 Sonnet) to analyze a user request and output a structured plan (e.g., JSON) detailing required MCP tool calls, including tool names and parameters.
3.  **Modify `/interact` for Planning:**
    *   First, call the agent with the user's message and the planning prompt.
    *   Add logic to parse the structured plan from the agent's response.
4.  **(Placeholder) Execute Plan:** Add placeholder logic to iterate through the parsed plan and print the intended MCP calls (actual execution of the planned sequence comes next).

## 4. Active Decisions & Considerations
- Basic MCP tool loading and execution via `agent.do` in a thread works.
- The next core challenge is getting the LLM to generate a usable plan for tool usage.
- The structure of the plan (JSON schema?) needs to be defined in the prompt.

## 5. Important Patterns & Preferences
- Incremental implementation: Planning -> Parsing -> Execution.

## 6. Learnings & Insights
- `asyncio.to_thread` is necessary to run blocking `agent.do` within FastAPI's async environment.
- Upsonic automatically handles the lifecycle of the MCP server process (`npx` in this case) when a tool class is passed to a task.

## 7. Project Structure (Corrected)
```
upsonic-beta2/
└── upsonic_backend/
    ├── .env
    ├── .venv/
    ├── mcp-config.json
    └── memory-bank/
        ├── activeContext.md
        ├── productContext.md
        ├── progress.md
        ├── projectbrief.md
        ├── systemPatterns.md
        └── techContext.md
``` 