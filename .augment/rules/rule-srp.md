---
type: "manual"
---

Python Code Generation Guidelines (SRP-Compliant)
When generating Python code, follow these principles to ensure maintainability, testability, and full compliance with the Single Responsibility Principle (SRP) and the DRY (Don’t Repeat Yourself) principle.

✅ Single Responsibility Principle (SRP)
Each class, function, or module must have only one reason to change and should handle a single responsibility.

If a function mixes validation, business logic, and data persistence, split it into smaller, responsibility-focused components.

✅ Functions and Classes Design
Functions must be short and focused (ideally ≤ 30 lines) and clearly named after their specific responsibility.

Classes should not combine multiple concerns such as data access, business logic, and API response handling.

Break complex workflows into small, composable functions instead of large monolithic ones.

✅ Modularization and Dependency Management
Separate different concerns into distinct modules (e.g., validators.py, services.py, repository.py).

Adhere to high cohesion and low coupling principles.

Prefer Python’s standard library; avoid third-party dependencies unless strongly justified.

✅ Code Style Guidelines
Each function must do one thing only and be easily testable.

For logic that might evolve (e.g., external APIs, business rules), define contracts using Abstract Base Classes (abc) or Protocol interfaces.

Avoid mixing I/O operations with domain logic.

✅ Avoid Code Duplication (DRY Principle)
Proactively check for duplicate code and eliminate it.

Abstract repeated logic or data processing into helper functions, classes, or shared modules.

Favor reusable utilities over copy-paste coding practices.

✅ Before Generating Code
Provide a brief overview of module/component responsibilities and describe how SRP and DRY principles are applied.

Ensure the generated code is maintainable, testable, and easy to refactor.