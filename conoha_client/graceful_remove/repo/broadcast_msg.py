"""broadcast message."""
import subprocess


def broadcast_message(msg: str) -> None:
    """Display message on the terminals of all currently logged in users."""
    result = subprocess.run(["/usr/bin/wall", msg], check=True)  # noqa: S603
    result.check_returncode()
