"""Tests for `snakypy` package."""
from getpass import getpass

import pytest
import os
import snakypy
from contextlib import suppress
from unittest import TestCase
from os.path import join, exists
from sys import platform
from unittest.mock import patch
from snakypy.helpers.utils.decorators import only_linux, silent_errors
from snakypy.helpers.files import create_file, backup_file, read_file
from snakypy.helpers.files import create_json
from snakypy.helpers.files import read_json
from snakypy.helpers.files import update_json
from snakypy.helpers.os import cleaner, systemctl_is_active, remove_objects
from snakypy.helpers.catches import shell, extension
from snakypy.helpers import printer, FG, BG, SGR
from snakypy.helpers.calcs import percentage, fibonacci, compound_interest, simple_interest
from snakypy.helpers.path import create as create_path
from snakypy.helpers.os import rmdir_blank
from snakypy.helpers.calcs import bmi
from snakypy.helpers.console import cmd
from snakypy.helpers.catches.finders import find_objects, is_tool, tools_requirements
from snakypy.helpers.os import super_command


def test_version():
    assert snakypy.helpers.__info__["version"] == "0.1.0"


@pytest.fixture
def base(tmpdir):
    tmp = tmpdir.mkdir("temporary")
    files = ["file.txt", "file.json"]
    content = """Snakypy"""
    return {"tmp": tmp, "files": files, "content": content}


def test_create_file(base):
    forced = create_file(base["content"], join(base["tmp"], base["files"][0]), force=True)
    assert forced is True
    with pytest.raises(FileExistsError):
        assert create_file(base["content"], join(base["tmp"], base["files"][0]), force=False)

    return forced


def test_decorators():
    @only_linux
    def get_shell():
        return shell()

    assert get_shell() in ["sh", "zsh", "bash", "fish", "ion", "elvish", "tcsh"]


def test_backup_copy_and_error(base):
    create_file(base["files"][0], join(base["tmp"], base["files"][0]), force=True)
    backup_file(join(base["tmp"], base["files"][0]), join(base["tmp"], base["files"][0]), date=True)
    with pytest.raises(FileNotFoundError):
        cleaner(base["tmp"], "*.txt")


def test_error_extension_create_json(base):
    content = {"Hello": "World!"}
    with pytest.raises(Exception):
        assert create_json(content, join(base["tmp"], base["files"][0]))  # file.txt


def test_cleaner_not_found_object(base):
    with pytest.raises(FileNotFoundError):
        cleaner(base["tmp"], "foo.txt")


def test_is_tool():
    if not is_tool("ls"):
        assert False
    if not is_tool("ls__"):
        assert True


def test_tools_requirements():
    if not tools_requirements("ls"):
        assert False
    with suppress(FileNotFoundError):
        tools_requirements("ls__")


# def test_super_command(base):
#     test_create_file(base)
#     path = join(base["tmp"], base["files"][0])
#     super_command(f"chmod 000 {path}")
#     with pytest.raises(PermissionError):
#         read_file(path)


def test_systemctl_is_active():
    ret = systemctl_is_active("systemd-udevd.service")
    if "inactive" or "active" in ret[0]:
        assert True


def test_remove_objects(base):
    test_create_file(base)
    os.mkdir(join(base["tmp"], "temp_dir"))
    obj = (join(base["tmp"], base["files"][0]), join(base["tmp"], "temp_dir"))
    remove_objects(objects=obj)
    if not exists(join(base["tmp"], "temp_dir")) and not exists(join(base["tmp"], base["files"][0])):
        assert True
    else:
        assert False


@silent_errors
def test_silent_errors():
    assert 1 != 1


def test_fibonacci():
    assert fibonacci(50) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fibonacci(50, ret_text=True) == '0 1 1 2 3 5 8 13 21 34'


def test_compound_interest():
    assert compound_interest(2455, 12, 1) == {'amount': 2766.36, 'fess': 311.36}
    assert compound_interest(2455, 12, 1, ret_text=True) == 'The amount was: $ 2766.36. The fees were: $ 311.36.'


def test_simple_interest():
    assert simple_interest(2455, 12, 1) == {'amount': 2749.6, 'fess': 294.6}
    assert simple_interest(2455, 12, 1, ret_text=True) == 'The amount was: $ 2749.60. The fees were: $ 294.60.'


def test_cleaner_successfully(base):
    if test_create_file(base):
        ret = cleaner(base["tmp"], base["files"][0])
        if isinstance(ret, int):
            assert True
        else:
            assert False


def test_printer_return():
    val = printer("Hello, World!", ":D", foreground=FG.BLACK, background=BG.WHITE, sgr=SGR.UNDERLINE)
    assert val[0] == "Hello, World!"
    assert val[1] == ":D"


def test_create_json(base):
    content = {"Hello": "World!"}
    forced = create_json(content, join(base["tmp"], base["files"][1]), force=True)
    assert forced is True
    with pytest.raises(Exception):
        create_json(content, join(base["tmp"], base["files"][1]))


def test_read_json(base):
    test_create_json(base)  # Created
    data = read_json(join(base["tmp"], base["files"][1]))
    assert data['Hello'] == 'World!'


def test_update_json(base):
    test_create_json(base)  # Created
    data = read_json(join(base["tmp"], base["files"][1]))
    data['Hello'] = 'Terra!'
    assert update_json(join(base["tmp"], base["files"][1]), data) is True


def test_find_extension(base):
    filepath = join(base["tmp"], base["files"][0])
    json_path = join(base["tmp"], base["files"][1])
    test_create_file(base)
    data = find_objects(base["tmp"], by_extension=("txt", "json"))
    assert filepath in data["by_extension"]
    test_create_json(base)
    data = find_objects(base["tmp"], by_extension=("json",))
    assert filepath not in data["by_extension"]
    assert json_path in data["by_extension"]


def test_find_files(base):
    test_create_file(base)
    test_create_json(base)
    data = find_objects(base["tmp"], files=("file.txt", "file.json"))
    assert join(base["tmp"], base["files"][0]) in data["files"]
    assert join(base["tmp"], base["files"][1]) in data["files"]


def test_create_json_exists(base):
    content = {"Hello": "World!"}
    test_create_json(base)
    with pytest.raises(FileExistsError):
        assert create_json(content, join(base["tmp"], base["files"][1]))


def test_read_json_error(base):
    with pytest.raises(FileNotFoundError):
        assert read_json(join(base["tmp"], base["files"][1]))


def test_update_json_not_found(base):
    with pytest.raises(FileNotFoundError):
        data = read_json(join(base["tmp"], base["files"][1]))
        data['Hello'] = 'Marte!'
        assert update_json(join(base["tmp"], base["files"][1]), data)


def test_get_shell():
    if not platform.startswith('win'):
        shells = ['bash', 'zsh', 'sh', 'ksh']
        assert shell() in shells


def test_percentage():
    perc = 5  # 5%
    whole = 120
    result_v = percentage(perc, whole)
    result_sum = percentage(5, 120, operation='+')
    result_sub = percentage(5, 120, operation='-')
    result_log_sum = percentage(5, 120, operation='+', log=True)
    result_log_sub = percentage(5, 120, operation='-', log=True)
    assert result_v == 6.0
    assert result_sum == 126.0
    assert result_sub == 114.00
    assert result_log_sum == f'>> {whole} + {perc}% = 126.00'
    assert result_log_sub == f'>> {whole} - {perc}% = 114.00'


def test_file_extension():
    with pytest.raises(TypeError):
        file = 'None'
        assert extension(file) == '.txt'
    file = '/home/file.tar.gz'
    assert extension(file) == '.gz'
    assert extension(file, dots=True) == 'tar.gz'


def test_command_real_time():
    assert cmd('ls', ret=True, verbose=True) == 0


def test_imc():
    with pytest.raises(AttributeError):
        bmi('M', -70, 1.70)
        bmi('F', 70, -1.70)
        bmi('Male', 70, 1.70)
        bmi('M', 70, 4.00)
        bmi('F', 0, 0)
        bmi('F', 350, 1.50)
        bmi('', 70, 1.70)
    result = bmi('M', 70, 1.73)
    assert result == 'Normal weight.'
    result = bmi('m', 59.2, 1.80)
    assert result == 'Under weight.'
    result = bmi('m', 82.4, 1.69)
    assert result == 'Overweight.'
    result = bmi('m', 90.1, 1.62)
    assert result == 'Obesity.'
    result = bmi('f', 69.5, 1.68)
    assert result == 'Normal weight.'
    result = bmi('f', 45.1, 1.71)
    assert result == 'Under weight.'
    result = bmi('f', 83.7, 1.67)
    assert result == 'Overweight.'
    result = bmi('f', 83.7, 1.58)
    assert result == 'Obesity.'


def test_rmdir_blank(base):
    paths = (os.path.join(base["tmp"], "foo"), os.path.join(base["tmp"], "bar"))
    create_path(*paths)
    for path in paths:
        assert os.path.isdir(path) is True
    rmdir_blank(base["tmp"])
    for path in paths:
        assert os.path.isdir(path) is False


class TestBakeProject(TestCase):
    @patch('snakypy.helpers.console.pick', return_value='python')
    def test_pick_no_index(self, fn):
        title = 'What is your favorite programming language?'
        options = ['C', 'C++', 'Java', 'Javascript', 'Python', 'Ruby']
        self.assertEqual(fn(title, options), 'python')

    @patch('snakypy.helpers.console.pick', return_value=(5, 'python'))
    def test_pick_with_index(self, fn):
        title = 'What is your favorite programming language?'
        options = ['C', 'C++', 'Java', 'Javascript', 'Python', 'Ruby']
        self.assertEqual(fn(title, options, index=True), (5, 'python'))
        with pytest.raises(AssertionError):
            self.assertEqual(fn(title, options, index=True), (5, 'python3'))

    @patch('snakypy.helpers.entry', return_value="Snakypy")
    def test_entry_set_reply(self, fn):
        self.assertEqual(fn("What's your name?"), "Snakypy")

    @patch('snakypy.helpers.entry', autospec=True)
    def test_entry_not_set_question(self, fn):
        with pytest.raises(TypeError):
            fn()
