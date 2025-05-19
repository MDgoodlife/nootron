# Agentic Coding Setup for Nootron

## Project Structure

This project follows the PocketFlow framework for building LLM-powered applications with clear separation of concerns.

## Development Workflow

### Branch Strategy

1. **main**: Stable releases only
2. **dev**: Active development branch
3. **feature/***: Individual feature branches

### Development Process

1. Always work on the `dev` branch or feature branches
2. Test thoroughly before merging to main
3. Use semantic commits for clarity

### Code Standards

1. Follow PocketFlow patterns (Nodes, Flows, Utilities)
2. Keep utilities separate from core logic
3. Document all new features
4. Write tests for critical paths

### Commit Guidelines

```bash
# Feature commits
git commit -m "feat: add Notion integration node"

# Bug fixes
git commit -m "fix: resolve API timeout issue"

# Documentation
git commit -m "docs: update flow design patterns"

# Refactoring
git commit -m "refactor: simplify node communication"
```

### Testing Workflow

1. Unit test individual nodes
2. Integration test complete flows
3. End-to-end test user scenarios
4. Performance test with large datasets

### AI Agent Instructions

When working on this project as an AI agent:

1. **Read First**: Always check CLAUDE.md for project-specific guidance
2. **Design Before Code**: Create/update docs/design.md before implementing
3. **Small Changes**: Make incremental, testable changes
4. **Ask for Clarification**: When requirements are unclear, ask the human
5. **Test Everything**: Run tests before committing
6. **Document Changes**: Update relevant documentation

### Common Tasks

#### Adding a New Node
1. Design the node's purpose and interface
2. Implement in `nodes.py`
3. Add tests
4. Update documentation

#### Creating a New Flow
1. Design the flow diagram
2. Implement in `flow.py`
3. Add integration tests
4. Document the flow pattern

#### Adding Utilities
1. Determine if it's truly a utility (external interaction)
2. Create in `utils/` directory
3. Add unit tests
4. Document usage

### Security Notes

- Never commit secrets or API keys
- Use `.env` file for local development
- Use `.env.example` for documentation
- Keep `.gitignore` updated

### Collaboration

1. Use pull requests for all changes
2. Request reviews for significant changes
3. Keep PRs focused and small
4. Write clear PR descriptions

### Resources

- [PocketFlow Documentation](../CLAUDE.md)
- [Design Patterns](../docs/design.md)
- [Project PRD](./nootron-system.PRD)