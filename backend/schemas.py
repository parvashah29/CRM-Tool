from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class DealStage(str, Enum):
    NEW = "New"
    NEGOTIATION = "Negotiation"
    WON = "Won"
    LOST = "Lost"


def _blank_to_none(v):
    """HTML forms send '' for empty optional fields; treat that as 'not provided'."""
    return None if isinstance(v, str) and v.strip() == "" else v


class _BlankToNone(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def _clean(cls, v):
        return _blank_to_none(v)


# --- Contacts ---
class ContactBase(_BlankToNone):
    first_name: str = Field(..., min_length=1, max_length=100, examples=["John"])
    last_name: str = Field("", max_length=100, examples=["Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    phone: Optional[str] = Field(None, examples=["+1234567890"])
    company: Optional[str] = Field(None, examples=["Acme Corp"])
    position: Optional[str] = Field(None, examples=["CEO"])

    @field_validator("last_name", mode="before")
    @classmethod
    def _last_name_default(cls, v):
        return "" if v is None else v


class ContactCreate(ContactBase):
    pass


class ContactUpdate(_BlankToNone):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None


class Contact(ContactBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- Deals ---
class DealBase(_BlankToNone):
    title: str = Field(..., min_length=1, max_length=200, examples=["Big Sale"])
    value: float = Field(..., gt=0, examples=[10000.0])
    stage: DealStage = DealStage.NEW
    contact_id: Optional[int] = Field(None, description="Linked contact ID")
    expected_close_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2026-12-31"])


class DealCreate(DealBase):
    pass


class DealUpdate(_BlankToNone):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    value: Optional[float] = Field(None, gt=0)
    stage: Optional[DealStage] = None
    contact_id: Optional[int] = None
    expected_close_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")


class Deal(DealBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- Tasks ---
class TaskBase(_BlankToNone):
    title: str = Field(..., min_length=1, max_length=200, examples=["Follow up call"])
    description: Optional[str] = None
    due_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2026-12-01"])
    is_completed: bool = False
    related_deal_id: Optional[int] = None
    related_contact_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(_BlankToNone):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    is_completed: Optional[bool] = None
    related_deal_id: Optional[int] = None
    related_contact_id: Optional[int] = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- Dashboard ---
class Stats(BaseModel):
    contacts: int
    deals: int
    open_pipeline_value: float
    won_value: float
    tasks_open: int
    tasks_done: int
    deals_by_stage: dict[str, int]
