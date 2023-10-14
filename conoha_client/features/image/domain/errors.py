"""VM Image errors."""


class NeitherWindowsNorLinuxError(Exception):
    """WindowsかLinuxのどちらかしか有り得ない."""
