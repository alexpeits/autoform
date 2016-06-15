from wtforms.form import BaseForm, FormMeta
from wtforms import Form
from wtforms.fields import StringField, IntegerField
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from six import with_metaclass

MAPPING = {
    String: StringField,
    Integer: IntegerField,
    # etc.
}


class SqlaFormMeta(FormMeta):

    def __new__(cls, name, bases, attrs):
        if 'ModelMeta' not in attrs:
            return super(SqlaFormMeta, cls).__new__(cls, name, bases, attrs)
        model_meta = attrs.get('ModelMeta')
        model = getattr(model_meta, 'model')
        for col_name, col_type in model.__table__.columns.items():
            field_name = col_name
            field_type = MAPPING.get(col_type.type.__class__, None)(field_name.upper())
            assert field_type is not None, 'Column type not recognized'
            attrs.update({field_name: field_type})

        return super(SqlaFormMeta, cls).__new__(cls, name, bases, attrs)


class SqlaForm(with_metaclass(SqlaFormMeta, object)):
    pass


# Example:

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64))
    password = Column(String(64))

    def __repr__(self):
        return '<User: {}>'.format(self.name)


class UserForm(SqlaForm, Form):
    class ModelMeta:
        model = User
