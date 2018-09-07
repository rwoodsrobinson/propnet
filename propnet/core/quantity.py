# TODO: remove typing
from typing import *

from monty.json import MSONable

from propnet import ureg
from propnet.core.symbols import Symbol
from propnet.symbols import DEFAULT_SYMBOLS


class Quantity(MSONable):
    """
    Class storing the value of a property.

    Constructed by the user to assign values to abstract Symbol types. Represents the fact
    that a given Quantity
    has a given value. They are added to the PropertyNetwork graph in the context of Material
    objects that store
    collections of Quantity objects representing that a given material has those properties.

    Attributes:
        symbol_type: (Symbol) the type of information that is represented by the associated value.
        value: (id) the value associated with this symbol.
        tags: (list<str>)
        material (set<Material>): the materials to which this quantity is bound -- indicates which materials
                                   this quantity is representing.
    """

    def __init__(self,
                 symbol_type: Union[str, Symbol],
                 value: Any,
                 tags: Optional[List[str]]=None,
                 provenance=None):
        """
        Parses inputs for constructing a Property object.

        Args:
            symbol_type (Symbol): pointer to an existing PropertyMetadata
                object or String giving the name of a SymbolType object,
                identifies the type of data stored in the property.
            value (id): value of the property.
            tags (list<str>): list of strings storing metadata from
                Quantity evaluation.
            provenance (id): time of creation of the object.
        """

        if isinstance(symbol_type, str):
            if symbol_type not in DEFAULT_SYMBOLS.keys():
                raise ValueError("Quantity type {} not recognized".format(symbol_type))
            symbol_type = DEFAULT_SYMBOLS[symbol_type]

        if type(value) == float or type(value) == int:
            value = ureg.Quantity(value, symbol_type.units)
        elif type(value) == ureg.Quantity:
            value = value.to(symbol_type.units)

        self._symbol_type = symbol_type
        self._value = value
        self._tags = tags
        self._provenance = provenance

    @property
    def value(self):
        """
        Returns:
            (id): value of the Quantity
        """
        return self._value

    @property
    def symbol(self):
        """
        Returns:
            (Symbol): Symbol of the Quantity
        """
        return self._symbol_type

    @property
    def tags(self):
        """
        Returns:
            (list<str>): tags of the Quantity
        """
        return self._tags

    @property
    def provenance(self):
        """
        Returns:
            (id): time of creation of the Quantity
        """
        return self._provenance

    def __hash__(self):
        return hash(self.symbol.name)

    def __eq__(self, other):
        if not isinstance(other, Quantity) \
                or self.symbol != other.symbol \
                or self.symbol.category != other.symbol.category:
            return False
        return self.value == other.value

    def __str__(self):
        return "<{}, {}, {}>".format(self.symbol.name, self.value, self.tags)

    def __bool__(self):
        return bool(self.value)

    # TODO: lazily implemented, fix to be a bit more robust
    def as_dict(self):
        if isinstance(self.value, ureg.Quantity):
            value = self.value.magnitude
            units = self.value.units
        else:
            value = self.value
            units = None
        return {"symbol_type": self._symbol_type.name,
                "value": value,
                "provenance": self._provenance.as_dict() if self._provenance is not None else None,
                "units": units.format_babel() if units else None,
                "@module": "propnet.core.quantity",
                "@class": "Quantity"}
