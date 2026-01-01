# Agent Instructions Document (AID)

## Purpose

This document provides explicit instructions and best practices for Large Language Models (LLMs) tasked with generating or editing code for the HTMX Labs project. It is designed to ensure code quality, maintainability, and alignment with project conventions.

---

## Related Documents for AI-Assisted Coding

To maximize the effectiveness, safety, and maintainability of AI-generated code, the following documents are highly recommended for any project using LLMs for code generation:

### 1. Product Requirements Document (PRD)
- **Purpose:** Defines the product's goals, features, user stories, and technical requirements.
- **Benefit:** Ensures the AI understands the "why" and "what" behind the code, not just the "how".

### 2. Agent Instructions Document (AID) (this document)
- **Purpose:** Provides explicit instructions, best practices, and constraints for LLMs.
- **Benefit:** Guides the AI to produce code that matches project standards and avoids common pitfalls.

Make these documents easily accessible to both humans and LLMs. Reference them in prompts and keep them up to date as the project evolves.

---
## 1. General Principles

- **Follow Project Conventions:** Adhere to the existing code style, structure, and naming conventions found in the codebase.
- **Be Explicit:** Prefer explicit, readable code over clever or overly terse solutions.
- **Minimize Dependencies:** Use only the libraries and frameworks already present in the project unless otherwise instructed.
- **Documentation:** Add or update docstrings and comments where appropriate, especially for public functions, classes, and complex logic.
- **Atomic Commits:** Each code change should be atomic and focused on a single concern or feature.

---

## 2. Code Generation Guidelines

- **Correctness First:** Ensure all code is syntactically correct and logically sound.
- **Security:** Never expose secrets, credentials, or sensitive data. Follow Django security best practices.
- **Performance:** Write efficient code, but not at the expense of readability or maintainability.
- **Testing:** When adding new features or fixing bugs, include or update tests if the project has a test suite.

---

## 3. Prompting Instructions for LLMs

When generating code for this project, always:

1. **Understand the Context:** Read the relevant code and documentation before making changes.
2. **Preserve Functionality:** Do not remove or break existing features unless explicitly instructed.
3. **Use Django Best Practices:** For backend code, use Django idioms (views, templates, forms, models, etc.).
4. **Use HTMX Idioms:** For frontend, leverage htmx attributes and patterns as demonstrated in the examples.
5. **Frontend Consistency:** Use Bulma CSS classes and structure for UI components.
6. **Fragmentation:** When returning HTML fragments, ensure they are self-contained and follow the partials pattern used in the project.
7. **Error Handling:** Handle errors gracefully, both in backend and frontend code.

---

## 4. Code Review Checklist

Before submitting code, ensure:

- [ ] Code is formatted and linted according to project standards.
- [ ] No secrets or sensitive data are present.

---


## 5. Prohibited Actions

- Do not introduce new frameworks or major dependencies without approval.
- Do not use inline JavaScript except where required for htmx or Bulma integration.
- Do not expose or log sensitive information.
- Do not break existing URLs, endpoints, or API contracts.

---
