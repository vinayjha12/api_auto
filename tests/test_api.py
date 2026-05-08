import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

# ==================== GLOBAL CONFIGURATION ====================
BASE_URL = os.getenv("BASE_URL", "https://auth.vvdntech.com/api/v1")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")

COMMON_HEADERS = {
    "Content-Type": "application/json"
}

# ==================== TEST FUNCTIONS ====================
def test_tc001_verify_successful_user_creation_with_all_valid_fields():
    """TC001: Verify successful user creation with all valid fields | Expected: 201"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
      "email": "john.doe@example.com",
      "designation": "Senior Software Engineer",
      "phoneNumber": "+919876543210",
      "empName": "John Doe",
      "username": "johndoe123",
      "password": "StrongP@ssw0rd!",
      "empNo": "EMP12345"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "data" in response_data
    assert isinstance(response_data.get("data"), dict)
    assert "username" in response_data.get("data", {})
    assert "email" in response_data.get("data", {})
    assert "empNo" in response_data.get("data", {})
    assert "enabled" in response_data.get("data", {})

def test_tc002_verify_api_rejects_request_with_missing_authorization_header():
    """TC002: Verify API rejects request with missing Authorization header | Expected: 401"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Content-Type": "application/json"
    }
    payload = {
      "email": "jane.doe@example.com",
      "designation": "QA Engineer",
      "phoneNumber": "+919876543211",
      "empName": "Jane Doe",
      "username": "janedoe456",
      "password": "ValidP@ssw0rd!",
      "empNo": "EMP12346"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 401, f"Expected 401, got {response.status_code} | {response.text[:200]}"

def test_tc003_verify_api_rejects_request_with_an_invalid_random_token():
    """TC003: Verify API rejects request with an invalid (random) token | Expected: 401"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Authorization": "Bearer invalid_token_xyz",
        "Content-Type": "application/json"
    }
    payload = {
      "email": "jane.doe@example.com",
      "designation": "QA Engineer",
      "phoneNumber": "+919876543211",
      "empName": "Jane Doe",
      "username": "janedoe456",
      "password": "ValidP@ssw0rd!",
      "empNo": "EMP12346"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 401, f"Expected 401, got {response.status_code} | {response.text[:200]}"
    assert "message" in response.json()

def test_tc004_verify_api_rejects_request_with_an_expired_token():
    """TC004: Verify API rejects request with an expired token | Expected: 401"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Authorization": "Bearer expired_token_xyz",
        "Content-Type": "application/json"
    }
    payload = {
      "email": "jane.doe@example.com",
      "designation": "QA Engineer",
      "phoneNumber": "+919876543211",
      "empName": "Jane Doe",
      "username": "janedoe456",
      "password": "ValidP@ssw0rd!",
      "empNo": "EMP12346"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 401, f"Expected 401, got {response.status_code} | {response.text[:200]}"
    assert "message" in response.json()

def test_tc005_verify_api_rejects_request_from_an_unauthorized_user_role():
    """TC005: Verify API rejects request from an unauthorized user role | Expected: 403"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
      "email": "test.user@example.com",
      "designation": "Intern",
      "phoneNumber": "+919000000000",
      "empName": "Test User",
      "username": "testuser",
      "password": "Password123!",
      "empNo": "EMP99999"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 403, f"Expected 403, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data
    assert "path" in response_data

def test_tc006_verify_api_rejects_creation_of_a_user_with_a_duplicate_username():
    """TC006: Verify API rejects creation of a user with a duplicate username | Expected: 409"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
      "email": "new.user@example.com",
      "designation": "Engineer",
      "phoneNumber": "+919111122222",
      "empName": "New User",
      "username": "existinguser",
      "password": "Password123!",
      "empNo": "EMP55555"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 409, f"Expected 409, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data

def test_tc007_verify_api_rejects_creation_of_a_user_with_a_duplicate_employee_number():
    """TC007: Verify API rejects creation of a user with a duplicate employee number | Expected: 409"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
      "email": "another.user@example.com",
      "designation": "Analyst",
      "phoneNumber": "+919333344444",
      "empName": "Another User",
      "username": "anotheruser",
      "password": "Password123!",
      "empNo": "EMP12345"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 409, f"Expected 409, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data

def test_tc008_verify_api_rejects_request_with_a_missing_mandatory_field_username():
    """TC008: Verify API rejects request with a missing mandatory field (username) | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {
        **COMMON_HEADERS,
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
      "email": "missing.username@example.com",
      "designation": "SSE",
      "phoneNumber": "+911232455465",
      "empName": "asfGDG",
      "password": "gh@W12343",
      "empNo": "176354365"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data
    assert "details" in response_data
    assert isinstance(response_data.get("details"), list)

def test_tc009_verify_api_rejects_request_with_an_invalid_email_format():
    """TC009: Verify API rejects request with an invalid email format | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
      "email": "invalid-email-format",
      "designation": "SSE",
      "phoneNumber": "+911232455465",
      "empName": "asfGDG",
      "username": "invalidemailuser",
      "password": "gh@W12343",
      "empNo": "176354365"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data
    assert "details" in response_data
    assert isinstance(response_data.get("details"), list)

def test_tc010_verify_api_rejects_request_with_an_empty_request_body():
    """TC010: Verify API rejects request with an empty request body | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {}
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data

def test_tc011_verify_api_rejects_request_with_an_invalid_phone_number_format():
    """TC011: Verify API rejects request with an invalid phone number format | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
      "email": "phone.test@example.com",
      "designation": "SSE",
      "phoneNumber": "12345",
      "empName": "Phone Test",
      "username": "phonetestuser",
      "password": "gh@W12343",
      "empNo": "176354370"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data
    assert "details" in response_data
    assert isinstance(response_data.get("details"), list)

def test_tc012_verify_api_rejects_request_with_a_weak_password():
    """TC012: Verify API rejects request with a weak password | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
      "email": "weak.pass@example.com",
      "designation": "SSE",
      "phoneNumber": "+919876543210",
      "empName": "Weak Pass",
      "username": "weakpassuser",
      "password": "123",
      "empNo": "176354371"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data
    assert "details" in response_data
    assert isinstance(response_data.get("details"), list)

def test_tc013_verify_api_handles_very_long_string_input_for_empname():
    """TC013: Verify API handles very long string input for empName | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
      "email": "long.name@example.com",
      "designation": "SSE",
      "phoneNumber": "+919876543210",
      "empName": "AbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyz",
      "username": "longnameuser",
      "password": "gh@W12343",
      "empNo": "176354372"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data
    assert "details" in response_data
    assert isinstance(response_data.get("details"), list)

def test_tc014_verify_api_handles_username_with_special_characters():
    """TC014: Verify API handles username with special characters | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
      "email": "special.char@example.com",
      "designation": "SSE",
      "phoneNumber": "+919876543210",
      "empName": "Special Char",
      "username": "user!@#$%",
      "password": "gh@W12343",
      "empNo": "176354373"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "error" in response_data
    assert "details" in response_data
    assert isinstance(response_data.get("details"), list)

def test_tc015_verify_api_handles_username_with_leading_trailing_spaces():
    """TC015: Verify API handles username with leading/trailing spaces | Expected: 201"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
      "email": "spaces.user@example.com",
      "designation": "SSE",
      "phoneNumber": "+919876543210",
      "empName": "Spaces User",
      "username": "  spacesuser  ",
      "password": "gh@W12343",
      "empNo": "176354374"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "status" in response_data
    assert "message" in response_data
    assert "data" in response_data
    assert "username" in response_data.get("data", {})

def test_tc016_verify_api_rejects_request_with_wrong_content_type_header():
    """TC016: Verify API rejects request with wrong Content-Type header | Expected: 415"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/xml"}
    payload = {
      "email": "wrong.content@example.com",
      "designation": "SSE",
      "phoneNumber": "+919876543210",
      "empName": "Wrong Content",
      "username": "wrongcontent",
      "password": "gh@W12343",
      "empNo": "176354375"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 415, f"Expected 415, got {response.status_code} | {response.text[:200]}"
    assert "error" in response.json()

def test_tc017_verify_api_rejects_request_with_null_value_for_a_mandatory_field():
    """TC017: Verify API rejects request with null value for a mandatory field | Expected: 400"""
    url = f"{BASE_URL}/api/v1/users"
    headers = {**COMMON_HEADERS}
    headers["Authorization"] = "Bearer " + AUTH_TOKEN
    payload = {"email": "null.field@example.com", "designation": "SSE", "phoneNumber": "+919876543210", "empName": "Null Field", "username": None, "password": "gh@W12343", "empNo": "176354376"}
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert 'status' in data
    assert 'message' in data
    assert 'error' in data
    assert 'path' in data
    assert 'details' in data