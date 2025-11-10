if __name__ == '__main__':
    from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine
    from sqlalchemy.orm import sessionmaker, mapper

    engine = create_engine("sqlite:///python.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()

    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(16), nullable=False),
                  Column('email', String(50)),
                  Column('login', String(60), nullable=False)
                )

    class User(object):
        def __init__(self, name, email, login):
            self.name = name
            self.email = email
            self.login = login

        def __repr__(self):
            return f"{self.name}, {self.email}, {self.login}"

    mapper(User, users)
    metadata.create_all(bind=engine)