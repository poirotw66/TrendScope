---
type: "manual"
---

When generating Python code, follow these principles to ensure compliance with the Single Responsibility Principle (SRP):

Single Responsibility Principle

Each class, function, or module must have only one reason to change and should handle a single responsibility.

If a function mixes validation, business logic, and data persistence, split it into smaller, responsibility-focused components.

Functions and Classes Design

Functions must be short and focused (ideally ≤ 30 lines) and clearly named after their specific responsibility.

Classes should not combine multiple responsibilities like data access, business logic, or API response handling in one place.

Break complex workflows into composable small functions instead of large monolithic ones.

Modularization and Dependency Management

Separate different concerns into different modules (e.g., validators.py, services.py, repository.py).

Adhere to high cohesion and low coupling principles.

Prefer Python’s standard library and avoid unnecessary third-party dependencies unless justified.

Code Style Guidelines

Functions should do one thing only and be easily testable.

For logic that might evolve (e.g., external APIs, business rules), use abstract base classes (abc) or interfaces (Protocol) to define contracts.

Avoid mixing I/O operations with domain logic.

Before generating code

Provide a brief overview of the module/component responsibilities and how SRP is applied.

Ensure the generated code is maintainable, testable, and easy to refactor.