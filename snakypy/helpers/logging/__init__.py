import logging
from typing import Any

from snakypy.helpers import FG, NONE


class Log:
    def __init__(self, filename, datefmt="%m/%d/%Y %I:%M:%S %p"):
        self.filename = filename
        self.date_format = datefmt
        self.formatted = "%(levelname)s:[%(asctime)s]:%(message)s"

        if not self.filename:
            raise ValueError("Enter the filename parameter. Aborted.")

        self.levels = {
            "exception": logging.exception,
            "info": logging.info,
            "warning": logging.warning,
            "error": logging.error,
            "debug": logging.debug,
            "critical": logging.critical,
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def record(
        self,
        text: str,
        *args: Any,
        exc_info=True,
        level: str = "exception",
        colorize: bool = False,
        **kwargs: Any,
    ) -> None:
        """
            Function to write logs to a text file.

        .. code-block:: python

            from snakypy.helpers.logging import Log
            log = Log(filename="/tmp/mylogs.log")
            log.record("Hello", level="info", colorize=True)

        Args:
            text (str): You should receive a message that will be generated in the log.

            \*args: Specifies other desirable arguments.

            exc_info (bool): If True, specifies exception information.

            level (str): Must inform the log messages to be used. They are: exception, info, warning
            error, debug, critical.

            colorize (bool): Prints the colored log if using the terminal.

            \**kwargs: Specific dictionaries.

        Returns: None
        """
        for item in self.levels.keys():
            if item == level:
                if colorize:
                    if item == "warning":
                        self.formatted = (
                            f"{FG().YELLOW}%(levelname)s:{FG().GREEN}[%(asctime)s]"
                            f"{NONE}:%(message)s"
                        )
                    elif item == "error" or item == "exception":
                        self.formatted = (
                            f"{FG().RED}%(levelname)s:{FG().GREEN}[%(asctime)s]"
                            f"{NONE}:%(message)s"
                        )
                    else:
                        self.formatted = f"{FG().CYAN}%(levelname)s:{FG().GREEN}[%(asctime)s]{NONE}:%(message)s"
                # Set basic configuration logs
                logging.basicConfig(
                    filename=self.filename,
                    format=self.formatted,
                    datefmt=self.date_format,
                    level=logging.INFO,
                )

                # Verify message exception or not
                if item == "exception":
                    return self.levels[item](text, *args, exc_info=exc_info, **kwargs)
                else:
                    return self.levels[item](text, *args, **kwargs)

        raise ValueError(
            f'Error implementing the method "{self.record.__name__}" in class Log.'
        )


__all__ = ["Log"]
