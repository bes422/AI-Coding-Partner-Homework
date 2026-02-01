"""
Pydantic models for Customer Support Ticket System

Enums:
- TicketCategory: account_access, technical_issue, billing_question, feature_request, bug_report, other
- TicketPriority: urgent, high, medium, low  
- TicketStatus: new, in_progress, waiting_customer, resolved, closed
- TicketSource: web_form, email, api, chat, phone

Models:
- TicketBase: Common fields
- TicketCreate: For POST requests
- TicketUpdate: For PATCH requests (all optional)
- Ticket: Full model with id and timestamps
- TicketList: Response wrapper
- ClassificationResult: Auto-classification output
- ImportResult: Bulk import result
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class TicketCategory(str, Enum):
    """Categories for support tickets"""
    ACCOUNT_ACCESS = "account_access"
    TECHNICAL_ISSUE = "technical_issue"
    BILLING_QUESTION = "billing_question"
    FEATURE_REQUEST = "feature_request"
    BUG_REPORT = "bug_report"
    OTHER = "other"


class TicketPriority(str, Enum):
    """Priority levels for tickets"""
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TicketStatus(str, Enum):
    """Status values for ticket lifecycle"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketSource(str, Enum):
    """Source channels for tickets"""
    WEB_FORM = "web_form"
    EMAIL = "email"
    API = "api"
    CHAT = "chat"
    PHONE = "phone"


class TicketBase(BaseModel):
    """Base model with common ticket fields"""
    title: str = Field(..., min_length=10, max_length=100, description="Ticket title")
    description: str = Field(..., min_length=50, max_length=500, description="Detailed description")
    customer_email: EmailStr = Field(..., description="Customer email address")
    category: TicketCategory = Field(..., description="Ticket category")
    priority: TicketPriority = Field(default=TicketPriority.MEDIUM, description="Ticket priority")
    source: TicketSource = Field(default=TicketSource.WEB_FORM, description="Source channel")


class TicketCreate(TicketBase):
    """Model for creating a new ticket"""
    pass


class TicketUpdate(BaseModel):
    """Model for updating an existing ticket (all fields optional)"""
    title: Optional[str] = Field(None, min_length=10, max_length=100)
    description: Optional[str] = Field(None, min_length=50, max_length=500)
    customer_email: Optional[EmailStr] = None
    category: Optional[TicketCategory] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    source: Optional[TicketSource] = None


class Ticket(TicketBase):
    """Full ticket model with all fields"""
    id: int = Field(..., description="Unique ticket identifier")
    status: TicketStatus = Field(default=TicketStatus.NEW, description="Current status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    class Config:
        from_attributes = True


class TicketList(BaseModel):
    """Response model for listing tickets"""
    items: List[Ticket] = Field(default_factory=list, description="List of tickets")
    total: int = Field(..., description="Total number of tickets")


class ClassificationResult(BaseModel):
    """Result of auto-classification"""
    ticket_id: int = Field(..., description="ID of classified ticket")
    suggested_category: TicketCategory = Field(..., description="Suggested category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    suggested_priority: Optional[TicketPriority] = Field(None, description="Suggested priority if detected")
    keywords_matched: List[str] = Field(default_factory=list, description="Keywords that matched")


class ImportError(BaseModel):
    """Error details for failed import row"""
    row: int = Field(..., description="Row number (1-indexed)")
    errors: List[str] = Field(default_factory=list, description="List of validation errors")


class ImportResult(BaseModel):
    """Result of bulk import operation"""
    success_count: int = Field(..., description="Number of successfully imported tickets")
    error_count: int = Field(..., description="Number of failed imports")
    errors: List[ImportError] = Field(default_factory=list, description="Details of import errors")
    imported_ids: List[int] = Field(default_factory=list, description="IDs of imported tickets")
