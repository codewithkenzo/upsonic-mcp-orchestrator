import json
import os
import pathlib
from dotenv import load_dotenv
from upsonic import Agent, Task
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import subprocess
import signal
import time
import asyncio

# --- Configuration & Setup ---

def load_environment():
    """Loads environment variables and sets API keys."""
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        print("OpenRouter API Key loaded and set.")
    else:
        print("Warning: OPENROUTER_API_KEY not found in .env file.")

# Load environment variables on script start
load_environment()

# --- MCP Tool Loading ---

def load_mcp_tools_from_config() -> dict:
    """Loads MCP server definitions from JSON and creates dynamic classes."""
    mcp_config_path_str = os.getenv("MCP_CONFIG_PATH", "./mcp-config.json")
    mcp_config_path = pathlib.Path(mcp_config_path_str)
    loaded_tools = {}

    if not mcp_config_path.is_file():
        print(f"Warning: MCP config file not found at '{mcp_config_path}'")
        return loaded_tools

    print(f"Loading MCP tools from '{mcp_config_path}'")
    try:
        with open(mcp_config_path, 'r') as f:
            config_data = json.load(f)

        mcp_servers = config_data.get("mcpServers", {})

        for tool_name, tool_config in mcp_servers.items():
            class_name = tool_name.capitalize() + "MCPTool"
            command = tool_config.get("command")
            args = tool_config.get("args", [])
            env = tool_config.get("env", {})
            description = tool_config.get("description", f"MCP tool: {tool_name}") # Add description

            if not command:
                print(f"Warning: Skipping tool '{tool_name}' due to missing 'command'.")
                continue

            # Dynamically create the class with necessary attributes
            # Use type(name, bases, dict)
            tool_class = type(
                class_name,
                (object,), # Base class
                {
                    "command": command,
                    "args": args,
                    "env": env,
                    "description": description # Add description attribute if needed by Upsonic/LLM
                    # Add __doc__?
                    # "__doc__": description
                }
            )

            loaded_tools[tool_name] = tool_class
            print(f"  - Loaded MCP tool: '{tool_name}' as class {class_name}")

    except json.JSONDecodeError as e:
        print(f"Error parsing MCP config file '{mcp_config_path}': {e}")
    except Exception as e:
        print(f"Error loading MCP tools: {e}")

    return loaded_tools

# Load tools globally on startup
mcp_tool_classes = load_mcp_tools_from_config()

# --- Agent Initialization ---

def initialize_agent(agent_id: str, model_name: str) -> Agent:
    """Initializes and returns an Upsonic Agent with memory enabled."""
    print(f"Initializing agent '{agent_id}' with model '{model_name}'")
    try:
        agent = Agent(
            agent_id, # Role/Name for the agent
            agent_id_=agent_id, # Agent ID for persistent memory (if needed later)
            model=model_name,
            memory=True # Ensure memory is enabled
        )
        return agent
    except Exception as e:
        print(f"Error initializing agent: {e}")
        raise HTTPException(status_code=500, detail=f"Agent initialization failed: {e}")

# --- API Definition ---

app = FastAPI()

class InteractionRequest(BaseModel):
    message: str
    model: str | None = "openrouter/anthropic/claude-3.7-sonnet" # Default model update
    agent_id: str = "default_user_agent" # Simple default ID for now

class InteractionResponse(BaseModel):
    reply: str

# In-memory store for agents (simple approach for now)
# WARNING: This is not suitable for production - agents are tied to the server process life
agents_store = {}

@app.post("/interact", response_model=InteractionResponse)
async def handle_interaction(request: InteractionRequest):
    """Handles user interaction, initializes agent, selects tools, and runs task."""
    print(f"Received interaction request for agent '{request.agent_id}' with message: '{request.message}'")

    if request.agent_id not in agents_store:
        print(f"Creating new agent instance for '{request.agent_id}'")
        agents_store[request.agent_id] = initialize_agent(
            agent_id=request.agent_id,
            model_name=request.model
        )
    else:
        print(f"Using existing agent instance for '{request.agent_id}'")

    agent = agents_store[request.agent_id]

    # --- Tool Selection (Placeholder & Test Logic) ---
    # TODO: Replace this with LLM-driven planning based on request.message
    selected_tool_classes = []
    message_lower = request.message.lower()
    
    # Explicit test trigger
    if "use filesystem tool" in message_lower:
        if "filesystem" in mcp_tool_classes:
            print("Explicitly selecting 'filesystem' tool for test.")
            selected_tool_classes.append(mcp_tool_classes["filesystem"])
        else:
            print("Warning: 'filesystem' tool requested for test, but not loaded.")
    # Fallback keyword-based selection
    elif ("file" in message_lower or "read" in message_lower or "write" in message_lower or "list" in message_lower):
        if "filesystem" in mcp_tool_classes:
            print("Selecting 'filesystem' tool based on keywords.")
            selected_tool_classes.append(mcp_tool_classes["filesystem"])
    
    # Add more placeholder logic for other tools here...

    # Create the task with selected tools
    print(f"Creating task with tools: {[tool.__name__ for tool in selected_tool_classes]}")
    task = Task(
        description=request.message,
        tools=selected_tool_classes # Pass the list of selected tool classes
    )

    try:
        print("Attempting to run blocking agent.do in separate thread...")
        # Run the potentially blocking agent.do in a separate thread
        result = await asyncio.to_thread(agent.do, task)
        print(f"...Task execution finished. Agent raw result: {result}")
        reply_text = str(result) if result is not None else "Agent produced no response."
        return InteractionResponse(reply=reply_text)

    except Exception as e:
        print(f"Error during task execution: {e}")
        raise HTTPException(status_code=500, detail=f"Task execution failed: {e}")

# --- Port Killing Logic ---

PORT = 8000

def kill_process_on_port(port: int):
    """Attempts to find and kill process(es) listening on the specified port."""
    print(f"Checking if port {port} is in use...")
    try:
        # Find PIDs using lsof. -t gives only PIDs, -i specifies network files.
        result = subprocess.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True, check=False)
        pid_lines = result.stdout.strip().splitlines()

        if not pid_lines:
            print(f"No process found using port {port}.")
            return

        killed_one = False
        for pid_str in pid_lines:
            if pid_str.isdigit():
                pid = int(pid_str)
                print(f"Found process {pid} using port {port}. Attempting to terminate...")
                try:
                    # Send SIGTERM first (graceful shutdown)
                    os.kill(pid, signal.SIGTERM)
                    print(f"Sent SIGTERM to process {pid}. Waiting briefly...")
                    killed_one = True
                    # Check if it's still alive after a short delay
                    try:
                        time.sleep(0.5) # Reduced wait time
                        os.kill(pid, 0) # Check if process exists
                        print(f"Process {pid} still alive after SIGTERM. Sending SIGKILL...")
                        os.kill(pid, signal.SIGKILL) # Force kill
                        print(f"Sent SIGKILL to process {pid}.")
                        killed_one = True
                    except OSError:
                        print(f"Process {pid} terminated successfully after SIGTERM.")

                except OSError as e:
                    print(f"Could not terminate process {pid}: {e}. It might have already exited or requires higher privileges.")
                except Exception as e:
                    print(f"An unexpected error occurred while trying to kill process {pid}: {e}")
            else:
                print(f"lsof returned non-PID line: '{pid_str}'")

        if killed_one:
            print("Waiting a moment after kill attempts...")
            time.sleep(1) # Wait a bit longer if we actually killed something
        else:
             print("No valid PIDs found in lsof output.")

    except FileNotFoundError:
        print("Warning: 'lsof' command not found. Cannot check/kill process on port.")
    except Exception as e:
        print(f"An error occurred while checking port {port}: {e}")

# --- Main Execution --- (for running with uvicorn)

if __name__ == "__main__":
    # Attempt to kill any existing process on the port before starting
    kill_process_on_port(PORT)

    print(f"Starting FastAPI server with uvicorn on port {PORT}...")
    # Run Uvicorn
    uvicorn.run("main_orchestrator:app", host="127.0.0.1", port=PORT, reload=True) 