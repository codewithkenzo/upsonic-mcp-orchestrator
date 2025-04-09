import os
from dotenv import load_dotenv
from upsonic import Agent, Task

# Load environment variables
load_dotenv()

# Load ONLY the OpenRouter key
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Set ONLY the OPENAI_API_KEY variable (using the OpenRouter key)
if openrouter_api_key:
    os.environ["OPENAI_API_KEY"] = openrouter_api_key
    print("OPENROUTER_API_KEY loaded and set as OPENAI_API_KEY.")
else:
    print("Error: OPENROUTER_API_KEY not found in .env file. This test will fail.")
    # Optional: Exit if key is missing
    # exit()

print("--- Upsonic Memory Test (using OpenRouter) --- ")

try:
    # Revert to the OpenRouter model identifier
    agent = Agent(
        "MemoryTestAgentOpenRouter",
        model="openrouter/anthropic/claude-3.7-sonnet", # OpenRouter model format
        memory=True # Explicitly enable memory based on docs
    )

    # First interaction: Give the agent some information
    task1_description = "My favorite color is blue. Please remember this."
    print(f"\nTask 1: {task1_description}")
    task1 = Task(task1_description)
    print("\nAgent Response 1:")
    agent.print_do(task1)

    # Second interaction: Ask a question based on the previous information
    task2_description = "What is my favorite color that I just told you?"
    print(f"\nTask 2: {task2_description}")
    task2 = Task(task2_description)
    print("\nAgent Response 2:")
    agent.print_do(task2)

    print("\n--- Memory Test Complete --- ")

except Exception as e:
    print(f"\nAn error occurred during the memory test: {e}")
    print("Please check your OPENROUTER_API_KEY in .env, model name, and network connectivity.") 