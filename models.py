from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)


class UserDatabase:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, username, email):
        session = self.Session()
        try:
            new_user = User(username=username, email=email)
            session.add(new_user)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_user(self, username):
        session = self.Session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()

    def close(self):
        self.engine.dispose()
