========
Autoform
========

--------------------------------------------------------
Automatically generated wtf Forms from SQLAlchemy models
--------------------------------------------------------


**Usage:**

.. code-block:: python

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    from autoform.forms import SqlaForm


    Base = declarative_base()
    engine = create_engine('sqlite:///app.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()


    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        username = Column(String(64))
        password = Column(String(64))

        def __repr__(self):
            return '<User: {}>'.format(self.name)


    class UserForm(SqlaForm):
        class ModelMeta:
            model = User
            session = session  # has to be created beforehand
