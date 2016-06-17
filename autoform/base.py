"""Automatic wtf Form generation from SQLAlchemy models."""

from wtforms.form import FormMeta
from wtforms.fields import SelectField
from wtforms.fields import (StringField, IntegerField, FloatField,
                            BooleanField)

from sqlalchemy import String, Integer, Float, Boolean


MAPPING = {
    String: StringField,
    Integer: IntegerField,
    Float: FloatField,
    Boolean: BooleanField,
}


def get_model_by_tablename(origin, table):
    """Return the model that represents given table."""
    for model in origin._decl_class_registry.values():
        if hasattr(model, '__tablename__') and model.__tablename__ == table:
            return model
    raise ValueError('No model exists for table %s' % table)


def get_related_model(origin, fk):
    """fk has the form <tablename>.<column>, assume <column>=id."""
    fk_table, fk_col = fk.split('.')
    fk_model = get_model_by_tablename(origin, fk_table)
    return fk_model


def is_foreign_key(col):
    """Check if a column is a foreign key."""
    if col.foreign_keys:
        return True
    return False


class SqlaFormMeta(FormMeta):
    """Extends wtf's FormMeta and generates fields from sql model columns."""

    def __new__(cls, name, bases, attrs):
        if 'ModelMeta' not in attrs:
            return super(SqlaFormMeta, cls).__new__(cls, name, bases, attrs)
        model_meta = attrs.get('ModelMeta')
        model = getattr(model_meta, 'model')
        excluded = getattr(model_meta, 'exclude', ())
        session = getattr(model_meta, 'session')
        for col_name, col_type in model.__table__.columns.items():
            if col_name in excluded:
                continue

            field_name = col_name
            if is_foreign_key(col_type):
                fk = list(col_type.foreign_keys)[0].target_fullname
                rel_model = get_related_model(model, fk)
                choices = [(m.id, m.name)
                           for m in session.query(rel_model).all()]
                field = SelectField(field_name, choices=choices)
            else:
                field_type = MAPPING.get(col_type.type.__class__, None)
                field = field_type(field_name)
            assert field_type is not None, 'Column type not recognized'
            attrs.update({field_name: field})

        return super(SqlaFormMeta, cls).__new__(cls, name, bases, attrs)
