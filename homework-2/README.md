# Customer Support Ticket System

A REST API for managing customer support tickets with multi-format bulk import and auto-categorization.

**Status:** ✅ Core Implementation Complete  
**Tests:** 14/14 passing (100%)  
**Documentation:** [Implementation Summary](IMPLEMENTATION_SUMMARY.md) | [AI Plan](AI-PLAN.md)

## Features

- ✅ Full CRUD operations for support tickets (UUID-based)
- ✅ Multi-format bulk import (CSV, JSON, XML)
- ✅ Auto-categorization based on keyword analysis
- ✅ Filtering by category, priority, and status
- ✅ Confidence scoring for classifications
- ✅ In-memory storage (no database required)
- ✅ Interactive API documentation (Swagger UI)
- ✅ Sample data fixtures for testing

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
cd homework-2
pip install -r requirements.txt
```

### Run the Server

**Windows:**
```bash
demo\run.bat
```

**Linux/Mac:**
```bash
chmod +x demo/run.sh
./demo/run.sh
```

**Or directly:**
```bash
uvicorn src.main:app --reload
```

### Access the API

- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json

## API Endpoints

### Tickets
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tickets` | Create a new ticket |
| GET | `/tickets` | List tickets (with filters) |
| GET | `/tickets/{id}` | Get ticket by ID |
| PATCH | `/tickets/{id}` | Update ticket |
| DELETE | `/tickets/{id}` | Delete ticket |
| GET | `/tickets/stats` | Get statistics |

### Import
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/import/csv` | Bulk import from CSV |
| POST | `/import/json` | Bulk import from JSON |
| POST | `/import/xml` | Bulk import from XML |

### Classification
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tickets/{id}/classify` | Classify single ticket |
| POST | `/tickets/classify-all` | Auto-classify all tickets |

## Data Models

### Ticket Categories
- `account_access` - Login and authentication issues
- `technical_issue` - Bugs and technical problems
- `billing_question` - Payment and invoice inquiries
- `feature_request` - Feature suggestions
- `bug_report` - Bug reports
- `other` - Miscellaneous

### Priority Levels
- `urgent` - Critical issues requiring immediate attention
- `high` - Important issues
- `medium` - Standard priority (default)
- `low` - Minor issues

### Status Values
- `new` - Newly created (default)
- `in_progress` - Being worked on
- `waiting_customer` - Awaiting customer response
- `resolved` - Issue resolved
- `closed` - Ticket closed

## Running Tests

```bash
# Run all smoke tests
pytest tests/test_smoke.py -v

# Run with coverage
pytest --cov=src --cov-report=html

# All 14 tests should pass
# ✅ test_health_check
# ✅ test_root_endpoint
# ✅ test_create_ticket
# ✅ test_list_tickets_empty
# ✅ test_list_tickets_with_data
# ✅ test_get_ticket
# ✅ test_get_nonexistent_ticket
# ✅ test_update_ticket
# ✅ test_delete_ticket
# ✅ test_filter_by_category
# ✅ test_get_statistics
# ✅ test_classification
# ✅ test_classify_all
# ✅ test_invalid_ticket_data
```

## Sample Data

Generate realistic test data:

```bash
cd fixtures
python generate_sample_data.py
```

This creates:
- `sample_tickets.csv` (50 tickets)
- `sample_tickets.json` (20 tickets)
- `sample_tickets.xml` (30 tickets)
- `invalid_tickets.*` (error cases for testing)

## Project Structure

```
homework-2/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── models/              # Pydantic models
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── validators/          # Custom validators
│   └── utils/               # Utility functions
├── tests/                   # Test suite
├── fixtures/                # Test data files
├── demo/                    # Demo scripts
├── docs/                    # Documentation
├── requirements.txt         # Dependencies
└── AI-PLAN.md              # Implementation plan
```

## Documentation

- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Complete implementation details
- [AI-PLAN.md](AI-PLAN.md) - Implementation plan and template mapping
- [HOWTORUN.md](HOWTORUN.md) - Detailed setup instructions
- [Interactive API Docs](http://localhost:8000/docs) - Available when server is running

## Key Technologies

- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation using Python type hints
- **UUID** - Unique ticket identifiers (not sequential integers)
- **Pytest** - Testing framework with fixtures
- **Uvicorn** - Lightning-fast ASGI server

## Implementation Highlights

### UUID-Based IDs
All tickets use UUID v4 for unique identification, not sequential integers. This avoids ID guessing and supports distributed systems.

### Keyword-Based Classification
The auto-categorization uses keyword matching for:
- **Categories:** account_access, technical_issue, billing_question, feature_request, bug_report, other
- **Priorities:** urgent, high, medium, low
- **Confidence Scoring:** 0.0-1.0 based on keyword matches
- **Disambiguation:** Smart handling when multiple categories match

### Multi-Format Import
Supports three file formats with partial success handling:
- **CSV:** Header row with flat structure
- **JSON:** Array of ticket objects with nested metadata
- **XML:** `<tickets><ticket>...</ticket></tickets>` structure

Continues processing on individual row failures and provides detailed error reports.

### In-Memory Storage
Uses `Dict[UUID, Ticket]` for simplicity. Easily replaceable with database backend through service abstraction layer.

## License

MIT
