import configparser
import json
import logging
import re

from modules.exceptions import SettingsError

log = logging.getLogger(__name__)


def readjson(jfile):
    """... just for reading json file and return data :)"""
    with open(jfile) as descriptor:
        data = json.load(descriptor)

    return data


def read_ini_to_dict(inifile):
    """read ini file to parsed dictionary"""
    log.debug("Reading %s", inifile)
    return parse_ini(read_ini(inifile))


def parse_ini(inidict):
    """... just for transform value into right type"""
    initype = {}
    for k in inidict.keys():
        i = inidict[k].split("#")[0]
        if i in ["True", "False"]:
            initype[k] = i == "True"
        elif re.match("^[0-9]+$", i):
            initype[k] = int(i)
        elif re.match("^[0-9]+\.[0-9]+$", i):
            initype[k] = float(i)
        else:
            initype[k] = str(i)

    return initype


def read_ini(inifile):
    """... just for reading .ini file and return data"""
    config = configparser.ConfigParser()
    try:
        config.read(inifile)
    except configparser.DuplicateOptionError as err:
        log.error(err)
        raise SettingsError(f"Duplicate Option in Settings File: {err}") from err

    return config._sections
