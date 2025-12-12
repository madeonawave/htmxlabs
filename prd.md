# Product Requirements Document (PRD)

## Project: HTMX Labs ([htmxlabs.com](https://htmxlabs.com))

### 1. Purpose

HTMX Labs is an educational and demonstration website designed to showcase the capabilities of [htmx](https://htmx.org/) for building modern, dynamic web applications with minimal JavaScript. The site provides a wide range of interactive examples, code snippets, and real-world use cases, all powered by a Django backend.

---

### 2. Goals

- **Demonstrate** the power and flexibility of htmx through live, interactive examples.
- **Educate** developers on how to use htmx for AJAX, real-time updates, UI components, and more.
- **Provide** a resource for learning, experimenting, and sharing htmx techniques.
- **Enable** easy extension with new examples and integrations.

---

### 3. Features

#### 3.1. Examples Gallery
- A categorized and searchable gallery of htmx examples (AJAX, forms, tables, real-time, integrations, etc.).
- Each example includes:
  - Live demo
  - Source code snippet
  - Description and tags
  - Difficulty level

#### 3.2. Interactive Demos
- Users can interact with each example directly on the site.
- Examples cover a wide range of use cases, such as:
  - AJAX requests and partial page updates
  - Real-time features (WebSockets, Server-Sent Events, polling)
  - Form handling and validation
  - UI components (modals, tabs, tables, etc.)
  - Integrations with APIs and backend logic

#### 3.3. Documentation
- Getting started guide for htmx and the site itself.
- Core htmx attributes and usage patterns.
- Reference for each example.

#### 3.4. Backend
- Django backend serving all pages, fragments, and API endpoints.
- Examples are rendered server-side and support htmx requests.
- Easy to add new examples via JSON or Django templates.

#### 3.5. Frontend
- Modern, responsive UI using Bulma CSS and custom styles.
- Mobile-friendly navigation and layout.
- Code highlighting and copy-to-clipboard for code snippets.

#### 3.6. Community & Contribution
- Clear instructions for contributing new examples.
- Open source, MIT licensed.

---

### 4. User Stories

- **As a developer**, I want to see live htmx examples so I can learn how to use it in my projects.
- **As a beginner**, I want simple, step-by-step demos to understand the basics of htmx.
- **As an advanced user**, I want to explore real-time, API, and integration examples.
- **As a contributor**, I want to easily add new examples and documentation.

---

### 5. Technical Requirements

- **Backend:** Django (Python 3.10+)
- **Frontend:** Bulma CSS, htmx.js, FontAwesome
- **Hosting:** Compatible with any ASGI host 
- **Data:** Examples stored in JSON and/or Django templates
- **Testing:** Manual and automated tests for core features

---

### 6. Success Metrics
- Django-mammoth is used for visitor metrics

---

### 7. Out of Scope

- No user authentication or accounts (read-only, demo-focused)
- No persistent user data or profiles
- No paid features or commercial upsells

---

### 8. Future Enhancements

- User-submitted examples (with moderation)
- Example versioning and changelogs
- More advanced integrations (e.g., Alpine.js, Django Channels, SSE, etc.)
- Internationalization (i18n) support

---

### 9. References

- [htmx.org](https://htmx.org/)
- [Django](https://www.djangoproject.com/)
- [Bulma](https://bulma.io/)