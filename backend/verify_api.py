import requests
import sys
import time
import subprocess

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        print("✅ Health check passed")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)

def test_contacts():
    # Create
    contact_data = {
        "name": "Alice Window",
        "email": "alice@example.com",
        "phone": "555-0100",
        "company": "Wonderland Inc"
    }
    response = requests.post(f"{BASE_URL}/contacts/", json=contact_data)
    assert response.status_code == 201
    created_contact = response.json()
    assert created_contact["name"] == contact_data["name"]
    contact_id = created_contact["id"]
    print("✅ Create Contact passed")

    # Read
    response = requests.get(f"{BASE_URL}/contacts/{contact_id}")
    assert response.status_code == 200
    assert response.json()["email"] == contact_data["email"]
    print("✅ Read Contact passed")

    # Update
    update_data = {"position": "Director"}
    response = requests.put(f"{BASE_URL}/contacts/{contact_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["position"] == "Director"
    print("✅ Update Contact passed")

    # Delete
    response = requests.delete(f"{BASE_URL}/contacts/{contact_id}")
    assert response.status_code == 200
    print("✅ Delete Contact passed")

    # Verify Delete
    response = requests.get(f"{BASE_URL}/contacts/{contact_id}")
    assert response.status_code == 404
    print("✅ Verify Delete Contact passed")

def main():
    print("Waiting for server to start...")
    # Simple retry mechanism to wait for server
    for i in range(10):
        try:
            requests.get(f"{BASE_URL}/health")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        print("❌ Server failed to start")
        sys.exit(1)
        
    test_health()
    test_contacts()
    print("\nAll tests passed!")

if __name__ == "__main__":
    main()
