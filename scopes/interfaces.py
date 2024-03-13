# scopes.interfaces

from zope.interface import Interface


class ITraversable(Interface):

    def get(key, default):
        """Return the item addressed by `key`; return `default` if not found."""


class IContainer(ITraversable):

    def items():
        """Return a sequence of key, value pairs of child objects."""

    def keys():
        """Return a sequence of keys of child objects."""

    def __getitem__(key):
        """Return the item addressed by `key`; rais KeyError if not found."""

    def __setitem__(key, value):
        """Store the `value` under the `key`. 

        May modify `value` so that the attributes referencing this object
        and the value object (e.g. `parent´ and `name`) are stored correctly."""


class IView(Interface):

    def __call__():
        """Render the view data as HTML or JSON."""

