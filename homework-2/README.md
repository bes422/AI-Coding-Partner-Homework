# Customer Support Ticket System

A REST API for managing customer support tickets with multi-format bulk import and auto-categorization.

## Features

- ✅ Full CRUD operations for support tickets
- ✅ Multi-format bulk import (CSV, JSON, XML)
- ✅ Auto-categorization based on content analysis
- ✅ Filtering by category, priority, and status
- ✅ In-memory storage (no database required)

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
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_ticket_api.py
```

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

- [AI-PLAN.md](AI-PLAN.md) - Implementation plan and template mapping
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - Detailed API documentation
- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) - Testing guide
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture

## License

MIT
