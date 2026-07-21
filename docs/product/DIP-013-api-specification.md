# Decision Intelligence Platform

## Make better decisions through data, analytics and AI.

---

**Document ID:** DIP-013
**Title:** API Specification
**Version:** 1.0
**Status:** Approved
**Owner:** Solution Architecture
**Last Updated:** 2026-07-20

---

# 1. Purpose

This document defines the REST API exposed by the Decision Intelligence Platform (DIP).

The API follows RESTful principles and serves as the contract between the Frontend and the Decision Intelligence Platform.

The API is domain-oriented rather than provider-oriented.

---

# 2. Design Principles

The API follows these principles:

- REST First
- Resource Oriented
- Stateless
- JSON-based
- Versioned
- OpenAPI Compatible
- Provider Independent

---

# 3. Base URL

```text
/api/v1
```

---

# 4. Resource Overview

| Resource | Description |
|----------|-------------|
| /decisions | Decision lifecycle |
| /search | Search operations |
| /recommendations | Recommendation results |
| /providers | Provider information |
| /analytics | Analytical data |
| /health | Health check |

---

# 5. Endpoints

## Health

### GET /health

Returns application status.

Response

```json
{
  "status":"UP"
}
```

---

## Providers

### GET /providers

Returns available providers.

Example Response

```json
[
  {
    "name":"Amadeus",
    "type":"Flight"
  },
  {
    "name":"Duffel",
    "type":"Flight"
  }
]
```

---

## Search

### POST /search

Starts a decision search.

Request

```json
{
  "origin":"RIO",
  "destination":"BRC",
  "departureDate":"2026-09-03",
  "returnDate":"2026-09-07"
}
```

Response

```json
{
  "decisionId":"UUID"
}
```

---

## Decision

### GET /decisions/{id}

Returns the current decision.

---

## Recommendation

### GET /recommendations/{id}

Returns recommendation details.

Example

```json
{
    "recommendationScore":92,
    "bestOption":"OPTION_01"
}
```

---

## Analytics

### GET /analytics

Returns analytical summary.

---

# 6. HTTP Status Codes

| Code | Meaning |
|------|----------|
|200|Success|
|201|Created|
|400|Bad Request|
|401|Unauthorized|
|404|Not Found|
|429|Rate Limit|
|500|Internal Error|

---

# 7. Error Format

```json
{
  "code":"PROVIDER_TIMEOUT",
  "message":"Provider unavailable",
  "correlationId":"..."
}
```

---

# 8. Versioning Strategy

Versioning follows URI strategy.

Example

```
/api/v1
/api/v2
```

Major versions preserve backward compatibility whenever possible.

---

# 9. Security

The MVP does not require authentication.

Future versions may support:

- OAuth2
- JWT
- API Keys

---

# 10. OpenAPI

The entire API shall be documented automatically through FastAPI.

Endpoints:

```
/docs
/redoc
/openapi.json
```

---

# Related Documents

## Upstream

- DIP-011 — Solution Architecture
- DIP-012 — Data Architecture

## Downstream

- DIP-014 — Design System

---

# Conclusion

The REST API provides a stable contract between clients and the Decision Intelligence Platform while remaining independent of provider implementations.