import sys
import os
from flow import create_qa_flow
from utils.call_llm import call_llm

# Terminal colors and styles
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Print a styled header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def print_prompt(text):
    """Print styled prompt."""
    return input(f"{Colors.YELLOW}▶ {text}{Colors.ENDC}")

def test_llm_direct():
    """Test the LLM directly without using the flow."""
    print_header("Direct LLM Test")
    print_info("Testing LLM connection...")
    
    try:
        # Test with a simple prompt
        test_prompt = "Say 'Hello! LLM is working!' if you can read this."
        response = call_llm(test_prompt)
        print(f"\n{Colors.CYAN}LLM Response:{Colors.ENDC} {response}")
        print_success("LLM connection successful!")
        return True
    except Exception as e:
        print_error(f"Error connecting to LLM: {e}")
        print("\n" + Colors.YELLOW + "Please check:" + Colors.ENDC)
        print("  1. Your API keys are correctly set in the .env file")
        print("  2. You have installed all requirements: pip install -r requirements.txt")
        print("  3. Your internet connection is working")
        return False

def run_qa_flow():
    """Run the Q&A flow."""
    clear_screen()
    print_header("Q&A Flow Mode")
    print_info("Type 'quit' to exit")
    print(f"{Colors.CYAN}{'─'*60}{Colors.ENDC}\n")
    
    while True:
        # Create fresh shared state for each question
        shared = {
            "question": None,
            "answer": None
        }
        
        # Get user input
        user_input = print_prompt("Enter your question (or 'quit'): ")
        
        if user_input.lower() == 'quit':
            print_info("Goodbye!")
            break
        
        # For now, bypass the flow and use LLM directly
        # (since PocketFlow might not be installed properly)
        try:
            print(f"\n{Colors.BLUE}Thinking...{Colors.ENDC}")
            answer = call_llm(user_input)
            print(f"\n{Colors.GREEN}Answer:{Colors.ENDC}")
            print(f"{answer}\n")
            print(f"{Colors.CYAN}{'─'*60}{Colors.ENDC}\n")
        except Exception as e:
            print_error(f"Error: {e}")
            print_info("Make sure your API keys are set correctly.")

def main():
    """Main function with improved user experience."""
    clear_screen()
    print_header("LLM Project CLI")
    print(f"{Colors.BOLD}Welcome to your LLM-powered application!{Colors.ENDC}\n")
    
    # First, test if LLM is working
    if not test_llm_direct():
        print_error("\nExiting due to LLM connection error.")
        sys.exit(1)
    
    # Show menu
    print(f"\n{Colors.CYAN}Choose an option:{Colors.ENDC}")
    print(f"  {Colors.BOLD}1.{Colors.ENDC} Run Q&A mode")
    print(f"  {Colors.BOLD}2.{Colors.ENDC} Test different LLM providers")
    print(f"  {Colors.BOLD}3.{Colors.ENDC} Exit")
    
    choice = print_prompt("\nEnter your choice (1-3): ")
    
    if choice == "1":
        run_qa_flow()
    elif choice == "2":
        test_providers()
    else:
        print_info("Goodbye!")

def test_providers():
    """Test different LLM providers."""
    clear_screen()
    print_header("Testing LLM Providers")
    
    test_prompt = "What is 2+2? Answer with just the number."
    
    # Test OpenAI
    try:
        from utils.call_llm import call_openai
        print(f"\n{Colors.BLUE}Testing OpenAI GPT-4...{Colors.ENDC}")
        response = call_openai(test_prompt)
        print_success(f"OpenAI: {response}")
    except Exception as e:
        print_error(f"OpenAI Error: {e}")
    
    # Test Anthropic
    try:
        from utils.call_llm import call_anthropic
        print(f"\n{Colors.BLUE}Testing Anthropic Claude...{Colors.ENDC}")
        response = call_anthropic(test_prompt)
        print_success(f"Anthropic: {response}")
    except Exception as e:
        print_error(f"Anthropic Error: {e}")
    
    print(f"\n{Colors.GREEN}Provider testing complete!{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─'*60}{Colors.ENDC}")
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
    main()  # Return to main menu

if __name__ == "__main__":
    main()