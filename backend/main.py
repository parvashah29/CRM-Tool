import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models  # noqa: F401  (registers tables on Base.metadata)
import schemas
from database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="CRM Tool API",
    description="Backend API for CRM Tool managing Contacts, Deals, and Tasks.",
    version="1.1.0",
    lifespan=lifespan,
)

# --- CORS --- (override with CORS_ORIGINS="https://app.example.com,https://other.example.com")
origins = [
    o.strip()
    for o in os.environ.get(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    ).split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _bad_relation(exc: Exception) -> HTTPException:
    code = status.HTTP_409_CONFLICT if isinstance(exc, crud.DuplicateError) else 422
    return HTTPException(status_code=code, detail=str(exc))


def _or_404(obj, label):
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{label} not found")
    return obj


# --- Health & stats ---
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Service is running"}


@app.get("/stats", response_model=schemas.Stats, tags=["Dashboard"])
def stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)


# --- Contacts ---
@app.get("/contacts/", response_model=List[schemas.Contact], tags=["Contacts"])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)


@app.post("/contacts/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED, tags=["Contacts"])
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_contact(db, contact)
    except (crud.DuplicateError, crud.RelationError) as exc:
        raise _bad_relation(exc)


@app.get("/contacts/{contact_id}", response_model=schemas.Contact, tags=["Contacts"])
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    return _or_404(crud.get_contact(db, contact_id), "Contact")


@app.put("/contacts/{contact_id}", response_model=schemas.Contact, tags=["Contacts"])
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    try:
        return _or_404(crud.update_contact(db, contact_id, contact), "Contact")
    except (crud.DuplicateError, crud.RelationError) as exc:
        raise _bad_relation(exc)


@app.delete("/contacts/{contact_id}", response_model=schemas.Contact, tags=["Contacts"])
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return _or_404(crud.delete_contact(db, contact_id), "Contact")


# --- Deals ---
@app.get("/deals/", response_model=List[schemas.Deal], tags=["Deals"])
def read_deals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_deals(db, skip=skip, limit=limit)


@app.post("/deals/", response_model=schemas.Deal, status_code=status.HTTP_201_CREATED, tags=["Deals"])
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_deal(db, deal)
    except crud.RelationError as exc:
        raise _bad_relation(exc)


@app.get("/deals/{deal_id}", response_model=schemas.Deal, tags=["Deals"])
def read_deal(deal_id: int, db: Session = Depends(get_db)):
    return _or_404(crud.get_deal(db, deal_id), "Deal")


@app.put("/deals/{deal_id}", response_model=schemas.Deal, tags=["Deals"])
def update_deal(deal_id: int, deal: schemas.DealUpdate, db: Session = Depends(get_db)):
    try:
        return _or_404(crud.update_deal(db, deal_id, deal), "Deal")
    except crud.RelationError as exc:
        raise _bad_relation(exc)


@app.delete("/deals/{deal_id}", response_model=schemas.Deal, tags=["Deals"])
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    return _or_404(crud.delete_deal(db, deal_id), "Deal")


# --- Tasks ---
@app.get("/tasks/", response_model=List[schemas.Task], tags=["Tasks"])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)


@app.post("/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_task(db, task)
    except crud.RelationError as exc:
        raise _bad_relation(exc)


@app.get("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def read_task(task_id: int, db: Session = Depends(get_db)):
    return _or_404(crud.get_task(db, task_id), "Task")


@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    try:
        return _or_404(crud.update_task(db, task_id, task), "Task")
    except crud.RelationError as exc:
        raise _bad_relation(exc)


@app.delete("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return _or_404(crud.delete_task(db, task_id), "Task")
