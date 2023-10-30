"""VM Image errors."""


class NeitherWindowsNorLinuxError(Exception):
    """WindowsかLinuxのどちらかしか有り得ない."""


class NotLinuxError(Exception):
    """Linuxしか許されない."""


class DistributionNotFoundInImageNameError(Exception):
    """イメージ名からLinux Distributionを特定できなかった."""


class ImageIdMatchNotUniqueError(Exception):
    """image idが一意にマッチしなかった."""


class DeleteImageError(Exception):
    """image削除に失敗した."""


class DeletePriorImageForbiddenError(Exception):
    """所与のイメージ削除は禁止."""
