import os
from dotenv import load_dotenv
from upsonic import Agent, Task

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("Error: OPENROUTER_API_KEY not found in .env file.")
    print("Please add your OpenRouter API key to the .env file.")
else:
    # Set the API key in the environment for Upsonic to potentially pick up
    # (Though Upsonic might primarily rely on OPENAI_API_KEY or its own config)
    # If this fails, check Upsonic docs for explicit OpenRouter key passing
    # os.environ["OPENROUTER_API_KEY"] = api_key # Might not be needed if Upsonic uses OPENAI_API_KEY variable name
    os.environ["OPENAI_API_KEY"] = api_key # Upsonic examples often use OPENAI_API_KEY

    print("OPENROUTER_API_KEY loaded.")
    print("Attempting to run task via Upsonic Agent...")

    try:
        # Define the agent, specifying an OpenRouter model
        # Using claude-3.5-sonnet as an example
        # Format: openrouter/{provider}/{model-name}
        # Note: Upsonic might internally map this or expect specific naming.
        # Check Upsonic docs if 'openai/' prefix is needed even for OpenRouter.
        # Let's try the explicit OpenRouter path first.
        agent = Agent(
            "TestAgent",
            # model="openai/openrouter/anthropic/claude-3.5-sonnet" # Incorrect: Caused 'Unsupported LLM model' error
            model="openrouter/anthropic/claude-3.5-sonnet" # Correct format for OpenRouter
        )

        # Define a simple task
        task = Task("Tell me a short, one-sentence joke about programming.")

        # Run the task and print the output
        print("\n--- Agent Output ---")
        agent.print_do(task)
        print("--- End Agent Output ---")
        print("\nTask execution attempted.")

    except Exception as e:
        print(f"\nAn error occurred during agent execution: {e}")
        print("Please check:")
        print("- Your OPENROUTER_API_KEY in .env is correct.")
        print("- The model name 'openrouter/anthropic/claude-3.5-sonnet' is valid for your key and OpenRouter.")
        print("- Network connectivity.")
        print("- Upsonic compatibility with the 'openrouter/' prefix or if 'openai/' prefix is required.") 