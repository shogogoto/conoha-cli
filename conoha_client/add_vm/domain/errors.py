"""add vm erros."""


class ImageIdMappingMismatchWarning(Warning):
    """VM Image Idを検索できない可能性が生じた."""


class NotFoundFlavorIdError(Exception):
    """Flavorが見つからないはずがない."""


class OSVersionExtractError(Exception):
    """Image名にOS名やバージョン情報が入っていない訳がない."""


class ApplicationWithoutVersionError(Exception):
    """Image名にアプリ名やバージョン情報が入っていない訳がない."""


class ApplicationUnexpectedError(Exception):
    """アプリ情報が何らかのせいで正常に取得できなかった."""


class NotFoundOSVersionError(Exception):
    """OSのバージョンが見つからなかった."""


class NotFoundApplicationError(Exception):
    """アプリケーションが見つからなかった."""


class NotFlavorProvidesError(Exception):
    """そのImageとFlavorの組み合わせは提供されていない."""


class NotFoundAddedVMError(Exception):
    """VMが追加されたはずなのに契約中VM一覧にはない."""
