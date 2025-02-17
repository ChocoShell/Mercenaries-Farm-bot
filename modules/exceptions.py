class MercenariesFarmBaseException(Exception):
    pass


class SettingsError(MercenariesFarmBaseException):
    pass


class MissingGameDirectory(SettingsError):
    pass


class UnsetGameDirectory(SettingsError):
    pass
