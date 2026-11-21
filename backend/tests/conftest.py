import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DATABASE_URL"] = "sqlite://"  # in-memory database for tests

import pytest
from fastapi.testclient import TestClient
from database import Base, engine  # noqa: E402


@pytest.fixture()
def client():
    from main import app

    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as c:  # triggers lifespan -> create_all
        yield c
