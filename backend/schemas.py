from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum

# --- Enums ---
class DealStage(str, Enum):
    LEAD = "Lead"
    CONTACTED = "Contacted"
    NEGOTIATION = "Negotiation"
    CLOSED_WON = "Closed Won"
    CLOSED_LOST = "Closed Lost"

class TaskStatus(str, Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

# --- Contacts ---
class ContactBase(BaseModel):
    name: str = Field(..., min_length=1, example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")
    company: Optional[str] = Field(None, example="Acme Corp")
    position: Optional[str] = Field(None, example="CEO")

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None

class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True

# --- Deals ---
class DealBase(BaseModel):
    title: str = Field(..., min_length=1, example="Big Sale")
    value: float = Field(..., gt=0, example=10000.0)
    stage: DealStage = Field(default=DealStage.LEAD)
    contact_id: Optional[int] = Field(None, description="Linked contact ID")

class DealCreate(DealBase):
    pass

class DealUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[float] = None
    stage: Optional[DealStage] = None
    contact_id: Optional[int] = None

class Deal(DealBase):
    id: int

    class Config:
        from_attributes = True

# --- Tasks ---
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, example="Follow up call")
    description: Optional[str] = Field(None, example="Discuss contract details")
    status: TaskStatus = Field(default=TaskStatus.TODO)
    due_date: Optional[str] = Field(None, description="ISO sequence date string")
    related_deal_id: Optional[int] = None
    related_contact_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[str] = None
    related_deal_id: Optional[int] = None
    related_contact_id: Optional[int] = None

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
