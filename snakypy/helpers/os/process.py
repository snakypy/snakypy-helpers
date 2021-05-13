from subprocess import Popen, PIPE
from typing import Union, Optional
from snakypy.helpers.console import printer
from snakypy.helpers.ansi import FG
from snakypy.helpers.utils.decorators import only_linux
from getpass import getpass


@only_linux
def super_command(command: str) -> Union[Optional[str], None]:
    """
        Allows to execute superuser command in shell.

        >>> from snakypy.helpers.os import super_command
        >>> super_command("python --version | cut -d' ' -f1")
        ''

    Args:
        command (str): The command statement to be executed.

    Returns:
        [str]: Returns the result of the command if it has.
    """
    try:
        while True:
            super_password = getpass()
            command_str = f"su -c '{command}';"
            p = Popen(
                command_str,
                stdin=PIPE,
                stderr=PIPE,
                stdout=PIPE,
                universal_newlines=True,
                shell=True,
            )
            communicate = p.communicate(super_password)

            if "failure" not in communicate[1].split():
                return communicate[0]
            printer("Password incorrect.", foreground=FG.WARNING)
    except KeyboardInterrupt:
        printer("Aborted by user.", foreground=FG.WARNING)
        return None


@only_linux
def systemctl_is_active(service: str) -> Union[tuple, None]:
    """
        Checks whether a service is active or inactive in the operating system through SystemD.

        >>> from snakypy.helpers.os import systemctl_is_active
        >>> systemctl_is_active("systemd-udevd.service")
        ('active', None)

    Args:
        service (str): You must inform the name of the service, with its extension. Example: cronie.service

    Returns (str|None): It will return a tuple with error output and output or None if the SystemD is not found.

    """
    try:
        process = Popen(
            ["systemctl", "is-active", service], stdout=PIPE, universal_newlines=True
        )
        output, err = process.communicate()
        return output.replace("\n", ""), err
    except FileNotFoundError:
        printer("The system does not support SystemD.", foreground=FG.ERROR)
        return None


__all__ = ["super_command", "systemctl_is_active"]
