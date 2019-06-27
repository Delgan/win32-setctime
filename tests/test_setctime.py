import time
import os
import pathlib
from os.path import getctime

import pytest

from win32_setctime import setctime


def test_setctime(tmp_path):
    filepath = tmp_path / "test_setctime.txt"
    timestamp = 946681200
    filepath.touch()
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_timestamp_negative(tmp_path):
    filepath = tmp_path / "test_timestamp_negative.txt"
    timestamp = -5694948000
    filepath.touch()
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_timestamp_with_nanoseconds(tmp_path):
    filepath = tmp_path / "test_timestamp_with_nanoseconds.txt"
    timestamp = 737206464.123456789
    filepath.touch()
    setctime(filepath, timestamp)
    assert pytest.approx(getctime(filepath), timestamp)


def test_timestamp_lower_bound(tmp_path):
    filepath = tmp_path / "test_timestamp_lower_sdfds.dds"
    timestamp = -11644473599
    filepath.touch()
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_timestamp_exceeds_lower_bound(tmp_path):
    filepath = tmp_path / "test_timestamp_exceeds_lower_bound.txt"
    timestamp = -11644473600
    filepath.touch()
    with pytest.raises(ValueError):
        setctime(filepath, timestamp)


def tes_timestamp_upper_bound(tmp_path):
    filepath = tmp_path / "tes_timestamp_upper_bound.txt"
    timestamp = 1833029933770.9551615
    filepath.touch()
    setctime(filepath, timestamp)
    assert pytest.approx(getctime(filepath), timestamp)


def test_timestamp_exceeds_upper_bound(tmp_path):
    filepath = tmp_path / "test_timestamp_exceeds_upper_bound.txt"
    timestamp = 1833029933770.9551616
    filepath.touch()
    with pytest.raises(ValueError):
        setctime(filepath, timestamp)


def test_file_does_not_exist(tmp_path):
    filepath = tmp_path / "test_file_does_not_exist.txt"
    timestamp = 123456789
    with pytest.raises(OSError):
        setctime(filepath, timestamp)


def test_file_already_opened_read(tmp_path):
    filepath = tmp_path / "test_file_already_opened_read.txt"
    timestamp = 123456789
    filepath.touch()
    with open(filepath, "r"):
        setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_file_already_opened_write(tmp_path):
    filepath = tmp_path / "test_file_already_opened_write.txt"
    timestamp = 123456789
    with open(filepath, "w"):
        setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_file_already_opened_exclusive(tmp_path):
    filepath = tmp_path / "test_file_already_opened_write.txt"
    timestamp = 123456789
    with open(filepath, "x"):
        setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_file_unicode(tmp_path):
    filepath = tmp_path / "𤭢.txt"
    timestamp = 123456789
    filepath.touch()
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_forward_slash(tmp_path):
    folder = tmp_path / "foo" / "bar" / "baz"
    filepath = folder / "test_forward_slash.txt"
    timestamp = 123456789
    folder.mkdir(exist_ok=True, parents=True)
    filepath.touch()
    setctime(str(filepath).replace(r"\\", "/"), timestamp)
    assert getctime(filepath) == timestamp


def test_mtime_not_modified(tmp_path):
    filepath = tmp_path / "test_mtime_not_modified.txt"
    filepath.touch()
    before = os.path.getmtime(filepath)
    time.sleep(0.1)
    setctime(filepath, 123456789)
    assert os.path.getmtime(filepath) == before


def test_atime_not_modified(tmp_path):
    filepath = tmp_path / "test_atime_not_modified.txt"
    filepath.touch()
    before = os.path.getatime(filepath)
    time.sleep(0.1)
    setctime(filepath, 123456789)
    assert os.path.getatime(filepath) == before


def test_fix_file_tunneling(tmp_path):
    filepath = tmp_path / "test_fix_file_tunneling.txt"
    timestamp = 123456789
    filepath.touch()
    before = getctime(filepath)
    time.sleep(0.1)
    os.remove(filepath)
    filepath.touch()
    assert getctime(filepath) == before
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp
