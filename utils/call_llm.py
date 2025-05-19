import os
import logging
from typing import Dict, List, Optional, Union
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_llm(
    prompt: str, 
    provider: str = "openai",
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> str:
    """
    Call various LLM providers to generate a response.
    
    Args:
        prompt (str): The input prompt to send to the LLM
        provider (str): LLM provider to use ('openai', 'anthropic')
        model (str): Specific model to use (defaults to provider's best model)
        temperature (float): Temperature for response randomness (0-1)
        max_tokens (int): Maximum tokens in response
    
    Returns:
        str: The LLM's response
    """
    logger.info(f"Calling {provider} LLM with prompt length: {len(prompt)}")
    
    try:
        if provider.lower() == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key == "YOUR_API_KEY_HERE":
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            client = OpenAI(api_key=api_key)
            model = model or "gpt-4o"
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            result = response.choices[0].message.content
            
        elif provider.lower() == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            
            client = Anthropic(api_key=api_key)
            model = model or "claude-3-opus-20240229"
            
            response = client.messages.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens or 4096
            )
            result = response.content[0].text
            
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        logger.info(f"Received response of length: {len(result)}")
        return result
        
    except Exception as e:
        logger.error(f"Error calling {provider} LLM: {str(e)}")
        raise

# Convenience functions for specific providers
def call_openai(prompt: str, **kwargs) -> str:
    """Call OpenAI's GPT models."""
    return call_llm(prompt, provider="openai", **kwargs)

def call_anthropic(prompt: str, **kwargs) -> str:
    """Call Anthropic's Claude models."""
    return call_llm(prompt, provider="anthropic", **kwargs)

# Support for chat history
def call_llm_with_history(
    messages: List[Dict[str, str]], 
    provider: str = "openai",
    **kwargs
) -> str:
    """
    Call LLM with full message history.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        provider: LLM provider to use
        **kwargs: Additional arguments for the specific provider
    
    Returns:
        str: The LLM's response
    """
    if not messages:
        raise ValueError("Messages list cannot be empty")
    
    logger.info(f"Calling {provider} with {len(messages)} messages")
    
    try:
        if provider.lower() == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            client = OpenAI(api_key=api_key)
            model = kwargs.get("model", "gpt-4o")
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens")
            )
            return response.choices[0].message.content
            
        elif provider.lower() == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            
            client = Anthropic(api_key=api_key)
            model = kwargs.get("model", "claude-3-opus-20240229")
            
            # Convert messages to Anthropic format
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    # Anthropic doesn't have system role, prepend to first user message
                    if anthropic_messages and anthropic_messages[0]["role"] == "user":
                        anthropic_messages[0]["content"] = msg["content"] + "\n\n" + anthropic_messages[0]["content"]
                else:
                    anthropic_messages.append(msg)
            
            response = client.messages.create(
                model=model,
                messages=anthropic_messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 4096)
            )
            return response.content[0].text
            
    except Exception as e:
        logger.error(f"Error calling {provider} with history: {str(e)}")
        raise

if __name__ == "__main__":
    # Test the LLM call function
    test_prompt = "What is the meaning of life? Answer in one sentence."
    
    # Test different providers
    try:
        print("Testing OpenAI:")
        openai_response = call_openai(test_prompt)
        print(f"OpenAI: {openai_response}\n")
    except Exception as e:
        print(f"OpenAI Error: {e}\n")
    
    try:
        print("Testing Anthropic:")
        anthropic_response = call_anthropic(test_prompt)
        print(f"Anthropic: {anthropic_response}\n")
    except Exception as e:
        print(f"Anthropic Error: {e}\n")
    
    # Test with message history
    try:
        print("Testing with message history:")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a high-level programming language."},
            {"role": "user", "content": "What are its main uses?"}
        ]
        history_response = call_llm_with_history(messages)
        print(f"Response: {history_response}")
    except Exception as e:
        print(f"History Error: {e}")