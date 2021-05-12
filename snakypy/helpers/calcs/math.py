from typing import Union


def percentage(
    per: float, whole: float, *, operation: str = "", log: bool = False
) -> Union[float, str]:
    """
    This function will calculate a whole with a certain percentage value.

    >>> from snakypy.helpers.calcs import percentage
    >>> percentage(25, 500)
    >>> percentage(25, 500, log=True)
    >>> percentage(25, 500, operation='+')
    >>> percentage(25, 500, operation='-')
    >>> percentage(25, 500, operation='+', log=True)
    >>> percentage(25, 500, operation='-', log=True)

    **output:**

    .. code-block:: shell

        125
        '>> 25% of 500 = 125.00'
        625.00
        375.00
        '>> 500 + 25% = 625.00'
        '>> 500 - 25% = 375.00'

    Arguments:

        **per {float}** -- Input argument that should receive a float representing \
                       a certain percentage value.

        **whole {float}** -- Input argument that should receive a float representing \
                         total value.

    Keyword Arguments:

        **operation {str}** -- This named parameter must receive two types of string \
                           values. One is the plus sign ('+') that will add the total \
                           to the imposed percentage. The other is the minus sign ('-'), \
                           which subtracts the total value from the imposed percentage \
                           value. (default: {None})

        **log {bool}** -- If this parameter is of the value True, then the return will be \
                     a custom string with the percent signs and the operation. \
                     (default: {False})
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


def fibonacci(num: int, *, ret_text=False) -> Union[list, str]:
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
    ret_dict=True,
    ret_text=False,
) -> Union[tuple, dict, str, bool]:
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
    return False


def compound_interest(
    capital: float,
    application_time: float,
    fess: float,
    *,
    ret_dict=True,
    ret_text=False,
) -> Union[tuple, dict, str, bool]:
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
    return False


__all__ = ["percentage", "fibonacci", "compound_interest", "simple_interest"]
