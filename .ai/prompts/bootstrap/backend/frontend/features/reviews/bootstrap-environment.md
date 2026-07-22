# Bootstrap Environment Prompt

You are a Senior Software Engineer responsible for creating the initial development environment of the Decision Intelligence Platform.

Before generating code, review the project documentation.

Mandatory references:

- AGENTS.md
- docs/adr
- docs/product
- .ai/context

Objectives

- Preserve the documented architecture.
- Avoid unnecessary abstractions.
- Keep the MVP simple.
- Produce production-quality code.

Create the project foundation including:

Backend

- FastAPI
- uv
- Pydantic v2
- Ruff
- Pytest

Frontend

- React
- Vite
- TypeScript
- Tailwind CSS

Infrastructure

- Docker Compose

Quality

- ESLint
- Prettier

Do not implement business features.

Return a summary describing every created file.