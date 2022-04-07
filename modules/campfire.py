"""
Campfire

Handle the campfire window with tasks
"""
import logging
import time

from .constants import Action, Button, UIElement
from .game import waitForItOrPass
from .image_utils import find_ellement
from .mouse_utils import mouse_click, move_mouse_and_click
from .platform import windowMP

log = logging.getLogger(__name__)


def look_at_campfire_completed_tasks():
    """Once opened, look at campfire if you find completed tasks and, if so, open them"""

    if not find_ellement(UIElement.campfire.filename, Action.screenshot):
        return
    while find_ellement(UIElement.campfire.filename, Action.screenshot):
        waitForItOrPass(Button.campfire_completed_task, 5)
        if not find_ellement(
            Button.campfire_completed_task.filename, Action.move_and_click
        ):
            break

        while not find_ellement(Button.campfire_claim.filename, Action.move_and_click):
            time.sleep(0.5)

        while not find_ellement(UIElement.campfire.filename, Action.screenshot):
            mouse_click()
            time.sleep(1)
    move_mouse_and_click(windowMP(), windowMP()[2] / 1.25, windowMP()[3] / 2)
