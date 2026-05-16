from password_checker import check_password
from password_generator import generate_password
from unittest.mock import patch

# Test 1: Too short
def test_too_short():
    strong, msgs = check_password("Short1!")
    assert not strong
    assert any("Too short" in m for m in msgs)

# Test 2: Missing uppercase
def test_missing_uppercase():
    strong, msgs = check_password("alllowercase1!")
    assert not strong
    assert any("uppercase" in m for m in msgs)

# Test 3: Missing number
def test_missing_number():
    strong, msgs = check_password("NoNumberHere!")
    assert not strong
    assert any("number" in m.lower() for m in msgs)

# Test 4: Missing special char
def test_missing_special():
    strong, msgs = check_password("NoSpecialChar1")
    assert not strong
    assert any("special" in m.lower() for m in msgs)

# Test 5: Strong password
def test_strong_password():
    strong, msgs = check_password("StrongPass@123")
    assert strong

# Test 6: Generator length
def test_generator_length():
    pwd = generate_password(length=20)
    assert len(pwd) == 20

# Test 7: Generator has all required chars
def test_generator_policy():
    pwd = generate_password(length=16)
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in "!@#$%^&*()" for c in pwd)

# Test 8: No symbols flag
def test_no_symbols():
    pwd = generate_password(length=16, no_symbols=True)
    assert not any(c in "!@#$%^&*()" for c in pwd)

# --- NEW TESTS FOR FIXES ---

# Test 9: Password too long — input validation
def test_password_too_long():
    import pytest
    from app import app
    client = app.test_client()
    res = client.post('/check',
        json={"password": "A" * 129},
        content_type='application/json'
    )
    assert res.status_code == 400
    assert b'too long' in res.data.lower()

# Test 10: Invalid length in generate
def test_invalid_length():
    from app import app
    client = app.test_client()
    res = client.post('/generate',
        json={"length": 8},
        content_type='application/json'
    )
    assert res.status_code == 400

# Test 11: Invalid no_symbols type
def test_invalid_no_symbols():
    from app import app
    client = app.test_client()
    res = client.post('/generate',
        json={"length": 16, "no_symbols": "yes"},
        content_type='application/json'
    )
    assert res.status_code == 400

# Test 12: Raw password not in generate response
@patch('app.send_password_to_slack')
def test_password_not_in_response(mock_slack):
    mock_slack.return_value = (True, '✅ Password sent to Slack!')
    from app import app
    client = app.test_client()
    res = client.post('/generate',
        json={"length": 16},
        content_type='application/json'
    )
    data = res.get_json()
    # Only hint returned, not full password
    assert "password_hint" in data
    assert "*" in data["password_hint"]

# Test 13: HIBP API failure blocks password
@patch('hibp.requests.get')
def test_hibp_failure_blocks(mock_get):
    mock_get.side_effect = Exception("API down")
    from hibp import check_hibp
    breached, msg = check_hibp("SomePassword123!")
    # Strict fail — should be treated as breached
    assert breached
    assert "try again" in msg.lower()