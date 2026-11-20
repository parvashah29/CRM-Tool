from schemas import ContactCreate, ContactUpdate, DealCreate, DealUpdate, TaskCreate, TaskUpdate
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
