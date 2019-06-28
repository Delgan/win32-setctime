import os

try:
    from ctypes import windll, wintypes, byref, FormatError, WinError

    CreateFileW = windll.kernel32.CreateFileW
    SetFileTime = windll.kernel32.SetFileTime
    CloseHandle = windll.kernel32.CloseHandle

    CreateFileW.argtypes = (
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    CreateFileW.restype = wintypes.HANDLE

    SetFileTime.argtypes = (
        wintypes.HANDLE,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
    )
    SetFileTime.restype = wintypes.BOOL

    CloseHandle.argtypes = (wintypes.HANDLE,)
    CloseHandle.restype = wintypes.BOOL
except (ImportError, AttributeError, OSError, ValueError):
    SUPPORTED = False
else:
    SUPPORTED = os.name == "nt"


__version__ = "1.0.1"
__all__ = ["setctime"]


def setctime(filepath, timestamp):
    """Set the "ctime" (creation time) attribute of a file given an unix timestamp (Windows only)."""
    if not SUPPORTED:
        raise OSError("This function is only available for the Windows platform.")

    filepath = os.path.normpath(os.path.abspath(str(filepath)))
    timestamp = int((timestamp * 10000000) + 116444736000000000)

    if not 0 < timestamp < (1 << 64):
        raise ValueError("The system value of the timestamp exceeds u64 size: %d" % timestamp)

    atime = wintypes.FILETIME(0xFFFFFFFF, 0xFFFFFFFF)
    mtime = wintypes.FILETIME(0xFFFFFFFF, 0xFFFFFFFF)
    ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)

    handle = wintypes.HANDLE(CreateFileW(filepath, 256, 0, None, 3, 128, None))
    if handle.value == wintypes.HANDLE(-1).value:
        raise WinError()

    if not wintypes.BOOL(SetFileTime(handle, byref(ctime), byref(atime), byref(mtime))):
        raise WinError()

    if not wintypes.BOOL(CloseHandle(handle)):
        raise WinError()
