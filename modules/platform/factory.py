from modules.exceptions import WindowManagerError

from .platform import find_os
from .window_managers.linux import WindowMgrLinux
from .window_managers.windows import get_window_mgr_on_windows


def get_window_manager():
    """Get Window Manager

    Raises:
        Exception: Could not find window manager for OS

    Returns:
        WindowManager: Window Manager Object for specific OS
    """
    operating_system = find_os()

    if operating_system == "windows":
        WindowMgrWindows = get_window_mgr_on_windows()
        return WindowMgrWindows()

    if operating_system == "linux":
        return WindowMgrLinux()

    raise WindowManagerError(f"OS not recognized: {operating_system}")
