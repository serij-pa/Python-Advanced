if __name__ == '__main__':
    from sqlalchemy import Column, Integer, String, create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

    engine = create_engine("sqlite:///python.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    #Base = declarative_base()

    class Base(DeclarativeBase): pass

    class User(Base):
        __tablename__ = "user"

        id = Column(Integer, primary_key=True)
        name = Column(String(16), nullable=False)
        email = Column(String(50))
        login = Column(String(60), nullable=False)

        def __repr__(self):
            return f"{self.name}, {self.email}, {self.login}"
    Base.metadata.create_all(engine)