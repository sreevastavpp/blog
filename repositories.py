from sqlalchemy.orm import sessionmaker, joinedload
from models import User, Post


class BaseRepository:
    def __init__(self, engine, model):
        self.Session = sessionmaker(bind=engine)
        self.model = model

    def _session_manager(self):
        session = self.Session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add(self, **kwargs):
        with next(self._session_manager()) as session:
            entity = self.model(**kwargs)
            session.add(entity)
            session.commit()

    def get_by_id(self, id):
        with next(self._session_manager()) as session:
            return session.query(self.model).filter_by(id=id).first()

    def all(self):
        with next(self._session_manager()) as session:
            return session.query(self.model).all()


class UserRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine, User)

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


class PostRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine, Post)

    def get_user_posts(self, user_id):
        with next(self._session_manager()) as session:
            return session.query(Post).filter_by(author_id=user_id).all()
