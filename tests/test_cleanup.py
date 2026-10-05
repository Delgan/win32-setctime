from types import SimpleNamespace

import pytest

from win32_setctime import _setctime


@pytest.fixture
def api(monkeypatch):
    calls = []
    monkeypatch.setattr(_setctime, "SUPPORTED", True)
    monkeypatch.setattr(
        _setctime,
        "wintypes",
        SimpleNamespace(
            HANDLE=lambda value: SimpleNamespace(value=value),
            BOOL=bool,
            FILETIME=lambda low, high: (low, high),
        ),
        raising=False,
    )
    monkeypatch.setattr(_setctime, "byref", lambda value: value, raising=False)
    monkeypatch.setattr(_setctime, "get_last_error", lambda: 5, raising=False)
    monkeypatch.setattr(
        _setctime, "WinError", lambda code: OSError(code, "test error"), raising=False
    )
    monkeypatch.setattr(_setctime, "CreateFileW", lambda *args: 42, raising=False)
    monkeypatch.setattr(_setctime, "SetFileTime", lambda *args: True, raising=False)
    monkeypatch.setattr(
        _setctime,
        "CloseHandle",
        lambda handle: calls.append(handle.value) or True,
        raising=False,
    )
    return calls


def test_failed_setfiletime_closes_handle(monkeypatch, api):
    monkeypatch.setattr(_setctime, "SetFileTime", lambda *args: False)
    with pytest.raises(OSError) as error:
        _setctime.setctime("test.txt", 0)
    assert error.value.errno == 5
    assert api == [42]


def test_success_closes_handle_once(api):
    _setctime.setctime("test.txt", 0)
    assert api == [42]


def test_cleanup_cannot_overwrite_original_windows_error(monkeypatch, api):
    last_error = [5]
    monkeypatch.setattr(_setctime, "SetFileTime", lambda *args: False)
    monkeypatch.setattr(_setctime, "get_last_error", lambda: last_error[0])

    def close(handle):
        api.append(handle.value)
        last_error[0] = 6
        return False

    monkeypatch.setattr(_setctime, "CloseHandle", close)
    with pytest.raises(OSError) as error:
        _setctime.setctime("test.txt", 0)
    assert error.value.errno == 5
    assert api == [42]


def test_close_failure_after_success_is_reported(monkeypatch, api):
    def close(handle):
        api.append(handle.value)
        return False

    monkeypatch.setattr(_setctime, "CloseHandle", close)
    with pytest.raises(OSError) as error:
        _setctime.setctime("test.txt", 0)
    assert error.value.errno == 5
    assert api == [42]


def test_invalid_file_handle_is_not_closed(monkeypatch, api):
    monkeypatch.setattr(_setctime, "CreateFileW", lambda *args: -1)
    with pytest.raises(OSError):
        _setctime.setctime("test.txt", 0)
    assert api == []


def test_setfiletime_exception_closes_handle(monkeypatch, api):
    original_error = RuntimeError("SetFileTime call failed")

    def fail(*args):
        raise original_error

    monkeypatch.setattr(_setctime, "SetFileTime", fail)
    with pytest.raises(RuntimeError) as error:
        _setctime.setctime("test.txt", 0)
    assert error.value is original_error
    assert api == [42]
