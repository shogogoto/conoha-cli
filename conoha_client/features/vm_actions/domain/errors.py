"""VM actions error."""


class VMDeleteError(Exception):
    """VMを削除できなかった."""


class VMShutdownError(Exception):
    """VMをシャットダウンできなかった."""
