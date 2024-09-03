from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, joinedload
from models import User, Post


class Repository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def _session_manager(self):
        session = self.Session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class UserRepository(Repository):
    def add_user(self, username, email):
        print(f"Attempting to add user: {username}")  # Debug print
        with next(self._session_manager()) as session:
            new_user = User(username=username, email=email)
            session.add(new_user)
            session.commit()

    def get_user(self, username):
        with next(self._session_manager()) as session:
            return session.query(User).filter_by(username=username).first()

    def get_user_with_posts(self, username):
        with next(self._session_manager()) as session:
            return (
                session.query(User)
                .filter_by(username=username)
                .options(joinedload(User.posts))
                .first()
            )


class PostRepository(Repository):
    def add_post(self, title, content, author_id):
        with next(self._session_manager()) as session:
            new_post = Post(title=title, content=content, author_id=author_id)
            session.add(new_post)
            session.commit()

    def get_post(self, post_id):
        with next(self._session_manager()) as session:
            return session.query(Post).filter_by(id=post_id).first()

    def get_user_posts(self, user_id):
        with next(self._session_manager()) as session:
            return session.query(Post).filter_by(author_id=user_id).all()
