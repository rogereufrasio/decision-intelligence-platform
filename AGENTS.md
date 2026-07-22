# AGENTS.md

## Project

Decision Intelligence Platform (DIP)

Slogan

> Make better decisions through data, analytics and AI.

---

# Mission

Develop a real Decision Intelligence Platform using professional Product Management, Enterprise Architecture, Solution Architecture and AI-Driven Software Engineering practices.

The project prioritizes simplicity for the MVP while preserving scalability for future evolution.

---

# Development Principles

Every implementation must follow:

- Clean Architecture
- Domain Driven Design (DDD)
- SOLID Principles
- API First
- Provider Pattern
- Strategy Pattern
- Modular Monolith
- Cloud Ready
- Testable by Design

---

# Technology Stack

Frontend

- React
- Vite
- TypeScript
- Tailwind CSS
- shadcn/ui

Backend

- Python
- FastAPI
- Pydantic v2
- uv

Analytics

- DuckDB
- Parquet
- Power BI Desktop

Infrastructure

- Docker Compose

Quality

- Ruff
- Pytest
- ESLint
- Prettier

---

# AI Rules

Every generated implementation must:

- respect the documented architecture;
- avoid unnecessary abstractions;
- avoid overengineering;
- prioritize readability;
- use descriptive names;
- keep files small and cohesive;
- generate documentation when required.

---

## AI Assistant

This project adopts a vendor-independent AI strategy.

AI assistants are expected to:

- Follow all Architecture Decision Records (ADRs).
- Respect Product Documentation (DIPs).
- Preserve architectural consistency.
- Prefer simplicity over unnecessary complexity.
- Never introduce technology-specific assumptions unless explicitly requested.

The choice of AI provider is considered an implementation detail and must not influence the project's architecture or documentation.

---

# Coding Guidelines

Prefer composition over inheritance.

Avoid premature optimization.

Avoid unnecessary dependencies.

Keep functions small.

Prefer explicit code over clever code.

Every public method should have a clear responsibility.

---

# Documentation

Any architectural decision affecting the solution must be registered through an ADR.

Any significant product evolution must update the corresponding DIP documentation.

---

# Testing

Every feature should include:

- Unit Tests
- Integration Tests when applicable

End-to-End tests will be introduced after the MVP.

---

# Commit Convention

Use Conventional Commits.

Examples

feat:

fix:

docs:

refactor:

test:

chore:

---

# Review Checklist

Before considering a task complete, verify:

- Architecture respected
- Tests passing
- Documentation updated
- Build successful
- No duplicated logic
- No unnecessary complexity

---

# Final Principle

Always optimize for maintainability instead of short-term implementation speed.