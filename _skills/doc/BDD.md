Behavior-Driven Development (BDD) Skill

This skill provides a comprehensive guide to applying Behavior-Driven Development principles to your coding tasks. BDD is not just about tools; it's a methodology for shared understanding and high-quality implementation.
How to Use This Skill

When the user asks for a feature, bug fix, or refactor, apply the following mindset:

    Understand Behavior First: Do not start coding until you know what the system should do.
    Define Scenarios: Create or ask for concrete examples (Gherkin) of the expected behavior.
    Drive Implementation with Tests: Use the Red-Green-Refactor cycle.

Core Concepts
1. The BDD Cycle

The process flows from requirements to code:

    Discovery: Clarify requirements through examples (The "Three Amigos").
    Formulation: Write these examples as specific scenarios (Given/When/Then).
    Automation: Implement using TDD.

See BDD Best Practices for a detailed guide.
2. Writing Scenarios (Gherkin)

Scenarios are your "Executable Specifications".

    Keep them declarative (business focus).
    Avoid technical jargon and UI details.
    One behavior per scenario.
    Store in .feature files, NOT as code comments - this makes them executable and accessible to non-technical stakeholders.

See Cucumber Gherkin Guide for syntax and storage structure.
3. Red-Green-Refactor (TDD)

The engine of implementation:

    🔴 RED: Write a failing test for the scenario (or a unit thereof).
    🟢 GREEN: Write the minimal code to pass the test.
    🔵 REFACTOR: Clean up the code while keeping tests passing.

Quick Reference: The Iron Law

    "No production code is written without a failing test first."

If you write code before the test:

    You don't know if the test is capable of failing (false positives).
    You are biased by your implementation.
    You are writing legacy code from day one.
