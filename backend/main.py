from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from database import MockDB, get_db
import schemas
import crud

app = FastAPI(
    title="CRM Tool API",
    description="Backend API for CRM Tool managing Contacts, Deals, and Tasks.",
    version="1.0.0"
)

# --- CORS ---
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check ---
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Service is running"}

# --- Contacts Endpoints ---
@app.get("/contacts/", response_model=List[schemas.Contact], tags=["Contacts"])
def read_contacts(skip: int = 0, limit: int = 100, db: MockDB = Depends(get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.post("/contacts/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED, tags=["Contacts"])
def create_contact(contact: schemas.ContactCreate, db: MockDB = Depends(get_db)):
    return crud.create_contact(db, contact)

@app.get("/contacts/{contact_id}", response_model=schemas.Contact, tags=["Contacts"])
def read_contact(contact_id: int, db: MockDB = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact, tags=["Contacts"])
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: MockDB = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact, tags=["Contacts"])
def delete_contact(contact_id: int, db: MockDB = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# --- Deals Endpoints ---
@app.get("/deals/", response_model=List[schemas.Deal], tags=["Deals"])
def read_deals(skip: int = 0, limit: int = 100, db: MockDB = Depends(get_db)):
    return crud.get_deals(db, skip=skip, limit=limit)

@app.post("/deals/", response_model=schemas.Deal, status_code=status.HTTP_201_CREATED, tags=["Deals"])
def create_deal(deal: schemas.DealCreate, db: MockDB = Depends(get_db)):
    return crud.create_deal(db, deal)

@app.get("/deals/{deal_id}", response_model=schemas.Deal, tags=["Deals"])
def read_deal(deal_id: int, db: MockDB = Depends(get_db)):
    db_deal = crud.get_deal(db, deal_id)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal

@app.put("/deals/{deal_id}", response_model=schemas.Deal, tags=["Deals"])
def update_deal(deal_id: int, deal: schemas.DealUpdate, db: MockDB = Depends(get_db)):
    db_deal = crud.update_deal(db, deal_id, deal)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal

@app.delete("/deals/{deal_id}", response_model=schemas.Deal, tags=["Deals"])
def delete_deal(deal_id: int, db: MockDB = Depends(get_db)):
    db_deal = crud.delete_deal(db, deal_id)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal

# --- Tasks Endpoints ---
@app.get("/tasks/", response_model=List[schemas.Task], tags=["Tasks"])
def read_tasks(skip: int = 0, limit: int = 100, db: MockDB = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)

@app.post("/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: MockDB = Depends(get_db)):
    return crud.create_task(db, task)

@app.get("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def read_task(task_id: int, db: MockDB = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def update_task(task_id: int, task: schemas.TaskUpdate, db: MockDB = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def delete_task(task_id: int, db: MockDB = Depends(get_db)):
    db_task = crud.delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
