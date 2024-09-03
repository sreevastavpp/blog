import pytest
import os
import sqlite3
from user import UserDatabase


@pytest.fixture
def user_db():
    # Setup: Create a temporary database
    db_path = "test_users.db"
    db = UserDatabase(db_path)

    yield db  # This is where the testing happens

    # Teardown: Close the database connection and remove the file
    db.close()
    os.remove(db_path)


def test_add_user(user_db):
    user_db.add_user("john_doe", "john@example.com")
    user = user_db.get_user("john_doe")
    assert user is not None
    assert user[1] == "john_doe"
    assert user[2] == "john@example.com"


def test_get_nonexistent_user(user_db):
    user = user_db.get_user("nonexistent")
    assert user is None


def test_add_duplicate_user(user_db):
    user_db.add_user("jane_doe", "jane@example.com")
    with pytest.raises(sqlite3.IntegrityError):
        user_db.add_user("jane_doe", "jane_another@example.com")
