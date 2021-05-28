import sys
import time
from datetime import date
from typing import Any, Union

from snakypy.helpers.ansi import BG, FG, NONE, SGR
from snakypy.helpers.decorators import denying_os


@denying_os("nt")
def printer(
    *args: str,
    foreground: str = "",
    background: str = "",
    sgr: str = "",
    sep: str = " ",
    end: str = "\n",
    file: Any = None,
    flush: bool = False,
) -> tuple:
    """A function that allows you to print colored text on the terminal.

    >>> from snakypy.helpers import printer, FG, BG, SGR
    >>> printer('Hello, World!', foreground=FG().BLACK, background=BG().WHITE, sgr=SGR.UNDERLINE)
    Hello, World!
    ('Hello, World!',)
    >>> printer('Hello, World!', foreground=FG().MAGENTA, sgr=SGR.UNDERLINE)
    Hello, World!
    ('Hello, World!',)
    >>> printer('Not found', foreground=FG(error_icon="[x]").ERROR, sgr=SGR.UNDERLINE)
    Not found
    ('Not found',)
    >>> printer('Not found', foreground=BG(error_icon="[x]").ERROR, sgr=SGR.BOLD)
    Not found
    ('Not found',)

    Args:
        foreground (str): This named argument should optionally receive an object of class "snakypy.ansi.FG" for
                          the foreground color of the text. This object will be text with ansi code.

        background (str): This named argument should optionally receive an object of class "snakypy.ansi.BG" for
                          the background color of the text. This object will be text with ansi code.

        sgr (str): This named argument should optionally receive an object of class "snakypy.ansi.SGR" for the effect
                     of the text. This object will be text with ansi code.

        sep (str): Separator between printer function objects.

        end (str): Responsible for skipping a line after printing is finished.

        file (Any):

        flush (bool):
    """

    #  TODO: DEPRECATED
    # check_fg_bg_sgr(FG, BG, SGR, foreground, background, sgr)

    try:
        lst = []
        for i in range(len(args)):
            lst.append(args[i])
        text = " ".join(map(str, lst))

        print(
            f"{NONE}{sgr}{foreground}{background}{text}{NONE}",
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )
        return args
    except AttributeError:
        raise AttributeError("Invalid parameter passed")


@denying_os("nt")
def entry(
    text,
    *,
    foreground: str = "",
    background: str = "",
    sgr: str = "",
    jump_line: str = "\n> ",
) -> str:
    """
        This function is derived from the input, but with the option of
        coloring it and some different formatting.
        Note: If you use Windows, the coloring option will not work.

    >>> from snakypy.helpers import entry, FG
    >>> entry("What's your name?", foreground=FG().QUESTION)
    ➜ What's your name?
    > 'snakypy'
    >>> entry("What's your name?", foreground=FG().BLUE)
    ➜ What's your name?
    > 'snakypy'
    >>> entry("What's your name?", foreground=FG().GREEN)
    ➜ What's your name?
    > 'snakypy'

    Args:
        text (object): Argument must receive an object

        foreground (str): This named argument should optionally receive \
                            an object of class "snakypy.helpers.ansi.FG" for the foreground \
                            color of the text. This object will be text with ansi code. \
                            (default: '')

        background (str):  This named argument should optionally receive \
                            an object of class "snakypy.helpers.ansi.BG" for the background \
                            color of the text. This object will be text with ansi code. \
                            (default: '')

        sgr (str): This named argument should optionally receive \
                         an object of class "snakypy.helpers.ansi.SGR" for the effect \
                         of the text. This object will be text with ansi code. \
                         (default: '')

        jump_line (str): Named argument that makes the action of skipping a line \
                           and adding a greater sign to represent an arrow. You change \
                           that argument to your liking. (default: '[bar]n> ') \

    """

    # TODO: DEPRECATED
    # check_fg_bg_sgr(FG, BG, SGR, foreground, background, sgr)

    try:
        return input(f"{NONE}{sgr}{foreground}{background}{text}{jump_line}{NONE}")
    except KeyboardInterrupt:
        print(f"\n{FG().WARNING} Aborted by user.{NONE}")
        return "Aborted by user."
    except TypeError:
        print(f"\n{FG().ERROR} Input value not defined.{NONE}")
        return "Input value not defined."


def pick_options(
    title: str,
    options: list,
    answer: str,
    *,
    colorful: bool = False,
    index: bool = False,
    lowercase: bool = False,
    ctrl_c_message: bool = False,
) -> Union[tuple[int, Any], bool, None]:
    if not colorful:
        FG().QUESTION = ""
        FG().GREEN = ""
        FG().MAGENTA = ""
        FG().CYAN = ""
        FG().ERROR = ""
        FG().WARNING = ""
    ctrl_c = "(Ctrl+C to Cancel)" if ctrl_c_message else ""
    printer(title, ctrl_c, foreground=FG().QUESTION)
    count = 1
    for option in options:
        print(f"{FG().GREEN}[{count}] {FG().MAGENTA}{option}{NONE}")
        count += 1
    try:
        pos = int(input(f"{FG().CYAN}{answer} {NONE}")) - 1
        assert pos > -1
        if index and lowercase:
            return pos, options[pos].lower()
        elif index and not lowercase:
            return pos, options[pos]
        if lowercase:
            return options[pos].lower()
        return options[pos]
    except IndexError:
        printer("Option invalid!", foreground=FG().ERROR)
        return False
    except KeyboardInterrupt:
        printer("Canceled by user.", foreground=FG().WARNING)
        return True


def pick(
    title: str,
    options: list,
    *,
    answer: str = "Answer:",
    index: bool = False,
    colorful: bool = False,
    lowercase: bool = False,
    ctrl_c_message: bool = False,
) -> Union[tuple[int, Any], bool, None]:
    """Function that creates a menu of options in the terminal.

    >>> from snakypy.helpers import pick
    >>> title_ = 'What is your favorite programming language?'
    >>> options_ = ['C', 'C++', 'Java', 'Javascript', 'Python', 'Ruby']
    >>> pick(title_, options_, lowercase=True)

    **output:**

    .. code-block:: shell

        What is your favorite programming language? (Ctrl+C to Cancel)
        [1] C
        [2] C++
        [3] Java
        [4] Javascript
        [5] Python
        [6] Ruby
        Answer: 5
        'python'

    Args:
        title (str): - You should receive a text that will be the \
                       title or the question with meaning in the alternatives.

        options (list): - You should receive a list with certain elements \
                          that will be part of the menu options.

        answer (str): -- The text that will be shown before entering the answer. \
                        You can change to your language. (default: {'Answer:'})

        index (bool): This argument for True, will return a tuple, where element 0, \
                        will be the index of the option that the user chose, and \
                        element 1 of the tuple, will be the name of the choice option. \
                        Remember that the indexing of the menu is not the same as the \
                        list of options because it starts with zero (0). \
                        (default: {False})

        colorful (bool): If it has True, the menu color will be active, but it only \
                           works if it is on a UNIX system, as the color uses Ansi Color. \
                           If have Windows, no effect will appear. \
                           (default: {False})

        lowercase (bool) If set to True, the text value returned from the chosen \
                            option will be lowercase.

        ctrl_c_message (bool): If you are in True value, it shows the text (Ctrl + C to Cancel) in the header.
    """

    if not type(options) is list:
        raise TypeError("You must enter a list in the argument: options")

    if len(title) == 0:
        raise TypeError("The title cannot contain an empty element. Approached.")

    for option in options:
        if len(option) == 0:
            raise TypeError("The list cannot contain an empty element. Approached.")

    try:
        while True:
            option = pick_options(
                title,
                options,
                answer=answer,
                index=index,
                colorful=colorful,
                lowercase=lowercase,
                ctrl_c_message=ctrl_c_message,
            )
            if option or option is None:
                break
        return option
    except Exception:
        raise Exception("An unexpected error occurs when using pick")


def billboard(
    text: str,
    foreground: str = "",
    background: str = "",
    ret_text: bool = False,
    justify: str = "auto",
) -> Union[str, tuple]:
    """
        Creates a Billboard in the terminal.

    >>> from snakypy.helpers.console import billboard
    >>> from snakypy.helpers import FG, BG
    >>> billboard('Hello, Snakypy!')
    >>> billboard('Hello, Snakypy!', foreground=FG().BLUE, background=BG().WHITE)

    Args:
        text (str): Any text must be informed.

        foreground (str): -- This named argument should optionally receive \
                            an object of class "snakypy.ansi.FG" for the foreground \
                            color of the text. This object will be text with ansi code. \
                            (default: '')

        background (str): This named argument should optionally receive \
                            an object of class "snakypy.ansi.BG" for the background \
                            color of the text. This object will be text with ansi code. \
                            (default: '')

        ret_text (bool): Receives a Boolean value. If the value is True, it will only \
                               return the text. If the value is False, it will resume printing.

        justify (str): -- Justify the position of the text: auto | center | right. \
                             (default: 'auto')

    Returns:
        [str]: The text informed in billboard form.
    """
    import pyfiglet

    banner = pyfiglet.figlet_format(text, justify=justify)
    if ret_text:
        return banner
    return printer(banner, foreground=foreground, background=background)


def credence(
    app_name: str,
    app_version: str,
    app_url: str,
    data: dict,
    foreground: str = "",
    column: int = 80,
) -> None:
    """
        Print project development credits.

    >>> from snakypy.helpers.console import credence
    >>> content = {
        "credence": [
            {
                "my_name": "William Canin",
                "email": "example@domain.com",
                "website": "http://williamcanin.github.io",
                "locale": "Brazil - SP"
            },
            {
                "my_name": "Maria",
                "email": "example@domain.com",
                "locale": "Brazil - SP"
            }
        ]
    }
    >>> credence('Snakypy', '0.1.0', 'https://github.com/snakypy/snakypy', content)

    **output:**

    .. code-block:: shell

        ---------------------------------------------------------
                       Snakypy - Version 0.1.0
        ---------------------------------------------------------

                              Credence:

                        My Name: William Canin
                      Email: example@domain.com
                   Website: http://williamcanin.me
                         Locale: Brazil - SP

                         My Name: Maria
                      Email: example@domain.com
                         Locale: Brazil - SP

        -----------------------------------------------------------------
                    Snakypy Helpers © 2021 - All Right Reserved.
                    Home: https://github.com/snakypy/snakypy-helpers
        -----------------------------------------------------------------

    Ars:
        app_name (str): Put application name.

        app_version (str): Application version.

        app_url (str): Application or website url.

        data (dict): You must receive a dictionary containing a key called "credence". E.g: data = {'credence': []}

        foreground (str): This named argument should optionally receive \
                            an object of class "snakypy.ansi.FG" for the foreground \
                            color of the text. This object will be text with ansi code. \
                            (default: '')

        column (int): Justify the position of the credits through the columns using an integer. (default: 80)
    """
    try:

        if type(data) is not dict:
            msg = (
                f'>>> The function "{credence.__name__}" '
                "must take a dictionary as an argument."
            )
            raise Exception(msg)

        printer(f'{57 * "-"}'.center(column), foreground=foreground)
        printer(
            f"{app_name} - Version {app_version}".center(column), foreground=foreground
        )
        printer(f'{57 * "-"}\n'.center(column), foreground=foreground)
        printer("Credence:\n".center(column), foreground=foreground)
        for item in data["credence"]:
            for key, value in item.items():
                printer(
                    f'{key.title().replace("_", " ")}: {value}'.center(column),
                    foreground=foreground,
                )
            print()
        printer(f'{57 * "-"}'.center(column), foreground=foreground)
        printer(
            f"{app_name} © {date.today().year} - All Right Reserved.".center(column),
            foreground=foreground,
        )
        printer(f"Home: {app_url}".center(column), foreground=foreground)
        printer(f'{57 * "-"}'.center(column), foreground=foreground)
    except KeyError:
        msg = (
            "The 'credence' key was not found."
            "Enter a dictionary containing a 'credits' key."
        )
        raise KeyError(msg)


def loading(
    set_time: float = 0.030,
    bar: bool = False,
    header: str = "[Loading]",
    foreground: str = "",
) -> None:
    """
    Function will show animated logging in percentage and bar style.

    >>> from snakypy.helpers.console import loading
    >>> loading()
    >>> loading(set_time=0.20, bar=True)

    set_time (float): Time when the animation will last. (default: {0.030})

    bar (bool): If True, the animation will be barred and not percentage. (default: {False})

    header (str): Modifies the animation header (default: {'[Loading]'})
    """
    printer(header, foreground=foreground)
    try:
        if bar:
            for i in range(0, 100):
                time.sleep(set_time)  # 5 seconds
                width = (i + 1) / 4
                bar_ = f"[{'#' * int(width)}{' ' * (25 - int(width))}]"
                sys.stdout.write("\u001b[1000D" + bar_)
                sys.stdout.flush()
            print()
            return
        for i in range(0, 100):
            time.sleep(set_time)
            sys.stdout.write("\u001b[1000D")
            sys.stdout.flush()
            # time.sleep(0.1)
            sys.stdout.write(f"{str(i + 1)}%")
            sys.stdout.flush()
        print()
        return
    except KeyboardInterrupt:
        printer("\nCanceled by user.", foreground=FG().WARNING)
        return


__all__ = ["pick", "entry", "printer", "billboard", "credence", "loading"]
