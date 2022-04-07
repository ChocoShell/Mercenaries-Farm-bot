import logging

from .conf import (ability_order, jposition, jthreshold, mercsAbilities,
                   mercslist)
from .settings import get_settings

log = logging.getLogger(__name__)

# Personalized Settings files
settings_filename = "settings.ini"

try:
    settings_dict = get_settings(settings_filename)

    log.info("Settings")
    for setting, value in settings_dict.items():
        log.info(f" - {setting}: {value}")
except Exception as e:
    log.error("Running without settings")


__all__ = [
    "jthreshold",
    "jposition",
    "mercslist",
    "mercsAbilities",
    "ability_order",
    "settings_dict",
]
