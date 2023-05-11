import os
from modules.utils import ExitException, clear_screen, is_windows, clear_screen_windows, clear_screen_unix

def test_exit_exception():
    try:
        raise ExitException()
    except ExitException:
        pass

def test_is_windows(mocker):
    mocker.patch('os.name', 'nt')
    assert is_windows() == True

    mocker.patch('os.name', 'posix')
    assert is_windows() == False

def test_clear_screen_windows(mocker):
    mocker.patch('your_module.is_windows', return_value=True)
    mocker.patch('os.system')
    clear_screen()
    os.system.assert_called_once_with('cls')

def test_clear_screen_unix(mocker):
    mocker.patch('your_module.is_windows', return_value=False)
    mocker.patch('os.system')
    clear_screen()
    os.system.assert_called_once_with('clear')

def test_clear_screen_windows_direct(mocker):
    mocker.patch('os.system')
    clear_screen_windows()
    os.system.assert_called_once_with('cls')

def test_clear_screen_unix_direct(mocker):
    mocker.patch('os.system')
    clear_screen_unix()
    os.system.assert_called_once_with('clear')