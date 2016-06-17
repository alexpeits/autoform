from six import with_metaclass

from flask.ext.wtf import Form as FlaskForm

from .base import SqlaFormMeta

class SqlaFlaskForm(with_metaclass(SqlaFormMeta, FlaskForm)):
    """Use with Flask-WTForms Form class."""
    pass
