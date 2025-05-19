# LLM Project Structure

This project follows the PocketFlow framework and Agentic Coding principles for building LLM applications.

## Features

- 🤖 Multiple LLM provider support (OpenAI, Anthropic)
- 🎨 Beautiful terminal interface with colors and styling
- 🔐 Automatic environment variable loading from `.env`
- 📝 Comprehensive logging and error handling
- 🚀 Ready-to-use Q&A interface
- 🧪 Built-in provider testing

## Directory Structure

```
nootron/
├── main.py            # Entry point with styled CLI interface
├── nodes.py           # Node definitions for the flow
├── flow.py            # Flow orchestration logic
├── utils/             # Utility functions
│   ├── __init__.py
│   ├── call_llm.py    # Enhanced LLM wrapper with multi-provider support
│   └── search_web.py  # Web search utility (optional)
├── requirements.txt   # Python dependencies
├── docs/              # Documentation
│   └── design.md      # High-level design document
├── .env               # Environment variables (API keys)
├── .cursorrules       # Cursor rules for AI-assisted development
└── CLAUDE.md          # Agentic coding guidelines
```

## Component Descriptions

### Core Files

- **`main.py`**: Enhanced CLI interface with:
  - Color-coded terminal output
  - Interactive menu system
  - LLM connection testing
  - Provider testing functionality
  - Clean screen transitions

- **`nodes.py`**: Contains all node class definitions following the three-step process:
  - `prep()`: Read and preprocess data from shared store
  - `exec()`: Execute main logic (typically LLM calls)
  - `post()`: Postprocess and write data back to shared store

- **`flow.py`**: Defines the flow structure by connecting nodes and creating the execution pipeline.

### Utilities Directory (`utils/`)

- **`call_llm.py`**: Advanced LLM wrapper with:
  - Automatic `.env` file loading
  - Multiple provider support (OpenAI, Anthropic)
  - Comprehensive error handling
  - Logging for debugging
  - Chat history support
  - Configurable parameters (temperature, max_tokens)

- **`search_web.py`**: Optional web search functionality template.

### Documentation (`docs/`)

- **`design.md`**: High-level design document following Agentic Coding principles.

## Getting Started

### 1. Prerequisites

Ensure you have Python 3.8+ installed on your system.

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd nootron

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Ensure your `.env` file contains the necessary API keys:
   ```env
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   # Add other keys as needed
   ```

2. The system will automatically load these keys when you run the application.

### 4. Running the Application

```bash
python main.py
```

You'll see a beautiful CLI interface with options:
- Test LLM connection
- Run Q&A mode
- Test different providers
- Exit

## Usage Examples

### Basic Q&A Mode

```bash
$ python main.py
# Select option 1 for Q&A mode
# Type your questions and get AI-powered answers
# Type 'quit' to exit
```

### Testing Providers

```bash
$ python main.py
# Select option 2 to test different LLM providers
# See comparative results from OpenAI and Anthropic
```

### Direct LLM Usage in Code

```python
from utils.call_llm import call_llm, call_openai, call_anthropic

# Default provider (OpenAI)
response = call_llm("What is Python?")

# Specific providers
openai_response = call_openai("Explain quantum computing")
anthropic_response = call_anthropic("Write a haiku about coding")

# With parameters
response = call_llm(
    "Explain AI", 
    provider="anthropic",
    temperature=0.3,
    max_tokens=500
)

# With chat history
messages = [
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": "AI is..."},
    {"role": "user", "content": "Tell me more"}
]
response = call_llm_with_history(messages)
```

## Development Guidelines

### Agentic Coding Principles

1. **Start Simple**: Begin with a minimal implementation and iterate
2. **Design First**: Document high-level design before implementation
3. **Separate Concerns**: Keep data storage (shared store) and processing (nodes) separate
4. **Fail Fast**: Errors are logged and displayed clearly for quick debugging

### Node Development

When creating new nodes:
1. Implement `prep()` to read from shared store
2. Implement `exec()` for main logic (keep it idempotent for retries)
3. Implement `post()` to write results and determine next action
4. Use retries for fault tolerance when needed

### Shared Store Design

Design your shared store structure early:
```python
shared = {
    "user": {
        "id": "user123",
        "context": {}
    },
    "results": {},
    "intermediate_data": {}
}
```

## Terminal Design

The CLI features a modern, colorful interface:
- 🟦 Blue: Information messages
- 🟩 Green: Success messages
- 🟥 Red: Error messages
- 🟨 Yellow: User prompts
- 🟪 Purple: Headers
- 🟦 Cyan: Decorative elements

## Best Practices

1. **Environment Variables**: All sensitive data is stored in `.env`
2. **Logging**: Comprehensive logging for debugging
3. **Error Handling**: Graceful error messages with helpful suggestions
4. **Testing**: Built-in testing functions for providers
5. **Documentation**: Keep this README and `docs/design.md` updated

## Common Patterns

- **Agents**: For dynamic decision-making flows
- **Workflows**: For sequential task processing
- **RAG**: For retrieval-augmented generation
- **Map-Reduce**: For processing large datasets in parallel

## Troubleshooting

### API Key Issues
- Ensure your `.env` file exists in the project root
- Check that API keys are valid and have proper permissions
- The system will show clear error messages if keys are missing

### Installation Issues
- Make sure you have Python 3.8+
- Use `pip install -r requirements.txt` to install all dependencies
- Some packages might require additional system dependencies

### Connection Issues
- Check your internet connection
- Verify API endpoints are accessible
- Review the logs for detailed error information

## Future Enhancements

- Add more LLM providers (Google, Azure, etc.)
- Implement caching for repeated queries
- Add conversation history persistence
- Create web interface option
- Support for streaming responses

Refer to the `.cursorrules` and `CLAUDE.md` files for detailed patterns and examples.