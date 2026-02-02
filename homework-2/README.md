# Customer Support Ticket System

A RESTful API for managing customer support tickets with multi-format bulk import capabilities and automatic ticket classification based on content analysis.

**Status:** ✅ Core Implementation Complete
**Tests:** All passing (smoke + integration + performance)
**Documentation:** [API Reference](docs/API_REFERENCE.md) | [Architecture](docs/ARCHITECTURE.md) | [Testing Guide](docs/TESTING_GUIDE.md)

## Features

- ✅ **Full CRUD Operations** - Create, read, update, and delete support tickets with UUID-based identifiers
- ✅ **Multi-Format Import** - Bulk import tickets from CSV, JSON, or XML files with partial failure handling
- ✅ **Auto-Classification** - Automatic categorization and priority assignment using keyword analysis with confidence scoring
- ✅ **Advanced Filtering** - Filter tickets by category, priority, and status with multi-criteria support
- ✅ **Statistics Dashboard** - View ticket distribution across categories, priorities, and statuses
- ✅ **In-Memory Storage** - Fast, lightweight storage with no database setup required
- ✅ **OpenAPI Documentation** - Auto-generated interactive API docs at `/docs`
- ✅ **Comprehensive Testing** - Integration tests, performance benchmarks, and smoke tests

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn src.main:app --reload

# 3. Open API documentation
# Visit http://localhost:8000/docs
```

The API will be running at `http://localhost:8000`

## Prerequisites

- **Python 3.8+** - Required for FastAPI and Pydantic v2
- **pip** - Python package manager
- **Virtual environment** (recommended)

No database installation required - uses in-memory storage.

## Installation

### 1. Navigate to project directory

```bash
cd homework-2
```

### 2. Create and activate virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

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

### 5. Verify installation

```bash
# Check health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"1.0.0","features":{...}}
```

### 6. Access the API

- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## API Overview

### Ticket Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tickets` | Create a new ticket |
| `GET` | `/tickets` | List all tickets (with optional filters) |
| `GET` | `/tickets/{id}` | Get ticket by UUID |
| `PATCH` | `/tickets/{id}` | Update ticket (partial update) |
| `DELETE` | `/tickets/{id}` | Delete ticket |
| `GET` | `/tickets/stats` | Get ticket statistics |

### Import Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/import/csv` | Bulk import from CSV file |
| `POST` | `/import/json` | Bulk import from JSON file |
| `POST` | `/import/xml` | Bulk import from XML file |

### Classification Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tickets/{id}/classify` | Classify single ticket |
| `POST` | `/tickets/classify-all` | Classify all unclassified tickets |

For detailed API documentation with request/response schemas and examples, see **[API_REFERENCE.md](docs/API_REFERENCE.md)**

## Usage Examples

### Create a Ticket

```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-0001",
    "customer_email": "user@example.com",
    "customer_name": "John Doe",
    "subject": "Cannot access my account",
    "description": "I have been unable to log in since this morning. The system shows an error message.",
    "category": "account_access",
    "priority": "high",
    "tags": ["urgent", "login"],
    "metadata": {
      "source": "email",
      "browser": "Chrome",
      "device_type": "desktop"
    }
  }'
```

### List Tickets with Filters

```bash
# All tickets
curl http://localhost:8000/tickets

# Filter by category
curl http://localhost:8000/tickets?category=account_access

# Filter by multiple criteria
curl "http://localhost:8000/tickets?priority=urgent&status=new"
```

### Import from CSV

```bash
curl -X POST http://localhost:8000/import/csv \
  -F "file=@fixtures/sample_tickets.csv"
```

**CSV Format Example:**
```csv
customer_id,customer_email,customer_name,subject,description,category,priority,tags,source,browser,device_type
CUST-0001,user@example.com,John Doe,Login issue,Cannot access dashboard,account_access,high,login;urgent,email,,
```

### Import from JSON

```bash
curl -X POST http://localhost:8000/import/json \
  -F "file=@fixtures/sample_tickets.json"
```

**JSON Format Example:**
```json
[
  {
    "customer_id": "CUST-0001",
    "customer_email": "user@example.com",
    "customer_name": "John Doe",
    "subject": "Login issue",
    "description": "Cannot access dashboard after password reset",
    "category": "account_access",
    "priority": "high",
    "tags": ["bug", "login"],
    "metadata": {
      "source": "web_form",
      "browser": "Chrome",
      "device_type": "desktop"
    }
  }
]
```

### Auto-Classification

```bash
# Classify a single ticket
curl -X POST http://localhost:8000/tickets/{ticket_id}/classify

# Classify all tickets
curl -X POST http://localhost:8000/tickets/classify-all
```

**Classification Response Example:**
```json
{
  "suggested_category": "billing_question",
  "suggested_priority": "medium",
  "confidence": 0.85,
  "reasoning": "Keywords: invoice, charge, refund",
  "keywords_found": ["invoice", "charge", "refund"]
}
```

## Data Models

### Ticket Categories
- `account_access` - Login, password, authentication, 2FA issues
- `technical_issue` - Errors, crashes, performance problems, timeouts
- `billing_question` - Invoices, payments, charges, refunds, subscriptions
- `feature_request` - Feature suggestions, enhancements
- `bug_report` - Defects, unexpected behavior (with reproduction steps)
- `other` - Miscellaneous tickets

### Priority Levels
- `urgent` - Critical issues requiring immediate attention (security, data loss, production down)
- `high` - Important blocking issues
- `medium` - Standard priority (default)
- `low` - Minor issues, cosmetic changes

### Status Values
- `new` - Newly created (default)
- `in_progress` - Being worked on
- `waiting_customer` - Awaiting customer response
- `resolved` - Issue resolved (sets resolved_at timestamp)
- `closed` - Ticket closed

## Project Structure

```
homework-2/
├── src/
│   ├── __init__.py
│   ├── main.py                         # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── ticket.py                   # Pydantic models and enums
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tickets.py                  # CRUD endpoints
│   │   ├── import_routes.py            # Bulk import endpoints
│   │   └── classification_routes.py    # Classification endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ticket_service.py           # Business logic and storage
│   │   ├── import_service.py           # CSV/JSON/XML parsing
│   │   └── classification_service.py   # Auto-categorization logic
│   └── validators/
│       ├── __init__.py
│       └── ticket_validator.py         # Custom validation functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # pytest fixtures
│   ├── test_smoke.py                   # Basic smoke tests (14 tests)
│   ├── test_integration.py             # End-to-end workflow tests (15+ tests)
│   └── test_performance.py             # Performance benchmarks (15+ tests)
├── fixtures/
│   ├── generate_sample_data.py         # Data generation script
│   ├── sample_tickets.csv              # Sample CSV data (50 tickets)
│   ├── sample_tickets.json             # Sample JSON data (20 tickets)
│   └── sample_tickets.xml              # Sample XML data (30 tickets)
├── docs/
│   ├── API_REFERENCE.md                # Detailed API documentation
│   ├── TESTING_GUIDE.md                # Testing documentation
│   └── ARCHITECTURE.md                 # System architecture
├── demo/
│   ├── run.bat                         # Windows run script
│   ├── run.sh                          # Linux/Mac run script
│   └── sample-requests.http            # HTTP request samples
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── HOWTORUN.md                         # Detailed setup instructions
└── AI-PLAN.md                          # Implementation plan
```

## Testing

### Run All Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test suites
pytest tests/test_smoke.py -v              # Smoke tests
pytest tests/test_integration.py -v        # Integration tests
pytest tests/test_performance.py -v        # Performance tests
```

### Test Coverage

The project includes comprehensive test coverage across multiple test categories:

- **Smoke Tests** (14 tests) - Basic functionality verification
- **Integration Tests** (15+ tests) - End-to-end workflows including:
  - Complete CRUD lifecycle
  - Bulk import and filtering
  - Classification integration
  - Edge cases and error scenarios
- **Performance Tests** (15+ tests) - Benchmark validation for:
  - Single operation performance (<50ms)
  - Bulk operations (<2s for 100 tickets)
  - Concurrent operations
  - Memory efficiency

**Target coverage: 85%+**

For detailed testing documentation, see **[TESTING_GUIDE.md](docs/TESTING_GUIDE.md)**

## Sample Data

Generate realistic test data:

```bash
cd fixtures
python generate_sample_data.py
```

This creates:
- `sample_tickets.csv` (50 tickets across all categories)
- `sample_tickets.json` (20 tickets with nested metadata)
- `sample_tickets.xml` (30 tickets in XML format)
- `invalid_tickets.*` (error cases for negative testing)

## Auto-Classification

The system uses keyword-based classification to automatically categorize tickets:

### How It Works

1. **Keyword Analysis** - Scans ticket subject and description for predefined keywords
2. **Category Matching** - Maps keywords to categories (account_access, billing_question, etc.)
3. **Priority Detection** - Identifies urgency keywords (critical, urgent, asap, etc.)
4. **Confidence Scoring** - Returns confidence score (0.0-1.0) based on keyword matches
5. **Disambiguation** - Handles tickets matching multiple categories using specificity rules

### Classification Keywords

**Categories:**
- `account_access`: login, password, access denied, locked out, authentication, 2fa
- `billing_question`: invoice, payment, charge, refund, subscription, price
- `technical_issue`: error, crash, not working, broken, failed, timeout, slow
- `feature_request`: feature, suggestion, improve, enhancement, would be nice
- `bug_report`: bug, defect, reproduce, steps to reproduce, regression

**Priorities:**
- `urgent`: can't access, critical, production down, security, emergency, data loss
- `high`: important, blocking, asap
- `low`: minor, cosmetic, suggestion, nice to have

### Confidence Scoring

- High confidence (0.8-1.0): Multiple keyword matches in category
- Medium confidence (0.5-0.8): Some keyword matches
- Low confidence (0.0-0.5): Weak matches or ambiguous content
- Ambiguity penalty: Reduces confidence when multiple categories match

## Troubleshooting

### Port Already in Use

```bash
# Error: Address already in use
# Solution: Use a different port
uvicorn src.main:app --port 8001
```

### Module Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'src'
# Solution: Ensure you're running from the homework-2 directory
cd homework-2
python -m uvicorn src.main:app --reload
```

### File Upload Issues

```bash
# Error: 422 Unprocessable Entity on CSV import
# Solution: Ensure CSV has proper headers and UTF-8 encoding
# Required headers: customer_id,customer_email,customer_name,subject,description,category,priority,tags,source,browser,device_type
```

### Test Failures

```bash
# Clear test cache and re-run
pytest --cache-clear tests/ -v

# Run specific test
pytest tests/test_smoke.py::test_health_check -v
```

### Virtual Environment Issues

```bash
# If pip install fails, upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

## Documentation

- **[API Reference](docs/API_REFERENCE.md)** - Complete endpoint documentation with request/response examples
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Test pyramid, benchmarks, manual testing checklist
- **[Architecture](docs/ARCHITECTURE.md)** - System design, component details, design decisions
- **[AI Plan](AI-PLAN.md)** - Implementation plan and template mapping
- **[How to Run](HOWTORUN.md)** - Detailed setup and deployment instructions

## Key Technologies

- **FastAPI** - Modern async web framework with automatic API docs
- **Pydantic** - Data validation using Python type hints
- **UUID** - Unique ticket identifiers (not sequential integers)
- **Pytest** - Testing framework with fixtures and parametrization
- **Uvicorn** - Lightning-fast ASGI server

## Implementation Highlights

### UUID-Based IDs
All tickets use UUID v4 for unique identification, not sequential integers. This prevents ID guessing and supports distributed systems.

### Keyword-Based Classification
Deterministic auto-categorization using keyword matching with:
- Weighted keyword scoring
- Category disambiguation rules
- Confidence scoring (0.0-1.0)
- Transparent reasoning

### Multi-Format Import
Supports three file formats with resilient error handling:
- **CSV:** Flat structure with header row
- **JSON:** Nested objects with metadata
- **XML:** Hierarchical structure

Continues processing on individual row failures and provides detailed error reports with row numbers.

### Layered Architecture
Clean separation of concerns:
- **Routes** → Handle HTTP requests/responses
- **Services** → Business logic and data operations
- **Models** → Data validation and structure
- **Validators** → Custom validation rules

### In-Memory Storage
Uses `Dict[UUID, Ticket]` for simplicity. Easily replaceable with database backend through service abstraction layer.

## License

This project is part of AI Coding Partner Homework assignments - MIT License.
