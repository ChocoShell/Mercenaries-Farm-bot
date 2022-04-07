import logging
import random
import time

from .campfire import look_at_campfire_completed_tasks
from .constants import Action, Button, UIElement
from .encounter import selectCardsInHand
from .game import waitForItOrPass
from .image_utils import find_ellement
from .mouse_utils import (mouse_click, mouse_position, mouse_range,
                          mouse_scroll, move_mouse, move_mouse_and_click)
from .platform import windowMP
from .settings import jposition, settings_dict

log = logging.getLogger(__name__)


def collect():
    """Collect the rewards just after beating the final boss of this level"""

    # it's difficult to find every boxes with lib CV2 so,
    # we try to detect just one and then we click on all known positions
    while not find_ellement(Button.done.filename, Action.move_and_click):
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 2.4)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.7, windowMP()[3] / 1.4)

        move_mouse_and_click(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2.7)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.7, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.6, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.8, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.9, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.4, windowMP()[3] / 1.3)
        time.sleep(1)

    # move the mouse to avoid a bug where the it is over a card/hero (at the end)
    # hiding the "OK" button
    move_mouse(windowMP(), windowMP()[2] // 1.25, windowMP()[3] // 1.25)
    # quit the bounty
    while not find_ellement(Button.finishok.filename, Action.move_and_click):
        time.sleep(1)
        mouse_click()
        time.sleep(0.5)


def quitBounty():
    end = False
    if find_ellement(Button.view_party.filename, Action.move_and_click):
        while not find_ellement(UIElement.your_party.filename, Action.move):
            time.sleep(0.5)
        while not find_ellement(Button.retire.filename, Action.move_and_click):
            time.sleep(0.5)
        while not find_ellement(Button.lockin.filename, Action.move_and_click):
            time.sleep(0.5)
        end = True
    return end


def nextlvl():
    """Progress on the map (Boon, Portal, ...) to find the next battle"""
    time.sleep(1.5)
    retour = True

    if not find_ellement(Button.play.filename, Action.screenshot):

        if find_ellement(Button.reveal.filename, Action.move_and_click):
            time.sleep(1)
            move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] // 1.25)
            time.sleep(1.5)

        elif find_ellement(Button.visit.filename, Action.move_and_click):
            pos_y = windowMP()[3] // 2.2
            time.sleep(7)
            while find_ellement(UIElement.visitor.filename, Action.screenshot):
                if settings_dict["stopatstranger"]:
                    log.info("Stopping after meeting Mysterious Stranger")
                    exit(1)

                temp = random.choice([3, 2, 1.7])
                pos_x = windowMP()[2] // temp

                move_mouse_and_click(windowMP(), pos_x, pos_y)

                time.sleep(0.2)
                find_ellement(Button.choose_task.filename, Action.move_and_click)
                time.sleep(3)
                mouse_click()
                time.sleep(8)

        elif find_ellement(
            UIElement.pick.filename, Action.move_and_click
        ) or find_ellement(Button.portal_warp.filename, Action.move_and_click):
            time.sleep(1)
            mouse_click()
            time.sleep(5)
        elif find_ellement(UIElement.surprise.filename, Action.screenshot):
            # type A
            time.sleep(1)
            find_ellement(UIElement.surprise.filename, Action.move_and_click)

        elif find_ellement(UIElement.spirithealer.filename, Action.screenshot):
            # type A
            time.sleep(1)
            find_ellement(UIElement.spirithealer.filename, Action.move_and_click)
        else:
            pos_x, pos_y = mouse_position(windowMP())
            log.debug("Mouse (x, y) : (%s, %s)", pos_x, pos_y)
            if (
                (windowMP()[3] // 2.2 + mouse_range)
                >= pos_y
                >= (windowMP()[3] // 2.2 - mouse_range)
            ):
                pos_x += windowMP()[2] // 25
            else:
                pos_x = windowMP()[2] // 3.7

            if pos_x > windowMP()[2] // 1.5:
                log.debug("Didn't find a battle. Try to go 'back'")
                find_ellement(Button.back.filename, Action.move_and_click)
                retour = False
            else:
                pos_y = windowMP()[3] // 2.2
                log.debug("Mouse (x, y) : (%s, %s)", pos_x, pos_y)
                move_mouse_and_click(windowMP(), pos_x, pos_y)

    return retour


def chooseTreasure():
    """used to choose a Treasure after a battle/fight
    Note: should be updated to select "good" (passive?) treasure instead of a random one
    """
    temp = random.choice([2.3, 1.7, 1.4])
    pos_y = windowMP()[3] // 2
    pos_x = windowMP()[2] // temp
    move_mouse_and_click(windowMP(), pos_x, pos_y)
    time.sleep(0.5)
    while True:
        if find_ellement(Button.take.filename, Action.move_and_click):
            time.sleep(1)
            break
        if find_ellement(Button.keep.filename, Action.move_and_click):
            time.sleep(1)
            break
        if find_ellement(Button.replace.filename, Action.move_and_click):
            time.sleep(1)
            break


def travelpointSelection():
    """Choose a Travel Point (The Barrens, Felwood, ...)
    and the mode : Normal or Heroic
    """

    if find_ellement(UIElement.travelpoint.filename, Action.screenshot):

        move_mouse(windowMP(), windowMP()[2] // 1.5, windowMP()[3] // 2)

        mouse_scroll(jposition["travelpoint.scroll.top"])
        time.sleep(0.5)

        location = settings_dict["location"]
        tag = f"travelpoint.{location}.scroll"
        if location == "The Barrens":
            find_ellement(UIElement.Barrens.filename, Action.move_and_click)

        else:
            try:
                mouse_scroll(jposition[tag])
                move_mouse(windowMP(), windowMP()[2] // 3, windowMP()[3] // 2)
                time.sleep(0.5)
                find_ellement(
                    getattr(UIElement, location).filename, Action.move_and_click
                )
            except Exception:
                log.error("Travel Point unknown : %s", location)

        move_mouse(windowMP(), windowMP()[2] // 2, windowMP()[3] // 2)
        time.sleep(0.5)

        if settings_dict["mode"] == "Normal":
            find_ellement(UIElement.normal.filename, Action.move_and_click)
        elif settings_dict["mode"] == "Heroic":
            find_ellement(UIElement.heroic.filename, Action.move_and_click)
        else:
            log.error("Settings (for Heroic/Normal) unrecognized.")

    waitForItOrPass(Button.choose_travel, 2)
    find_ellement(Button.choose_travel.filename, Action.move_and_click)


def goToEncounter():
    """
    Start new fight,
    continue on the road and collect everything (treasure, rewards, ...)
    """
    log.info("goToEncounter : entering")
    time.sleep(2)
    travelEnd = False

    while not travelEnd:
        # ToDo : add a tempo when pos_you detect a new completed task
        if find_ellement(Button.play.filename, Action.screenshot):
            if settings_dict["quitbeforebossfight"] == True and find_ellement(
                UIElement.boss.filename, Action.screenshot
            ):
                time.sleep(1)
                travelEnd = quitBounty()
                break

            find_ellement(Button.play.filename, Action.move_and_click)

            time.sleep(0.5)
            retour = (
                selectCardsInHand()
            )  # Start the battle : the bot choose the cards and fight against the enemy
            log.info("goToEncounter - retour = %s", retour)
            time.sleep(1)
            if retour == "win":
                log.info("goToEncounter : battle won")
                while True:
                    if find_ellement(UIElement.take_grey.filename, Action.screenshot):
                        chooseTreasure()
                        break

                    mouse_click()
                    time.sleep(0.5)

                    if find_ellement(
                        UIElement.replace_grey.filename, Action.screenshot
                    ):
                        chooseTreasure()
                        break

                    mouse_click()
                    time.sleep(0.5)

                    if find_ellement(
                        UIElement.presents_thing.filename, Action.screenshot
                    ):
                        log.info(
                            "goToEncounter : " "Boss defeated. Time for REWARDS !!!"
                        )
                        collect()
                        travelEnd = True
                        break
            elif retour == "loose":
                travelEnd = True
                log.info("goToEncounter : Battle lost")
            else:
                travelEnd = True
                log.info("goToEncounter : don't know what happened !")

            waitForItOrPass(UIElement.campfire.filename, 5)
            look_at_campfire_completed_tasks()

        elif not nextlvl():
            break

    while not find_ellement(Button.back.filename, Action.screenshot):
        mouse_click()
        time.sleep(1)


def travelToLevel(page="next"):
    """
    Go to a Travel Point, choose a level/bounty and go on the road to make encounter
    """

    retour = False

    if find_ellement(
        f"levels/{settings_dict['location']}"
        f"_{settings_dict['mode']}_{settings_dict['level']}.png",
        Action.move_and_click,
        0.5,
    ):
        waitForItOrPass(Button.start, 6)
        find_ellement(Button.start.filename, Action.move_and_click)
        retour = True
    elif page == "next":
        if find_ellement(Button.sec.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("next")
        if retour is False and find_ellement(
            Button.fir.filename, Action.move_and_click
        ):
            time.sleep(1)
            retour = travelToLevel("previous")
        elif retour is False:
            find_ellement(Button.back.filename, Action.move_and_click)
    elif page == "previous":
        if find_ellement(Button.fir.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("previous")
        else:
            find_ellement(Button.back.filename, Action.move_and_click)
    return retour
