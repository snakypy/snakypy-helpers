from typing import Union


def percentage(
    per: float, whole: float, *, operation: str = "", log: bool = False
) -> Union[float, str]:
    """
        This function will calculate a whole with a certain percentage value.

        >>> from snakypy.helpers.calcs import percentage
        >>> percentage(25, 500)
        125.0
        >>> percentage(25, 500, log=True)
        '>> 25% of 500 = 125.00'
        >>> percentage(25, 500, operation='+')
        625.0
        >>> percentage(25, 500, operation='-')
        375.0
        >>> percentage(25, 500, operation='+', log=True)
        '>> 500 + 25% = 625.00'
        >>> percentage(25, 500, operation='-', log=True)
        '>> 500 - 25% = 375.00'

    Args:
        per (float): Input argument that should receive a float representing a certain percentage value.

        whole (float): Input argument that should receive a float representing total value.

        operation: This named parameter must receive two types of string \
                           values. One is the plus sign ('+') that will add the total \
                           to the imposed percentage. The other is the minus sign ('-'), \
                           which subtracts the total value from the imposed percentage \
                           value. (default: "")

        log (bool):  If this parameter is of the value True, then the return will be \
                     a custom string with the percent signs and the operation. \
                     (default: {False})

    Returns:

    """
    try:
        option = {
            "+": lambda: whole + (whole * (per / 100)),
            "-": lambda: whole - (whole * (per / 100)),
        }.get(operation, lambda: whole * (per / 100))()

        if log:
            if operation == "+":
                return f">> {whole} + {per}% = {option:.2f}"
            elif operation == "-":
                return f">> {whole} - {per}% = {option:.2f}"
            return f">> {per}% of {whole} = {option:.2f}"
        return option
    except AttributeError:
        raise AttributeError("Invalid parameter passed")


def fibonacci(num: int, *, ret_text: bool = False) -> Union[list, str]:
    """
        Generates the sequence of Fibonacci

        >>> from snakypy import helpers
        >>> helpers.calcs.fibonacci(50)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        >>> helpers.calcs.fibonacci(50, ret_text=True)
        '0 1 1 2 3 5 8 13 21 34'

    Args:
        num (int):  It should pass a positive whole number than zero.

        ret_text (bool): If the TRUE option returns the form sequence in the opposite
                             case in the form of a list. Default: False

    Returns:
        Returns a list or a string depending on the value of the **ret_text**.
    """
    previous_, next_ = 0, 0
    fib = []
    while next_ < num:
        fib.append(next_)
        next_ = next_ + previous_
        previous_ = next_ - previous_
        if next_ == 0:
            next_ = next_ + 1
    if ret_text:
        return " ".join(str(n) for n in fib)
    return fib


def simple_interest(
    capital: float,
    application_time: float,
    fess: float,
    *,
    ret_dict: bool = False,
    ret_text: bool = False,
) -> Union[tuple, dict, str]:
    """
        Function to apply simple interest.

        >>> from snakypy import helpers
        >>> helpers.calcs.simple_interest(2455, 12, 1)
        {'amount': 2749.6, 'fess': 294.6}
        >>> helpers.calcs.simple_interest(2455, 12, 1, ret_text=True)
        'The amount was: $ 2749.60. The fees were: $ 294.60.'

    Args:
        capital (float): Capital value

        application_time (float): Time if applications

        fess (float): Value fees

        ret_dict (bool): If it is True returns in the dictionary form

        ret_text (bool): If it is True returns in the dictionary text

    Returns:
        Returns dictionary or a string or both. Default dictionary.
    """
    fess_value = capital * (fess / 100) * application_time
    amount = capital + fess_value
    format_text = f"The amount was: $ {amount:.2f}. The fees were: $ {fess_value:.2f}."
    format_dict = {"amount": float(f"{amount:.2f}"), "fess": float(f"{fess_value:.2f}")}
    if ret_dict and ret_text:
        return format_dict, format_text
    elif ret_text:
        return format_text
    elif ret_dict:
        return format_dict
    return format_dict


def compound_interest(
    capital: float,
    application_time: float,
    fess: float,
    *,
    ret_dict=False,
    ret_text=False,
) -> Union[tuple, dict, str]:
    """
        Function to apply compound interest.

        >>> from snakypy import helpers
        >>> helpers.calcs.compound_interest(2455, 12, 1)
        {'amount': 2766.36, 'fess': 311.36}
        >>> helpers.calcs.compound_interest(2455, 12, 1, ret_text=True)
        'The amount was: $ 2766.36. The fees were: $ 311.36.'

    Args:
        capital (float): Capital value

        application_time (float): Time if applications

        fess (float): Value fees

        ret_dict (bool): If it is True returns in the dictionary form

        ret_text (bool): If it is True returns in the dictionary text

    Returns:
        Returns dictionary or a string or both.
    """
    amount = capital * ((1 + fess / 100) ** application_time)
    fess_value = amount - capital
    format_text = f"The amount was: $ {amount:.2f}. The fees were: $ {fess_value:.2f}."
    format_dict = {"amount": float(f"{amount:.2f}"), "fess": float(f"{fess_value:.2f}")}
    if ret_dict and ret_text:
        return format_dict, format_text
    elif ret_text:
        return format_text
    elif ret_dict:
        return format_dict
    return format_dict


__all__ = ["percentage", "fibonacci", "compound_interest", "simple_interest"]
