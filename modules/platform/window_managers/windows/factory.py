import logging

from .ahk_manager import HAS_AHK, WindowMgrWindowsAHK
from .win32gui_manager import HAS_WIN32GUI, WindowMgrWindowsWin32Gui

log = logging.getLogger(__name__)


def get_window_mgr_on_windows():
    if HAS_WIN32GUI:
        return WindowMgrWindowsWin32Gui
    elif HAS_AHK:
        return WindowMgrWindowsAHK
    else:
        log.error("No Window Manager found for Windows")
