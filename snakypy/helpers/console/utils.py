# TODO: DEPRECATED
# def check_fg_bg_sgr(FG, BG, SGR, foreground, background, sgr) -> None:
#     """
#     Checks if the attributes of the functions that the foreground
#     and background parameters are in accordance with their respective class.
#     """
#
#     if foreground and foreground not in FG.__dict__.values():
#         raise AttributeError(
#             'Attribute invalid in parameter "foreground". Must receive from FG class.'
#         )
#     if background and background not in BG.__dict__.values():
#         raise AttributeError(
#             'Attribute invalid in parameter "background". Must receive from BG class.'
#         )
#     if sgr and sgr not in SGR.__dict__.values():
#         raise AttributeError(
#             'Attribute invalid in parameter "sgr". Must receive from SGR class.'
#         )
