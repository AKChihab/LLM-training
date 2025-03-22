from dotenv import load_dotenv
import os
# Apply the monkey patch for pydantic.networks
import sys
import types
from pydantic import AnyUrl

# Monkey-patch for Pydantic v2 compatibility
dummy_networks = types.ModuleType("pydantic.networks")
dummy_networks.Url = AnyUrl
dummy_networks.AnyUrl = AnyUrl
sys.modules["pydantic.networks"] = dummy_networks
import pydantic
# (Optional) You can also patch pydantic.networks.Url if needed:
pydantic.networks.Url = AnyUrl

from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings

async def main():
    load_dotenv()
     
    endpoint = os.getenv("ENDPOINT_URL", "https://openaillmdemo93.openai.azure.com/")
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
    api_key = os.getenv("OPENAI_API_KEY")

    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        endpoint=str(endpoint), 
        deployment_name=str(deployment), 
        api_key=api_key,
        )
    
    kernel.add_service(chat_completion)
    
    prompt_text = """
    I need to understand what are the most important trends in the crypto market. 
    For example what is the social sentiment about the market, 
    what are the new projects that are getting attention, what are the most popular coins, etc.
    """
    # Align the service id in your settings with your deployment name ("gpt-35-turbo")
    settings = {
        "gpt-35-turbo": PromptExecutionSettings(service_id="gpt-35-turbo", max_tokens=400, temperature=1.0),
    }
    

    kernel.add_function(
        prompt= prompt_text,
        plugin_name="analyst", 
        function_name = "crypto_analyst", 
        prompt_execution_settings=settings,)
    
    chat_history = ChatHistory()
    chat_history.add_user_message("I'm Chihab, I am 3 years old.")
 
    result = await kernel.invoke(plugin_name="analyst", function_name="crypto_analyst",chat_history=chat_history)
    print(result)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())