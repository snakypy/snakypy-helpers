from subprocess import Popen, PIPE
from snakypy.helpers.utils.decorators import only_linux


@only_linux
def command_superuser(cmd: str) -> None:
    Popen(["su", "-c", cmd])


@only_linux
def systemctl_is_active(service: str) -> tuple:
    process = Popen(
        ["systemctl", "is-active", service], stdout=PIPE, universal_newlines=True
    )
    output, err = process.communicate()
    return output.replace("\n", ""), err


__all__ = ["command_superuser", "systemctl_is_active"]
