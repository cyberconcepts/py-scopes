# scopes.interfaces

from zope.interface import Interface


class ITraversable(Interface):

    def get(key, default=None):
        """Return the item addressed by `key`; return `default` if not found."""


class IContainer(ITraversable):

    def values():
        """Return a sequence of child objects."""

    def __getitem__(key):
        """Return the item addressed by `key`; raise KeyError if not found."""

    def __setitem__(key, value):
        """Store the `value` under the `key`. 

        May modify `value` so that the attributes referencing this object
        and the value object (e.g. `parent´ and `name`) are stored correctly."""


class IConcept(IContainer):

    def parents(*predicates):
        """Return a sequence of `Triple`s in which this object is 
           referenced as `second`."""

    def children(*predicates):
        """Return a sequence of `Triple`s in which this object is 
           referenced as `first`."""


class IView(Interface):

    def __call__():
        """Render the view data as HTML or JSON."""

