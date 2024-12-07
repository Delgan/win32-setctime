import os
import time

import pytest

from win32_setctime import setctime, SUPPORTED


def getctime(filepath):
    # Fix for Python 3.5 not supporting pathlib
    return os.path.getctime(str(filepath))


def test_supported():
    assert SUPPORTED


def test_setctime(tmp_path):
    filepath = tmp_path / "test_setctime.txt"
    timestamp = 946681200
    filepath.touch()
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_directory(tmp_path):
    dirpath = tmp_path / "temp_dir"
    timestamp = 826618926
    dirpath.mkdir()
    setctime(dirpath, timestamp)
    assert getctime(dirpath) == timestamp


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
    assert getctime(filepath) == pytest.approx(timestamp)


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


def test_timestamp_far_in_the_future(tmp_path):
    filepath = tmp_path / "test_timestamp_far_in_the_future.txt"
    timestamp = 64675581821
    filepath.touch()
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_timestamp_exceeds_upper_bound(tmp_path):
    filepath = tmp_path / "test_timestamp_exceeds_upper_bound.txt"
    timestamp = 1833029933770.9551616
    filepath.touch()
    with pytest.raises(ValueError):
        setctime(filepath, timestamp)


def test_file_does_not_exist(tmp_path):
    filepath = tmp_path / "test_file_does_not_exist.txt"
    timestamp = 123456789
    with pytest.raises(FileNotFoundError):
        setctime(filepath, timestamp)


def test_file_already_opened_read(tmp_path):
    filepath = tmp_path / "test_file_already_opened_read.txt"
    timestamp = 123456789
    filepath.touch()
    with open(str(filepath), "r"):
        setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_file_already_opened_write(tmp_path):
    filepath = tmp_path / "test_file_already_opened_write.txt"
    timestamp = 123456789
    with open(str(filepath), "w"):
        setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


def test_file_already_opened_exclusive(tmp_path):
    filepath = tmp_path / "test_file_already_opened_write.txt"
    timestamp = 123456789
    with open(str(filepath), "x"):
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
    before = os.path.getmtime(str(filepath))
    time.sleep(0.1)
    setctime(filepath, 123456789)
    assert os.path.getmtime(str(filepath)) == before


def test_atime_not_modified(tmp_path):
    filepath = tmp_path / "test_atime_not_modified.txt"
    filepath.touch()
    before = os.path.getatime(str(filepath))
    time.sleep(0.1)
    setctime(filepath, 123456789)
    assert os.path.getatime(str(filepath)) == before


def test_fix_file_tunneling(tmp_path):
    filepath = tmp_path / "test_fix_file_tunneling.txt"
    timestamp = 123456789
    filepath.touch()
    before = getctime(filepath)
    time.sleep(0.1)
    os.remove(str(filepath))
    filepath.touch()
    assert getctime(filepath) == before
    setctime(filepath, timestamp)
    assert getctime(filepath) == timestamp


@pytest.mark.parametrize("follow_symlinks", [True, False])
def test_with_symlinks(tmp_path, follow_symlinks):
    target_path = tmp_path / "target.txt"
    symlink_path = tmp_path / "symlink.txt"
    timestamp = 123456789
    target_path.touch()
    time.sleep(0.1)
    symlink_path.symlink_to(target_path)
    target_ctime = target_path.lstat().st_ctime
    symlink_ctime = symlink_path.lstat().st_ctime

    assert target_ctime != symlink_ctime

    setctime(symlink_path, timestamp, follow_symlinks=follow_symlinks)

    if follow_symlinks:
        assert symlink_path.lstat().st_ctime == symlink_ctime
        assert target_path.lstat().st_ctime == timestamp
    else:
        assert symlink_path.lstat().st_ctime == timestamp
        assert target_path.lstat().st_ctime == target_ctime
