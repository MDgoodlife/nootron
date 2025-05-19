---
layout: default
title: "Agentic Coding"
---

# Agentic Coding: Humans Design, Agents code!

> If you are an AI agent building LLM Systems, read this guide **VERY CAREFULLY**! Throughout development: (1) start small and simple, (2) design high-level (`docs/design.md`) before implementation, (3) frequently ask humans for feedback.
{: .warning }

## Agentic Coding Steps

Collaboration between Human System Design and Agent Implementation:

| Steps | Human | AI | Comment |
|:------|:-----:|:--:|:--------|
| 1. Requirements | ★★★ High | ★☆☆ Low | Humans understand requirements and context. |
| 2. Flow | ★★☆ Medium | ★★☆ Medium | Humans specify high-level design, AI fills details. |
| 3. Utilities | ★★☆ Medium | ★★☆ Medium | Humans provide APIs, AI helps implement. |
| 4. Node | ★☆☆ Low | ★★★ High | AI designs node types based on flow. |
| 5. Implementation | ★☆☆ Low | ★★★ High | AI implements based on design. |
| 6. Optimization | ★★☆ Medium | ★★☆ Medium | Humans evaluate, AI optimizes. |
| 7. Reliability | ★☆☆ Low | ★★★ High | AI writes tests and handles edge cases. |

1. **Requirements**: Clarify requirements and evaluate if AI system is appropriate.
   - AI good for: routine tasks (forms, emails), creative tasks with defined inputs (slides, SQL)
   - AI not good for: ambiguous problems requiring complex decisions (strategy, planning)
   - Keep user-centric, balance complexity vs. impact

2. **Flow Design**: Outline how AI system orchestrates nodes.
   - Identify patterns (MapReduce, Agent, RAG)
   - Draw mermaid diagrams
   - **If humans can't specify flow, AI can't automate it!**

3. **Utilities**: Implement external functions the AI needs:
   - Reading inputs (Slack, emails)
   - Writing outputs (reports, emails)
   - External tools (LLMs, web search)
   - LLM tasks are internal, not utilities

4. **Node Design**: Plan node data flow:
   - Use shared store pattern
   - `type`: Regular/Batch/Async
   - `prep`: Read from shared
   - `exec`: Call utilities
   - `post`: Write to shared

5. **Implementation**: KISS principle, fail fast, add logging

6. **Optimization**: Intuition first, then prompt engineering and in-context learning

7. **Reliability**: Node retries, logging, self-evaluation

## Example File Structure

```
nootron/
├── main.py
├── nodes.py
├── flow.py
├── utils/
│   ├── __init__.py
│   ├── call_llm.py
│   └── search_web.py
├── requirements.txt
└── docs/
    └── design.md
```

Example implementations provided below.

================================================
# Pocket Flow

A 100-line minimalist LLM framework for Agents, Task Decomposition, RAG, etc.

- **Lightweight**: Core graph abstraction in 100 lines, zero dependencies
- **Expressive**: Agents, Workflow, RAG, and more
- **Agentic-Coding**: Intuitive for AI agents building complex LLM apps

## Core Abstraction

LLM workflow as **Graph + Shared Store**:

- [Node](#node): handles simple tasks
- [Flow](#flow): connects nodes through Actions
- [Shared Store](#communication): node communication
- [Batch](#batch): data-intensive tasks  
- [Async](#async): asynchronous tasks
- [(Advanced) Parallel](#parallel): I/O-bound tasks

## Design Patterns

- Agent: autonomous decisions
- Workflow: task pipelines  
- RAG: retrieval with generation
- Map Reduce: split data tasks
- Structured Output: consistent formatting
- Multi-Agents: coordinate multiple agents

================================================
# Node

Smallest building block with 3 steps `prep->exec->post`:

1. `prep(shared)`
   - Read/preprocess from `shared`
   - Return `prep_res`

2. `exec(prep_res)`
   - Execute compute logic (LLMs, APIs)
   - ⚠️ Don't access `shared`, ensure idempotency
   - Return `exec_res`

3. `post(shared, prep_res, exec_res)`
   - Write to `shared`
   - Return action string (default: "default")

### Fault Tolerance

```python
node = SummarizeFile(max_retries=3, wait=10)
```

Optional `exec_fallback(prep_res, exc)` for graceful failure.

### Example

```python
class SummarizeFile(Node):
    def prep(self, shared):
        return shared["data"]
    
    def exec(self, prep_res):
        return call_llm(f"Summarize: {prep_res}")
    
    def post(self, shared, prep_res, exec_res):
        shared["summary"] = exec_res
```

================================================
# Flow

Orchestrates nodes with action-based transitions:

```python
# Basic transition
node_a >> node_b  # default action

# Named action
node_a - "action_name" >> node_b

# Branching
review - "approved" >> payment
review - "rejected" >> finish
review - "revision" >> revise >> review
```

### Nested Flows

Flows can contain other flows:

```python
payment_flow = Flow(start=validate)
inventory_flow = Flow(start=check_stock)
payment_flow >> inventory_flow
```

================================================
# Communication

Two communication methods:

1. **Shared Store** (primary)
   - Global dict all nodes access
   - `prep()` reads, `post()` writes
   - Design structure upfront

2. **Params** (for Batch only)
   - Local, immutable identifiers
   - Good for filenames, IDs

Example:
```python
shared = {
    "data": {},
    "summary": {},
    "config": {}
}
```

================================================
# Batch

Handle large inputs or rerun flows:

### BatchNode

```python
class MapSummaries(BatchNode):
    def prep(self, shared):
        return chunks  # returns iterable
    
    def exec(self, chunk):
        return call_llm(f"Summarize: {chunk}")
    
    def post(self, shared, prep_res, exec_res_list):
        shared["summary"] = "\n".join(exec_res_list)
```

### BatchFlow

Runs flow multiple times with different params:

```python
class SummarizeAllFiles(BatchFlow):
    def prep(self, shared):
        return [{"filename": f} for f in files]
```

================================================
# Design Patterns

### Agent
Dynamic actions based on context:
- Context management
- Action space design
- Branching decisions

### Workflow
Chain multiple nodes:
- Task decomposition
- Find granularity sweet spot
- Consider agents for edge cases

### RAG
Two-stage pipeline:
- Offline: chunk → embed → store index
- Online: embed query → retrieve → generate

### MapReduce
Break tasks into parallel parts:
- Map phase with BatchNode
- Reduce phase for aggregation

### Structured Output
YAML preferred over JSON:
```python
prompt = """
Output:
```yaml
summary:
  - point 1
  - point 2
```"""
```

================================================
# Utility Functions

Example LLM wrapper:

```python
def call_llm(prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content
```

Enhancements:
- Chat history support
- Caching (careful with retries)
- Logging