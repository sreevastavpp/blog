import pytest
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
    user_repo.add(username="jane_doe", email="jane@example.com")
    retrieved_user = user_repo.get_user("jane_doe")
    assert retrieved_user.username == "jane_doe"
    assert retrieved_user.email == "jane@example.com"


def test_add_duplicate_user(user_repo):
    with pytest.raises(IntegrityError):
        user_repo.add(username="jane_doe", email="jane@example.com")


def test_get_nonexistent_user(user_repo):
    user = user_repo.get_user("nonexistent")
    assert user is None


def test_add_post(user_repo, post_repo):
    user_repo.add(username="alice", email="alice@example.com")
    user = user_repo.get_user("alice")
    post_repo.add(title="First Post", content="Hello, World!", author_id=user.id)
    post = post_repo.get_by_id(1)
    assert post.title == "First Post"
    assert post.content == "Hello, World!"
    assert post.author_id == user.id


def test_get_user_with_posts(user_repo, post_repo):
    user_repo.add(username="charlie", email="charlie@example.com")
    user = user_repo.get_user("charlie")
    post_repo.add(
        title="Charlie's Post", content="Hello from Charlie!", author_id=user.id
    )

    user_with_posts = user_repo.get_user_with_posts("charlie")
    assert user_with_posts.username == "charlie"
    assert len(user_with_posts.posts) == 1
    assert user_with_posts.posts[0].title == "Charlie's Post"


def test_get_user_posts(user_repo, post_repo):
    user_repo.add(username="bob", email="bob@example.com")
    user = user_repo.get_user("bob")
    post_repo.add(title="Post 1", content="Content 1", author_id=user.id)
    post_repo.add(title="Post 2", content="Content 2", author_id=user.id)

    posts = post_repo.get_user_posts(user.id)
    assert len(posts) == 2
    assert posts[0].title == "Post 1"
    assert posts[1].title == "Post 2"


"""
To demostrate the difference between scope="function" and scope="module",
"""


def test_get_all_posts(post_repo):
    posts = post_repo.all()
    assert len(posts) == 4
    assert posts[0].title == "First Post"
    assert posts[1].title == "Charlie's Post"


def test_get_all_users(user_repo):
    user_repo.add(username="user1", email="user1@example.com")
    user_repo.add(username="user2", email="user2@example.com")
    users = user_repo.all()
    assert len(users) == 6
    assert {u.username for u in users} == {
        "jane_doe",
        "alice",
        "charlie",
        "bob",
        "user1",
        "user2",
    }


# def test_get_post_by_id(user_repo, post_repo):
#     user_repo.add_user("alice", "alice@example.com")
#     user = user_repo.get_user("alice")
#     post_repo.add_post("First Post", "Hello, World!", user.id)
#     retrieved_post = post_repo.get_post(1)
#     assert retrieved_post.title == "First Post"
#     assert retrieved_post.content == "Hello, World!"
