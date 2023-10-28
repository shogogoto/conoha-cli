"""VM Image errors."""


class NeitherWindowsNorLinuxError(Exception):
    """WindowsかLinuxのどちらかしか有り得ない."""


class NotLinuxError(Exception):
    """Linuxしか許されない."""


class DistributionNotFoundInImageNameError(Exception):
    """イメージ名からLinux Distributionを特定できなかった."""


class OSIdentificationError(Exception):
    """OSを一意に特定できなかった."""


class OSVersionExtractError(Exception):
    """Image名にOS名やバージョン情報が入っていない訳がない."""


class ApplicationWithoutVersionError(Exception):
    """Image名にアプリ名やバージョン情報が入っていない訳がない."""
