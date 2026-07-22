# Decision Intelligence Platform

## Make better decisions through data, analytics and AI.

---

**Document ID:** ADR-004  
**Title:** AI Vendor Independence  
**Status:** Approved  
**Date:** 2026-07-21

---

# Context

Artificial Intelligence plays an important role in the development workflow of the Decision Intelligence Platform (DIP).

Initially, the project considered using a specific AI coding assistant as the primary implementation tool. During project inception, changes in licensing and authentication requirements demonstrated that AI providers evolve rapidly and should not become architectural dependencies.

To ensure long-term maintainability, the project adopts a vendor-independent strategy for AI-assisted software engineering.

---

# Decision

The project documentation, prompts and engineering workflow shall remain independent from any specific AI provider.

For the MVP, the recommended implementation stack is:

- Ollama
- Qwen2.5-Coder (or equivalent open-source coding model)

Future providers may be adopted without requiring changes to the project's architecture or documentation.

Examples include:

- OpenAI
- Anthropic
- Google
- Azure OpenAI
- Self-hosted LLMs

The selected provider is considered an implementation detail of the development environment rather than a project dependency.

---

# Consequences

Positive:

- Avoids vendor lock-in.
- Preserves long-term maintainability.
- Supports zero-cost local development.
- Aligns with the project's Open Source First strategy.
- Simplifies future migrations between AI providers.

Trade-offs:

- AI-specific optimizations should remain outside the core project documentation.
- Development instructions must remain generic whenever possible.

---

# Status

Approved.