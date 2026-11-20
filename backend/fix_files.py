import os

files = {
    "main.py": """from fastapi import FastAPI, HTTPException, Depends, status
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
""",
    "database.py": """# In-memory 'database' simulation
# In a real app, this would be a SQLAlchemy Session or similar.

class MockDB:
    def __init__(self):
        self.contacts = []
        self.deals = []
        self.tasks = []
        self._contact_id_counter = 1
        self._deal_id_counter = 1
        self._task_id_counter = 1

    def drop_all(self):
        self.contacts = []
        self.deals = []
        self.tasks = []
        self._contact_id_counter = 1
        self._deal_id_counter = 1
        self._task_id_counter = 1

db_instance = MockDB()

def get_db():
    return db_instance
""",
    "crud.py": """from schemas import ContactCreate, ContactUpdate, DealCreate, DealUpdate, TaskCreate, TaskUpdate
from database import MockDB

# --- Contacts ---
def get_contacts(db: MockDB, skip: int = 0, limit: int = 100):
    return db.contacts[skip : skip + limit]

def get_contact(db: MockDB, contact_id: int):
    for contact in db.contacts:
        if contact['id'] == contact_id:
            return contact
    return None

def create_contact(db: MockDB, contact: ContactCreate):
    new_contact = contact.model_dump()
    new_contact['id'] = db._contact_id_counter
    db._contact_id_counter += 1
    db.contacts.append(new_contact)
    return new_contact

def update_contact(db: MockDB, contact_id: int, contact_update: ContactUpdate):
    for i, contact in enumerate(db.contacts):
        if contact['id'] == contact_id:
            update_data = contact_update.model_dump(exclude_unset=True)
            updated_contact = contact.copy()
            updated_contact.update(update_data)
            db.contacts[i] = updated_contact
            return updated_contact
    return None

def delete_contact(db: MockDB, contact_id: int):
    for i, contact in enumerate(db.contacts):
        if contact['id'] == contact_id:
            return db.contacts.pop(i)
    return None

# --- Deals ---
def get_deals(db: MockDB, skip: int = 0, limit: int = 100):
    return db.deals[skip : skip + limit]

def get_deal(db: MockDB, deal_id: int):
    for deal in db.deals:
        if deal['id'] == deal_id:
            return deal
    return None

def create_deal(db: MockDB, deal: DealCreate):
    new_deal = deal.model_dump()
    new_deal['id'] = db._deal_id_counter
    db._deal_id_counter += 1
    db.deals.append(new_deal)
    return new_deal

def update_deal(db: MockDB, deal_id: int, deal_update: DealUpdate):
    for i, deal in enumerate(db.deals):
        if deal['id'] == deal_id:
            update_data = deal_update.model_dump(exclude_unset=True)
            updated_deal = deal.copy()
            updated_deal.update(update_data)
            db.deals[i] = updated_deal
            return updated_deal
    return None

def delete_deal(db: MockDB, deal_id: int):
    for i, deal in enumerate(db.deals):
        if deal['id'] == deal_id:
            return db.deals.pop(i)
    return None

# --- Tasks ---
def get_tasks(db: MockDB, skip: int = 0, limit: int = 100):
    return db.tasks[skip : skip + limit]

def get_task(db: MockDB, task_id: int):
    for task in db.tasks:
        if task['id'] == task_id:
            return task
    return None

def create_task(db: MockDB, task: TaskCreate):
    new_task = task.model_dump()
    new_task['id'] = db._task_id_counter
    db._task_id_counter += 1
    db.tasks.append(new_task)
    return new_task

def update_task(db: MockDB, task_id: int, task_update: TaskUpdate):
    for i, task in enumerate(db.tasks):
        if task['id'] == task_id:
            update_data = task_update.model_dump(exclude_unset=True)
            updated_task = task.copy()
            updated_task.update(update_data)
            db.tasks[i] = updated_task
            return updated_task
    return None

def delete_task(db: MockDB, task_id: int):
    for i, task in enumerate(db.tasks):
        if task['id'] == task_id:
            return db.tasks.pop(i)
    return None
"""
}

for filename, content in files.items():
    print(f"Overwriting {filename}...")
    with open(filename, "w") as f:
        f.write(content)
    print(f"Overwrote {filename}.")

print("All files updated.")
