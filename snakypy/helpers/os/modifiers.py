import platform
from contextlib import suppress
from os.path import join


def wtm_state(value: str = "enabled") -> None:
    """
        [Windows Task Manager State]
        Enable or disable Windows task manager

        .. code-block:: python

            from snakypy.helpers.os import wtm_state
            wtm_state(state="disable")


    Args:
        value (str): If "disabled", disable task manager, if "enabled" enable

    Returns:
        None
    """

    if platform.system() == "Windows":

        types = {"enabled": 0, "disabled": 1}

        if value not in types.keys():
            raise TypeError(
                f'Invalid type "{value}" in function "{wtm_state.__name__}". Use "enabled" or "disabled".'
            )

        with suppress(ModuleNotFoundError, PermissionError, TypeError):
            import winreg

            key = join(
                "SOFTWARE",
                "Microsoft",
                "Windows",
                "CurrentVersion",
                "Policies",
                "System",
            )
            subkey = "DisableTaskMgr"

            regkey = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key,
                0,
                winreg.KEY_WRITE,
            )
            # 1 = Disabled, 0 = Enabled
            value_ = types["disabled"] if value == "disabled" else types["enabled"]
            winreg.SetValueEx(regkey, subkey, 0, winreg.REG_DWORD, value_)
            winreg.CloseKey(regkey)


__all__ = ["wtm_state"]
