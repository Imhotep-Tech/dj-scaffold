# 🏗️ Architecture Layouts

When creating a new app inside an existing project (`dj-scaffold startapp` or interactive menu), you are prompted to choose an architecture layout.

### 1. Service Layer Pattern (Recommended)
Standard Django apps often suffer from "Fat Models" (too much logic inside model methods) or "Fat Views" (massive view functions handling business logic). 

The **Service Layer Pattern** strictly separates concerns into a highly scalable, testable structure.

**Folder Structure:**
```text
your_app/
├── apis.py          # HTTP Route Handlers (Extracts inputs, serializes outputs)
├── services.py      # Business Logic & Mutations (Creates, Updates, Deletes)
├── selectors.py     # Database Queries (Reads data)
├── models.py        # Schema and Relationships
└── urls.py          # App routes
```

**How data flows:**
`Request ──> apis.py ──> services.py (Write) or selectors.py (Read) ──> models.py`
This ensures your APIs are lightweight, testing is a breeze, and your business logic is completely isolated from the HTTP framework!

### 2. Standard Django Layout
The standard layout provides the default Django structure (`views.py`, `models.py`, `admin.py`, `tests.py`). Use this option if you are building a very simple app or prefer the traditional Django approach.
