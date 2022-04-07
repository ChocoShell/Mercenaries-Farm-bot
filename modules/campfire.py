import logging
import random
import time

from .constants import Action, Button, UIElement
from .game import waitForItOrPass
from .image_utils import find_ellement
from .mouse_utils import (mouse_click, mouse_position, mouse_range,
                          mouse_scroll, move_mouse, move_mouse_and_click)
from .platform import windowMP
from .settings import jposition, settings_dict

log = logging.getLogger(__name__)


def look_at_campfire_completed_tasks():
    """Once opened, look at campfire if you find completed tasks and, if so, open them"""

    if find_ellement(UIElement.campfire.filename, Action.screenshot):
        while find_ellement(UIElement.campfire.filename, Action.screenshot):
            waitForItOrPass(Button.campfire_completed_task, 5)
            if find_ellement(
                Button.campfire_completed_task.filename, Action.move_and_click
            ):
                while not find_ellement(
                    Button.campfire_claim.filename, Action.move_and_click
                ):
                    time.sleep(0.5)

                while not find_ellement(UIElement.campfire.filename, Action.screenshot):
                    mouse_click()
                    time.sleep(1)
            else:
                break

        move_mouse_and_click(windowMP(), windowMP()[2] / 1.25, windowMP()[3] / 2)
