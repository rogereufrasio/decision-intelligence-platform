# Architecture Rules

These rules are mandatory for every implementation.

## Layering

Business logic must never depend on infrastructure.

Dependencies always point inward.

## Providers

Every external service must be accessed through Provider interfaces.

Business logic must never call external APIs directly.

## Decision Engine

The Decision Engine is independent of providers.

It only consumes canonical models.

## Domain

Business rules belong inside the Domain Layer.

Never place business rules inside controllers or providers.

## API

API endpoints expose application use cases.

Controllers must remain thin.

## Data

Infrastructure owns persistence.

Domain never depends on databases.