# Decision Intelligence Platform

## Make better decisions through data, analytics and AI.

---

**Document ID:** DIP-012
**Title:** Data Architecture
**Version:** 1.0
**Status:** Approved
**Owner:** Data Architecture
**Last Updated:** 2026-07-20

---

# 1. Purpose

This document defines the data architecture for the Decision Intelligence Platform (DIP).

It describes how data is acquired, normalized, stored and consumed throughout the decision lifecycle.

The architecture prioritizes simplicity for the MVP while establishing a foundation for future analytical and AI capabilities.

---

# 2. Data Principles

The platform follows these principles:

- Single Source of Truth
- Canonical Data Model
- Data Quality by Design
- Metadata First
- Explainability
- Reproducibility
- Open Formats

---

# 3. Data Lifecycle

```text
External APIs
        │
        ▼
Raw Data
        │
        ▼
Normalization
        │
        ▼
Canonical Dataset
        │
        ▼
Decision Engine
        │
        ▼
Analytics
```

Every recommendation is generated exclusively from canonical data.

---

# 4. Data Layers

## Raw Layer

Contains provider responses without transformation.

Characteristics:

- Immutable
- Provider-specific
- Short retention
- Used for debugging

---

## Canonical Layer

Contains normalized domain objects.

Characteristics:

- Provider independent
- Stable schema
- Business oriented
- Primary processing layer

---

## Analytics Layer

Optimized for reporting.

Characteristics:

- Aggregated
- Query optimized
- Historical
- Read-only

---

# 5. Canonical Entities

Core datasets include:

Decision

Alternative

Criterion

Recommendation

ProviderResponse

Preference

Each dataset is shared across all business domains.

---

# 6. Storage Strategy

Technology

- DuckDB
- Parquet

Reasons

- Zero operational cost
- Excellent analytical performance
- Open format
- Local execution
- Easy migration to cloud environments

---

# 7. Data Flow

```text
Provider APIs

↓

Provider Response

↓

Normalizer

↓

Canonical Dataset

↓

Decision Engine

↓

Recommendation

↓

Analytics Dataset

↓

Power BI
```

---

# 8. Metadata

Each dataset should include:

- Source Provider
- Collection Timestamp
- Processing Timestamp
- Schema Version
- Correlation ID

Metadata ensures traceability and reproducibility.

---

# 9. Data Quality

Validation rules include:

- Mandatory fields
- Type validation
- Currency consistency
- Date consistency
- Duplicate detection

Invalid records must never reach the Decision Engine.

---

# 10. Data Retention

| Layer | Strategy |
|--------|----------|
| Raw | Short-term |
| Canonical | Medium-term |
| Analytics | Long-term |

Retention periods should remain configurable.

---

# 11. Analytical Model

Primary KPIs include:

- Lowest Price
- Recommendation Score
- Flight Duration
- Number of Stops
- Hotel Rating
- Exchange Rate
- Weather Score
- Miles Value

The analytical model should evolve independently from provider implementations.

---

# 12. AI Readiness

The architecture prepares the platform for:

- Feature Engineering
- Recommendation Models
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- LLM-based Explainability

These capabilities are intentionally outside the MVP scope.

---

# 13. Future Evolution

Future enhancements include:

- Data Catalog
- Data Lineage
- Data Contracts
- Data Quality Dashboard
- Feature Store
- Lakehouse Architecture

Migration should preserve the canonical model.

---

# Related Documents

## Upstream

- DIP-009 — Domain Model
- DIP-010 — Architecture Vision
- DIP-011 — Solution Architecture

## Downstream

- DIP-013 — API Specification
- DIP-014 — Design System

---

# Conclusion

The Data Architecture establishes a lightweight but scalable foundation that enables trustworthy decision-making while preparing the platform for advanced analytics and AI-driven capabilities.