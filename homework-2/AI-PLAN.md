# AI Implementation Plan - Customer Support Ticket System

**Project:** Customer Support Ticket System  
**Generated:** Using TEMPLATE_CLAUDE_PLANNER  
**Homework:** homework-2  

---

## Project Overview

A REST API for managing customer support tickets with:
- Multi-format bulk import (CSV, JSON, XML)
- Auto-categorization based on content analysis
- Full CRUD operations
- In-memory storage

---

## Phase 1: Project Setup & Models

### 1.1 Project Structure
```
homework-2/
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── ticket.py              # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tickets.py             # CRUD endpoints
│   │   └── import_routes.py       # Bulk import endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ticket_service.py      # Business logic
│   │   ├── import_service.py      # File parsing
│   │   └── classification_service.py  # Auto-categorization
│   ├── validators/
│   │   ├── __init__.py
│   │   └── ticket_validator.py    # Custom validators
│   └── utils/
│       ├── __init__.py
│       └── helpers.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest fixtures
│   ├── test_ticket_api.py         # API endpoint tests (11)
│   ├── test_ticket_model.py       # Model validation tests (9)
│   ├── test_import_csv.py         # CSV import tests (6)
│   ├── test_import_json.py        # JSON import tests (5)
│   ├── test_import_xml.py         # XML import tests (5)
│   ├── test_categorization.py     # Classification tests (10)
│   ├── test_integration.py        # End-to-end tests (5)
│   └── test_performance.py        # Benchmark tests (5)
├── fixtures/
│   ├── sample_tickets.csv         # 50 test tickets
│   ├── sample_tickets.json        # 20 test tickets
│   ├── sample_tickets.xml         # 30 test tickets
│   └── invalid_tickets.csv        # Invalid data for testing
├── demo/
│   ├── run.bat
│   ├── run.sh
│   └── sample-requests.http
├── docs/
│   ├── API_REFERENCE.md
│   ├── TESTING_GUIDE.md
│   └── ARCHITECTURE.md
├── requirements.txt
├── README.md
├── HOWTORUN.md
└── AI-PLAN.md                     # This file
```

### 1.2 Dependencies (requirements.txt)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
httpx>=0.25.0
```

### 1.3 Pydantic Models
**Template:** `TEMPLATE_CLAUDE_CODER_MODELS.md`

#### Enums
- `TicketCategory`: account_access, technical_issue, billing_question, feature_request, bug_report, other
- `TicketPriority`: urgent, high, medium, low
- `TicketStatus`: new, in_progress, waiting_customer, resolved, closed
- `TicketSource`: web_form, email, api, chat, phone

#### Models
- `TicketBase`: Common fields (title, description, customer_email, category, priority, source)
- `TicketCreate`: For POST requests (extends TicketBase)
- `TicketUpdate`: For PATCH requests (all fields optional)
- `Ticket`: Full model with id, status, timestamps
- `TicketList`: Response wrapper with items and count
- `ClassificationResult`: category, confidence, suggested_priority
- `ImportResult`: success_count, error_count, errors list

---

## Phase 2: Core Services

### 2.1 Ticket Service
**Template:** `TEMPLATE_CLAUDE_CODER_SERVICES.md` or `TEMPLATE_COPILOT_CODER_SERVICES.md`

**Storage:** In-memory Dict[int, Ticket]

**Methods:**
| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `create_ticket` | TicketCreate | Ticket | Create with auto-ID |
| `get_ticket` | int | Ticket \| None | Get by ID |
| `get_all_tickets` | filters | List[Ticket] | Filter by category/priority/status |
| `update_ticket` | int, TicketUpdate | Ticket \| None | Partial update |
| `delete_ticket` | int | bool | Delete by ID |
| `get_statistics` | None | Dict | Count by category/priority/status |

### 2.2 Import Service
**Template:** `TEMPLATE_GPT4_TESTER_IMPORT.md` (for understanding requirements)

**Methods:**
| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `import_csv` | UploadFile | ImportResult | Parse CSV, validate, create tickets |
| `import_json` | UploadFile | ImportResult | Parse JSON array, validate, create |
| `import_xml` | UploadFile | ImportResult | Parse XML, validate, create |
| `_parse_csv_row` | Dict | TicketCreate | Convert CSV row to model |
| `_validate_row` | Dict | List[str] | Return validation errors |

### 2.3 Classification Service
**Template:** `TEMPLATE_CLAUDE_CODER_CLASSIFICATION.md`

**Keyword Maps:**
```python
CATEGORY_KEYWORDS = {
    "account_access": ["login", "password", "access", "locked", "sign in", "authentication"],
    "technical_issue": ["error", "crash", "not working", "bug", "broken", "failed"],
    "billing_question": ["invoice", "payment", "charge", "refund", "subscription", "price"],
    "feature_request": ["feature", "add", "suggestion", "would be nice", "improve", "enhancement"],
    "bug_report": ["bug", "issue", "defect", "problem", "unexpected", "incorrect"]
}

PRIORITY_KEYWORDS = {
    "urgent": ["can't access", "critical", "production down", "security", "emergency"],
    "high": ["important", "blocking", "asap", "urgent need"],
    "low": ["minor", "cosmetic", "suggestion", "nice to have"]
}
```

**Methods:**
| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `classify_ticket` | Ticket | ClassificationResult | Analyze and suggest category |
| `_calculate_confidence` | matches | float | Score 0.0-1.0 |
| `_suggest_priority` | str | TicketPriority | Based on keywords |
| `auto_classify_all` | None | List[Ticket] | Classify all unclassified |

---

## Phase 3: API Routes

### 3.1 Ticket CRUD Routes
**Template:** `TEMPLATE_COPILOT_CODER_ROUTES.md`

| Endpoint | Method | Request | Response | Description |
|----------|--------|---------|----------|-------------|
| `/tickets` | POST | TicketCreate | Ticket | Create ticket |
| `/tickets` | GET | ?category&priority&status | TicketList | List with filters |
| `/tickets/{id}` | GET | - | Ticket | Get by ID |
| `/tickets/{id}` | PATCH | TicketUpdate | Ticket | Update ticket |
| `/tickets/{id}` | DELETE | - | 204 | Delete ticket |
| `/tickets/stats` | GET | - | Dict | Statistics |

### 3.2 Import Routes
| Endpoint | Method | Request | Response | Description |
|----------|--------|---------|----------|-------------|
| `/import/csv` | POST | File upload | ImportResult | Bulk import CSV |
| `/import/json` | POST | File upload | ImportResult | Bulk import JSON |
| `/import/xml` | POST | File upload | ImportResult | Bulk import XML |

### 3.3 Classification Routes
| Endpoint | Method | Request | Response | Description |
|----------|--------|---------|----------|-------------|
| `/tickets/{id}/classify` | POST | - | ClassificationResult | Classify single |
| `/tickets/classify-all` | POST | - | List[Ticket] | Classify all |

---

## Phase 4: Validators

**Template:** `TEMPLATE_GPT4_CODER_VALIDATORS.md`

### Custom Validators
| Validator | Field | Rule |
|-----------|-------|------|
| `validate_email` | customer_email | Valid email format |
| `validate_title` | title | 10-100 characters |
| `validate_description` | description | 50-500 characters |
| `validate_category` | category | Must be valid enum |
| `validate_priority` | priority | Must be valid enum |

---

## Phase 5: Testing

**Template:** `TEMPLATE_GPT4_TESTER_UNIT.md`, `TEMPLATE_CLAUDE_TESTER_INTEGRATION.md`

### Test Files Summary
| File | Tests | Coverage Target |
|------|-------|-----------------|
| test_ticket_api.py | 11 | All CRUD endpoints |
| test_ticket_model.py | 9 | Model validation |
| test_import_csv.py | 6 | CSV parsing |
| test_import_json.py | 5 | JSON parsing |
| test_import_xml.py | 5 | XML parsing |
| test_categorization.py | 10 | Classification logic |
| test_integration.py | 5 | End-to-end workflows |
| test_performance.py | 5 | Benchmarks |
| **TOTAL** | **56** | **85%+** |

### Key Test Scenarios
1. **CRUD**: Create, read, update, delete, list with filters
2. **Validation**: Invalid email, too short title, missing required fields
3. **Import**: Valid files, malformed files, partial failures
4. **Classification**: All category keywords, confidence thresholds
5. **Performance**: <50ms single operations, <2s bulk import

---

## Phase 6: Documentation

### 6.1 README.md
**Template:** `TEMPLATE_CLAUDE_DOCUMENTER_README.md`
- Project overview
- Quick start
- API summary
- Examples

### 6.2 API_REFERENCE.md
**Template:** `TEMPLATE_GPT4_DOCUMENTER_API_REFERENCE.md`
- All endpoints with examples
- Request/response schemas
- Error codes

### 6.3 TESTING_GUIDE.md
**Template:** `TEMPLATE_GPT4_DOCUMENTER_TESTING_GUIDE.md`
- Test pyramid
- How to run tests
- Coverage report
- Manual checklist

### 6.4 ARCHITECTURE.md
**Template:** `TEMPLATE_CLAUDE_DOCUMENTER_ARCHITECTURE.md`
- System diagrams (Mermaid)
- Component descriptions
- Data flow

---

## Implementation Order

### Week 1: Foundation
1. ✅ Create project structure
2. ⬜ Implement Pydantic models (use TEMPLATE_CLAUDE_CODER_MODELS)
3. ⬜ Implement basic validators (use TEMPLATE_GPT4_CODER_VALIDATORS)
4. ⬜ Write model tests

### Week 2: Core Logic
5. ⬜ Implement ticket_service.py (use TEMPLATE_COPILOT_CODER_SERVICES)
6. ⬜ Implement import_service.py 
7. ⬜ Implement classification_service.py (use TEMPLATE_CLAUDE_CODER_CLASSIFICATION)
8. ⬜ Write service tests

### Week 3: API Layer
9. ⬜ Implement ticket routes (use TEMPLATE_COPILOT_CODER_ROUTES)
10. ⬜ Implement import routes
11. ⬜ Implement classification routes
12. ⬜ Write API tests

### Week 4: Polish
13. ⬜ Generate sample data (use TEMPLATE_DATA_GENERATOR)
14. ⬜ Write integration tests (use TEMPLATE_CLAUDE_TESTER_INTEGRATION)
15. ⬜ Write performance tests
16. ⬜ Generate documentation
17. ⬜ Code review (use TEMPLATE_GPT4_REVIEWER)

---

## Template Usage Map

| Task | Primary Template | Alternative |
|------|-----------------|-------------|
| Models | TEMPLATE_CLAUDE_CODER_MODELS | - |
| Services | TEMPLATE_COPILOT_CODER_SERVICES | TEMPLATE_CLAUDE_CODER_SERVICES |
| Routes | TEMPLATE_COPILOT_CODER_ROUTES | - |
| Validators | TEMPLATE_GPT4_CODER_VALIDATORS | - |
| Classification | TEMPLATE_CLAUDE_CODER_CLASSIFICATION | - |
| Unit Tests | TEMPLATE_GPT4_TESTER_UNIT | TEMPLATE_COPILOT_TESTER_QUICK |
| Import Tests | TEMPLATE_GPT4_TESTER_IMPORT | - |
| Integration Tests | TEMPLATE_CLAUDE_TESTER_INTEGRATION | - |
| README | TEMPLATE_CLAUDE_DOCUMENTER_README | - |
| API Docs | TEMPLATE_GPT4_DOCUMENTER_API_REFERENCE | - |
| Testing Guide | TEMPLATE_GPT4_DOCUMENTER_TESTING_GUIDE | - |
| Architecture | TEMPLATE_CLAUDE_DOCUMENTER_ARCHITECTURE | - |
| Code Review | TEMPLATE_GPT4_REVIEWER | - |
| Sample Data | TEMPLATE_DATA_GENERATOR | - |

---

## Success Criteria

- [ ] All 56 tests passing
- [ ] Code coverage > 85%
- [ ] All import formats working (CSV, JSON, XML)
- [ ] Auto-classification with confidence scoring
- [ ] Complete API documentation
- [ ] Demo scripts working
- [ ] No linting errors
