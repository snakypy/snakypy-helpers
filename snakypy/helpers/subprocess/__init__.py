from getpass import getpass
from subprocess import PIPE, Popen
from typing import Any, Optional, Union

from snakypy.helpers.ansi import FG, NONE
from snakypy.helpers.console import printer
from snakypy.helpers.decorators import only_linux


# The use of static typing in this function in conjunction with "inter", caused
# errors when using Mypy, perhaps because at run time the inter would always return None,
# so it is recommended in the file mypy.ini, to use the option "strict_optional = False".
# Ref: https://stackoverflow.com/questions/57350490/mypy-complaining-that-popen-stdout-does-not-have-a-readline
def command(
    cmd: str,
    *args: Any,
    shell: bool = True,
    universal_newlines: bool = True,
    ret: bool = False,
    verbose: bool = False,
) -> int:
    """
        Function that uses the subprocess library with Popen.
        The function receives a command as an argument and shows
        execution in real time.

        >>> from snakypy.helpers.subprocess import command
        >>> url = 'git clone https://github.com/snakypy/snakypy.git'
        >>> command(url, verbose=True)

    Args:
        universal_newlines (bool):

        cmd (str): Must inform the command to be executed.

        shell (bool): Receives a Boolean value. If it has False, the command must be in list where
                            the command space is split. **E.g:** ['ls', '/bin']. If the value is True, the command
                            can be stored in a string normal. **E.g:** 'ls /bin'

        ret (bool): The default value is False, however if it is set to True it will \
                      return a code status of the command output, where the code 0 (zero), \
                      is output without errors. \

        verbose (bool): The default value is False, if you change it to True, the command \
                          will show in real time the exit at the terminal, if there is an exit. \
    Returns:
        A negative integer will return if everything is right, or the value of the process.
    """
    process = Popen(
        cmd, shell=shell, stdout=PIPE, universal_newlines=universal_newlines
    )
    if verbose:
        for line in iter(process.stdout.readline, ""):
            print(NONE, *args, line.rstrip(), NONE)
    if ret:
        return process.poll()
    return -1


@only_linux
def super_command(cmd: str) -> Union[Optional[str], None]:
    """
        Allows to execute superuser command in shell.

        >>> from snakypy.helpers.subprocess import super_command
        >>> super_command("python --version | cut -d' ' -f1")
        ''

    Args:
        cmd (str): The command statement to be executed.

    Returns:
        [str]: Returns the result of the command if it has.
    """
    try:
        while True:
            super_password = getpass()
            command_str = f"su -c '{cmd}';"
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
            printer("Password incorrect.", foreground=FG().WARNING)
    except KeyboardInterrupt:
        printer("Aborted by user.", foreground=FG().WARNING)
        return None


@only_linux
def systemctl_is_active(service: str) -> Union[tuple, None]:
    """
        Checks whether a service is active or inactive in the operating system through SystemD.

        >>> from snakypy.helpers.subprocess import systemctl_is_active
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
        printer("The system does not support SystemD.", foreground=FG().ERROR)
        return None


__all__ = ["command", "super_command", "systemctl_is_active"]
