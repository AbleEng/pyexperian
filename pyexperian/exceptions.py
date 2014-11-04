

class InvalidNetConnectUrlException(Exception):
    def __init__(self):
        super(InvalidNetConnectUrlException, self).__init__("Net Connect URL is invalid.")


class EcalsLookupException(Exception):
    def __init__(self):
        super(EcalsLookupException, self).__init__("Failed to retrieve Net Connect URL via ECALS lookup.")


class MaxAuthAttemptsException(Exception):
    def __init__(self):
        super(MaxAuthAttemptsException, self).__init__("You've maxed out your authentication attempts.")


class FailedAuthException(Exception):
    def __init__(self):
        super(FailedAuthException, self).__init__("Wrong USER_ID and USER_PW.")


class ConfigException(Exception):
    def __init__(self):
        super(ConfigException, self).__init__("Check your config values and try again.")