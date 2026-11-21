def make_contact(client, email="ada@example.com", **kw):
    body = {"first_name": "Ada", "last_name": "Lovelace", "email": email, **kw}
    r = client.post("/contacts/", json=body)
    assert r.status_code == 201, r.text
    return r.json()


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_contact_crud_and_duplicate_email(client):
    c = make_contact(client, phone="123", company="Analytical Engines")
    assert client.get(f"/contacts/{c['id']}").json()["company"] == "Analytical Engines"
    assert client.post("/contacts/", json={"first_name": "X", "email": "ADA@example.com"}).status_code == 409
    r = client.put(f"/contacts/{c['id']}", json={"position": "Mathematician"})
    assert r.json()["position"] == "Mathematician" and r.json()["first_name"] == "Ada"
    assert client.delete(f"/contacts/{c['id']}").status_code == 200
    assert client.get(f"/contacts/{c['id']}").status_code == 404


def test_blank_form_fields_are_accepted(client):
    """The React forms send '' for empty optional inputs."""
    c = make_contact(client)
    r = client.post("/deals/", json={"title": "Deal", "value": "1500", "stage": "New",
                                     "contact_id": str(c["id"]), "expected_close_date": ""})
    assert r.status_code == 201, r.text
    assert r.json()["value"] == 1500 and r.json()["expected_close_date"] is None
    r = client.post("/tasks/", json={"title": "Call", "description": "", "due_date": ""})
    assert r.status_code == 201 and r.json()["is_completed"] is False


def test_validation_errors(client):
    assert client.post("/contacts/", json={"first_name": "A", "email": "not-an-email"}).status_code == 422
    assert client.post("/deals/", json={"title": "D", "value": 0}).status_code == 422
    assert client.post("/deals/", json={"title": "D", "value": 5, "stage": "Bogus"}).status_code == 422
    assert client.post("/deals/", json={"title": "D", "value": 5, "contact_id": 999}).status_code == 422
    assert client.post("/tasks/", json={"title": "T", "related_deal_id": 999}).status_code == 422


def test_deleting_contact_keeps_deals_unlinked(client):
    c = make_contact(client)
    d = client.post("/deals/", json={"title": "D", "value": 10, "contact_id": c["id"]}).json()
    client.delete(f"/contacts/{c['id']}")
    assert client.get(f"/deals/{d['id']}").json()["contact_id"] is None


def test_deal_stage_move_and_task_toggle(client):
    d = client.post("/deals/", json={"title": "D", "value": 10}).json()
    assert client.put(f"/deals/{d['id']}", json={"stage": "Won"}).json()["stage"] == "Won"
    t = client.post("/tasks/", json={"title": "T"}).json()
    assert client.put(f"/tasks/{t['id']}", json={"is_completed": True}).json()["is_completed"] is True


def test_stats(client):
    client.post("/deals/", json={"title": "A", "value": 100})
    client.post("/deals/", json={"title": "B", "value": 50, "stage": "Won"})
    client.post("/tasks/", json={"title": "T1"})
    t2 = client.post("/tasks/", json={"title": "T2"}).json()
    client.put(f"/tasks/{t2['id']}", json={"is_completed": True})
    s = client.get("/stats").json()
    assert s["deals"] == 2 and s["open_pipeline_value"] == 100 and s["won_value"] == 50
    assert s["tasks_open"] == 1 and s["tasks_done"] == 1
    assert s["deals_by_stage"] == {"New": 1, "Negotiation": 0, "Won": 1, "Lost": 0}
