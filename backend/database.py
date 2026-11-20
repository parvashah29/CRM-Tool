# In-memory 'database' simulation
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
