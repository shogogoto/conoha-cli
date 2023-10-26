"""VM errors."""


class NotFlavorProvidesError(Exception):
    """そのImageとFlavorの組み合わせは提供されていない."""


class NotFoundAddedVMError(Exception):
    """VMが追加されたはずなのに契約中VM一覧にはない."""
