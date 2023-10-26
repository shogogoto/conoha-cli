"""add vm erros."""


class ImageIdentifyError(Exception):
    """VM Imageを一意に特定できなかった."""


class NotFlavorProvidesError(Exception):
    """そのImageとFlavorの組み合わせは提供されていない."""


class NotFoundAddedVMError(Exception):
    """VMが追加されたはずなのに契約中VM一覧にはない."""
