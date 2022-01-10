"""
Snakypy Helpers
~~~~~~~~~~~~~~~~

Snakypy Helpers is a package that contains code ready to assist in the
development of Snakypy projects, so as not to replicate the code.


For more information, access: 'https://github.com/snakypy/snakypy-helpers'

:copyright: Copyright 2020-2021 by Snakypy team, see AUTHORS.rst.
:license: MIT license, see LICENSE for details.
"""
from os.path import abspath, dirname, join

import snakypy.helpers.ansi  # noqa: F401
import snakypy.helpers.calcs
import snakypy.helpers.catches
import snakypy.helpers.console
import snakypy.helpers.decorators
import snakypy.helpers.files
import snakypy.helpers.os
import snakypy.helpers.path  # noqa: F401
from snakypy.helpers.ansi import BG, FG, NONE, SGR  # noqa: F401
from snakypy.helpers.console import entry, pick, printer  # noqa: F401
from snakypy.helpers.files import eqversion

__info__ = {
    "name": "Snakypy Organization",
    "package": "snakypy",
    "email": "contact.snakypy@gmail.com",
    "website": "https://snakypy.github.io",
    "github": "https://github.com/snakypy",
    "version": "0.3.1",
}

# Keep the versions the same on pyproject.toml and __init__.py
pyproject = join(dirname(abspath(__file__)), "../..", "pyproject.toml")
eqversion(pyproject, __info__["version"])
