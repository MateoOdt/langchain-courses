# LangChain Course

My personal learning repo while following the course:

> **Learn AI Engineering: Build LangChain Agents with LangChain, LangGraph, RAG, MCP, Production Oriented Agentic AI**

Each file is a  self-contained experiment exploring one concept, so the commit history doubles as my learning log.

## What's inside

| File | Concept explored |
| --- | --- |
| `main.py` | Prompt templates + LangChain chains (`prompt \| llm`) with OpenAI / local Ollama models |
| `search_agents.py` | Agents with tools (Tavily search) and structured output via Pydantic schemas |
| `agents_react_loop.py` | ReAct agent loop built with LangChain tools, defensive prompting, and LangSmith tracing |
| `agent_raw_loop_function_calling.py` | A raw agent loop using Ollama function calling — to understand what LangChain does for you |
| `raw_react_prompt.py` | A ReAct loop implemented from scratch, parsing tool calls from raw text |

## Tech stack

- Python >= 3.14, managed with [`uv`](https://docs.astral.sh/uv/)
- [LangChain](https://python.langchain.com/) + LangSmith for tracing
- [OpenAI](https://platform.openai.com/) and local [Ollama](https://ollama.com/) models
- [Tavily](https://tavily.com/) for web search

## Setup

```bash
# install dependencies
uv sync

# add your API keys to a .env file
# OPENAI_API_KEY=...
# TAVILY_API_KEY=...
# LANGSMITH_API_KEY=...
```

## Running an example

```bash
uv run python main.py
uv run python search_agents.py
uv run python agents_react_loop.py
```

> Some scripts use local Ollama models (e.g. `qwen3:1.7b`). Make sure Ollama is
> running and the model is pulled: `ollama pull qwen3:1.7b`.

## Progress

Topics covered so far:

- [x] Prompt templates, chains & LangSmith tracing
- [x] Search agents with Tavily & tools
- [x] Structured agent output with Pydantic
- [x] LangChain ReAct agent loop & tool binding
- [x] Raw agent loops (function calling + ReAct from scratch)
- [ ] LangGraph
- [ ] RAG
- [ ] MCP
- [ ] Production-oriented agentic AI
