# AI Engineering

The Decision Intelligence Platform (DIP) is developed using an AI-Driven Software Engineering approach.

Artificial Intelligence is considered an engineering capability rather than a code generation tool.

This directory contains all artifacts required to guide AI assistants during software development, ensuring consistency with the project's Product Vision, Architecture Decisions and Engineering Standards.

## Objectives

- Standardize AI interactions.
- Keep prompts versioned.
- Preserve architectural consistency.
- Improve implementation quality.
- Enable reproducible AI-assisted development.

## Directory Structure

```text
.ai/
│
├── context/
│
├── prompts/
│
├── templates/
│
└── reviews/
```

## Principles

- Architecture First
- Product First
- Human Review Required
- Small Iterations
- Commit Early
- Documentation Always Updated

## AI Workflow

1. Product defines the feature.
2. Architecture validates the solution.
3. AI generates the implementation.
4. Human reviews the result.
5. Tests are executed.
6. Documentation is updated.
7. Commit is created.

No AI-generated code is accepted without human review.

## AI Provider Independence

The `.ai` directory contains vendor-independent guidance for AI-assisted software engineering.

Its contents are intentionally designed to be reusable regardless of the AI provider used during development.

The current MVP recommends local execution using Ollama and an open-source coding model, but the project documentation must remain independent from any specific vendor.