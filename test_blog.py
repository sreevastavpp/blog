import pytest
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from models import get_db_engine, Base
from repositories import UserRepository, PostRepository


@pytest.fixture(scope="session")
def db_engine():
    # Setup: Create a temporary in-memory SQLite database
    db_url = "sqlite:///:memory:"
    engine = get_db_engine(db_url)
    Base.metadata.create_all(engine)

    yield engine  # This is where the testing happens

    # Teardown: Drop all tables
    Base.metadata.drop_all(engine)


@pytest.fixture
def user_repo(db_engine):
    return UserRepository(db_engine)


@pytest.fixture
def post_repo(db_engine):
    return PostRepository(db_engine)


def test_add_user(user_repo):
    user_repo.add_user("jane_doe", "jane@example.com")
    retrieved_user = user_repo.get_user("jane_doe")
    assert retrieved_user.username == "jane_doe"
    assert retrieved_user.email == "jane@example.com"


def test_add_duplicate_user(user_repo):
    with pytest.raises(IntegrityError):
        user_repo.add_user("jane_doe", "jane_another@example.com")


def test_get_nonexistent_user(user_repo):
    user = user_repo.get_user("nonexistent")
    assert user is None


def test_add_post(user_repo, post_repo):
    user_repo.add_user("alice", "alice@example.com")
    user = user_repo.get_user("alice")
    post_repo.add_post("First Post", "Hello, World!", user.id)
    post = post_repo.get_post(1)
    assert post.title == "First Post"
    assert post.content == "Hello, World!"
    assert post.author_id == user.id


def test_get_user_with_posts(user_repo, post_repo):
    user_repo.add_user("charlie", "charlie@example.com")
    user = user_repo.get_user("charlie")
    post_repo.add_post("Charlie's Post", "Hello from Charlie!", user.id)

    user_with_posts = user_repo.get_user_with_posts("charlie")
    assert user_with_posts.username == "charlie"
    assert len(user_with_posts.posts) == 1
    assert user_with_posts.posts[0].title == "Charlie's Post"


def test_get_user_posts(user_repo, post_repo):
    user_repo.add_user("bob", "bob@example.com")
    user = user_repo.get_user("bob")
    post_repo.add_post("Post 1", "Content 1", user.id)
    post_repo.add_post("Post 2", "Content 2", user.id)

    posts = post_repo.get_user_posts(user.id)
    assert len(posts) == 2
    assert posts[0].title == "Post 1"
    assert posts[1].title == "Post 2"
