"""add vm erros."""


class ImageIdMappingMismatchWarning(Warning):
    """VM Image Idを検索できない可能性が生じた."""


class NotFoundFlavorIdError(Exception):
    """Flavorが見つからないはずがない."""


class NotFoundVersionError(Exception):
    """OSのバージョンが見つからなかった."""
