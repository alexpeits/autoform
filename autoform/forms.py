from six import with_metaclass

from wtforms import Form

from .base import SqlaFormMeta


class SqlaForm(with_metaclass(SqlaFormMeta, Form)):
    """Use with regular wtforms Form class."""
    pass
