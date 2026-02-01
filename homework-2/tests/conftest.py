"""
pytest fixtures for Customer Support Ticket System tests
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.models import (
    Ticket,
    TicketCreate,
    TicketCategory,
    TicketPriority,
    TicketStatus,
    TicketSource,
)


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def sample_ticket_data():
    """Sample ticket data for testing"""
    return {
        "title": "Cannot access my account after password reset",
        "description": "I tried to reset my password but now I cannot log in at all. The error message says my account is locked. This is critical for my work.",
        "customer_email": "customer@example.com",
        "category": "account_access",
        "priority": "high",
        "source": "web_form",
    }


@pytest.fixture
def sample_ticket_create(sample_ticket_data):
    """Sample TicketCreate instance"""
    return TicketCreate(**sample_ticket_data)


@pytest.fixture
def sample_tickets():
    """Multiple sample tickets for bulk testing"""
    return [
        {
            "title": "Login issues after update",
            "description": "Ever since the last update, I cannot log into my account. I've tried clearing cookies and cache but nothing works.",
            "customer_email": "user1@example.com",
            "category": "account_access",
            "priority": "urgent",
            "source": "email",
        },
        {
            "title": "Request for dark mode feature",
            "description": "It would be really nice if you could add a dark mode option to the application. Many users have been requesting this feature.",
            "customer_email": "user2@example.com",
            "category": "feature_request",
            "priority": "low",
            "source": "web_form",
        },
        {
            "title": "Billing discrepancy on invoice",
            "description": "I noticed that my latest invoice shows charges that don't match what I expected. Please review my account and clarify the charges.",
            "customer_email": "user3@example.com",
            "category": "billing_question",
            "priority": "medium",
            "source": "chat",
        },
    ]


@pytest.fixture
def invalid_ticket_data():
    """Invalid ticket data for negative testing"""
    return {
        "title": "Short",  # Too short (< 10 chars)
        "description": "Too short description",  # Too short (< 50 chars)
        "customer_email": "invalid-email",  # Invalid email format
        "category": "unknown_category",  # Invalid category
        "priority": "super_high",  # Invalid priority
        "source": "carrier_pigeon",  # Invalid source
    }


@pytest.fixture
def csv_content():
    """Sample CSV content for import testing"""
    return """id,title,description,customer_email,category,priority,status,source,created_at,updated_at
1,Cannot access my account,I've been locked out of my account after multiple failed login attempts. This is critical.,user1@example.com,account_access,urgent,new,email,2024-01-15T10:30:00,2024-01-15T10:30:00
2,Request for PDF export,Would be great if you could add ability to export reports to PDF format. This would help with documentation.,user2@example.com,feature_request,low,new,web_form,2024-01-15T11:00:00,2024-01-15T11:00:00
3,Unexpected charge on account,I noticed an unexpected charge of $50 on my latest statement. Please investigate and provide details.,user3@example.com,billing_question,medium,new,chat,2024-01-15T11:30:00,2024-01-15T11:30:00"""


@pytest.fixture
def json_content():
    """Sample JSON content for import testing"""
    return """[
  {
    "title": "Application crashes on startup",
    "description": "The application crashes immediately when I try to open it. This started happening after the latest update.",
    "customer_email": "user4@example.com",
    "category": "technical_issue",
    "priority": "high",
    "source": "api"
  },
  {
    "title": "Need invoice for tax purposes",
    "description": "Please send me an official invoice for my recent purchases. I need this for my quarterly tax filing deadline.",
    "customer_email": "user5@example.com",
    "category": "billing_question",
    "priority": "medium",
    "source": "email"
  }
]"""


@pytest.fixture
def xml_content():
    """Sample XML content for import testing"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<tickets>
  <ticket>
    <title>Button not responding on form</title>
    <description>The submit button on the contact form doesn't work when clicked. I've tried multiple browsers with the same result.</description>
    <customer_email>user6@example.com</customer_email>
    <category>bug_report</category>
    <priority>high</priority>
    <source>web_form</source>
  </ticket>
  <ticket>
    <title>General inquiry about services</title>
    <description>I have some questions about your enterprise services and would like to learn more about pricing and features available.</description>
    <customer_email>user7@example.com</customer_email>
    <category>other</category>
    <priority>low</priority>
    <source>phone</source>
  </ticket>
</tickets>"""
