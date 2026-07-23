# Ollama

## Purpose

Ollama is the official AI provider for the MVP development environment.

Its purpose is to execute local coding models while preserving the project's principles:

- Zero Cost
- Open Source First
- Vendor Independence
- Local Execution

---

## Installation

Windows

https://ollama.com/download

---

## Verify Installation

```bash
ollama --version
```

---

## Pull Recommended Model

```bash
ollama pull qwen2.5-coder:14b
```

If hardware resources are limited:

```bash
ollama pull qwen2.5-coder:7b
```

---

## Start Interactive Session

```bash
ollama run qwen2.5-coder:14b
```

or

```bash
ollama run qwen2.5-coder:7b
```

---

## Development Workflow

ChatGPT

↓

Architecture
Backlog
Review

↓

Prompt

↓

Ollama

↓

Implementation

↓

Developer

↓

Validation

↓

Git Commit

---

## Responsibilities

Ollama is responsible only for software implementation assistance.

Product decisions, architecture decisions and documentation remain governed by:

- ADRs
- DIPs
- AGENTS.md