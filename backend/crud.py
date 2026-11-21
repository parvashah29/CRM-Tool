from sqlalchemy import func, select
from sqlalchemy.orm import Session

import models
import schemas


class RelationError(ValueError):
    """Raised when a foreign key points at a record that does not exist."""


class DuplicateError(ValueError):
    """Raised when a unique field (contact email) is already taken."""


def _require(db: Session, model, pk, label):
    if pk is not None and db.get(model, pk) is None:
        raise RelationError(f"{label} {pk} does not exist")


def _apply(obj, data: dict):
    for key, value in data.items():
        setattr(obj, key, value)


# --- Contacts ---
def get_contacts(db: Session, skip=0, limit=100):
    return db.scalars(select(models.Contact).order_by(models.Contact.id).offset(skip).limit(limit)).all()


def get_contact(db: Session, contact_id: int):
    return db.get(models.Contact, contact_id)


def _email_taken(db: Session, email: str, exclude_id: int | None = None):
    q = select(models.Contact.id).where(func.lower(models.Contact.email) == email.lower())
    found = db.scalar(q)
    return found is not None and found != exclude_id


def create_contact(db: Session, contact: schemas.ContactCreate):
    if _email_taken(db, contact.email):
        raise DuplicateError("A contact with this email already exists")
    obj = models.Contact(**contact.model_dump())
    db.add(obj)
    db.commit()
    return obj


def update_contact(db: Session, contact_id: int, update: schemas.ContactUpdate):
    obj = db.get(models.Contact, contact_id)
    if obj is None:
        return None
    data = update.model_dump(exclude_unset=True)
    if "email" in data and data["email"] and _email_taken(db, data["email"], exclude_id=contact_id):
        raise DuplicateError("A contact with this email already exists")
    _apply(obj, {k: v for k, v in data.items() if v is not None or k not in ("first_name", "email")})
    db.commit()
    return obj


def delete_contact(db: Session, contact_id: int):
    obj = db.get(models.Contact, contact_id)
    if obj is None:
        return None
    # SQLite does not enforce ON DELETE SET NULL unless PRAGMA foreign_keys is on; do it explicitly.
    for deal in db.scalars(select(models.Deal).where(models.Deal.contact_id == contact_id)):
        deal.contact_id = None
    for task in db.scalars(select(models.Task).where(models.Task.related_contact_id == contact_id)):
        task.related_contact_id = None
    db.delete(obj)
    db.commit()
    return obj


# --- Deals ---
def get_deals(db: Session, skip=0, limit=100):
    return db.scalars(select(models.Deal).order_by(models.Deal.id).offset(skip).limit(limit)).all()


def get_deal(db: Session, deal_id: int):
    return db.get(models.Deal, deal_id)


def create_deal(db: Session, deal: schemas.DealCreate):
    _require(db, models.Contact, deal.contact_id, "Contact")
    obj = models.Deal(**{**deal.model_dump(), "stage": deal.stage.value})
    db.add(obj)
    db.commit()
    return obj


def update_deal(db: Session, deal_id: int, update: schemas.DealUpdate):
    obj = db.get(models.Deal, deal_id)
    if obj is None:
        return None
    data = update.model_dump(exclude_unset=True)
    if data.get("contact_id") is not None:
        _require(db, models.Contact, data["contact_id"], "Contact")
    if "stage" in data and data["stage"] is not None:
        data["stage"] = data["stage"].value
    _apply(obj, {k: v for k, v in data.items() if v is not None or k in ("contact_id", "expected_close_date")})
    db.commit()
    return obj


def delete_deal(db: Session, deal_id: int):
    obj = db.get(models.Deal, deal_id)
    if obj is None:
        return None
    for task in db.scalars(select(models.Task).where(models.Task.related_deal_id == deal_id)):
        task.related_deal_id = None
    db.delete(obj)
    db.commit()
    return obj


# --- Tasks ---
def get_tasks(db: Session, skip=0, limit=100):
    return db.scalars(select(models.Task).order_by(models.Task.id).offset(skip).limit(limit)).all()


def get_task(db: Session, task_id: int):
    return db.get(models.Task, task_id)


def create_task(db: Session, task: schemas.TaskCreate):
    _require(db, models.Deal, task.related_deal_id, "Deal")
    _require(db, models.Contact, task.related_contact_id, "Contact")
    obj = models.Task(**task.model_dump())
    db.add(obj)
    db.commit()
    return obj


def update_task(db: Session, task_id: int, update: schemas.TaskUpdate):
    obj = db.get(models.Task, task_id)
    if obj is None:
        return None
    data = update.model_dump(exclude_unset=True)
    _require(db, models.Deal, data.get("related_deal_id"), "Deal")
    _require(db, models.Contact, data.get("related_contact_id"), "Contact")
    _apply(obj, {k: v for k, v in data.items() if v is not None or k in ("description", "due_date", "related_deal_id", "related_contact_id")})
    db.commit()
    return obj


def delete_task(db: Session, task_id: int):
    obj = db.get(models.Task, task_id)
    if obj is None:
        return None
    db.delete(obj)
    db.commit()
    return obj


# --- Dashboard ---
def get_stats(db: Session) -> schemas.Stats:
    by_stage = {s.value: 0 for s in schemas.DealStage}
    for stage, count in db.execute(select(models.Deal.stage, func.count()).group_by(models.Deal.stage)):
        by_stage[stage] = count
    value = lambda *stages: float(  # noqa: E731
        db.scalar(select(func.coalesce(func.sum(models.Deal.value), 0)).where(models.Deal.stage.in_(stages))) or 0
    )
    return schemas.Stats(
        contacts=db.scalar(select(func.count()).select_from(models.Contact)),
        deals=db.scalar(select(func.count()).select_from(models.Deal)),
        open_pipeline_value=value("New", "Negotiation"),
        won_value=value("Won"),
        tasks_open=db.scalar(select(func.count()).select_from(models.Task).where(models.Task.is_completed.is_(False))),
        tasks_done=db.scalar(select(func.count()).select_from(models.Task).where(models.Task.is_completed.is_(True))),
        deals_by_stage=by_stage,
    )
