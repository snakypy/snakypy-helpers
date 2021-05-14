def check_fg_bg_sgr(FG, BG, SGR, *args) -> None:
    """
    Checks if the attributes of the functions that the foreground
    and background parameters are in accordance with their respective class.
    """

    if args[0] and args[0] not in FG.__dict__.values():
        raise AttributeError(
            'Attribute invalid in parameter "foreground". Must receive from FG class.'
        )
    if args[1] and args[1] not in BG.__dict__.values():
        raise AttributeError(
            'Attribute invalid in parameter "background". Must receive from BG class.'
        )
    if args[2] and args[2] not in SGR.__dict__.values():
        raise AttributeError(
            'Attribute invalid in parameter "sgr". Must receive from SGR class.'
        )
