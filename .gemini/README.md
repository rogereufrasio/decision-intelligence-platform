# Gemini CLI Configuration

This directory contains instructions specifically designed for Gemini CLI.

The objective is to ensure that every interaction with Gemini follows the architectural, product and engineering standards defined for the Decision Intelligence Platform (DIP).

Gemini must always consider the following sources of truth, in order of priority:

1. AGENTS.md
2. docs/adr/
3. docs/product/
4. .ai/context/
5. .ai/rules/

Gemini-specific instructions complement—but never override—the project documentation.

## Responsibilities

Gemini CLI is responsible for:

- Generating production-quality code.
- Respecting the documented architecture.
- Keeping implementations simple.
- Explaining architectural decisions when requested.
- Updating documentation when changes impact architecture or product behavior.
- Never introducing unnecessary complexity.

Human review is mandatory before any generated code is committed.