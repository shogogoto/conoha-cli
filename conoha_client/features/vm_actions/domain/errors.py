"""VM actions error."""


class VMDeleteError(Exception):
    """VMを削除できなかった."""


class VMActionTargetNotFoundError(Exception):
    """VM操作対象が見つからなかったときの共通エラー."""


class VMShutdownError(Exception):
    """VMをシャットダウンできなかった."""


class VMBootError(Exception):
    """VMを起動できなかった."""


class VMRebootError(Exception):
    """VMを再起動できなかった."""


class VMSnapshotError(Exception):
    """VMをイメージとして保存できなかった."""
