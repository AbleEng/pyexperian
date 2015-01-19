

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
        super(FailedAuthException, self).__init__("Bad credentials.  Did you remember to reset your password?")


class PasswordExpiredException(Exception):
    def __init__(self):
        super(PasswordExpiredException, self).__init__("Your password is expired.")


class BadRequestException(Exception):
    def __init__(self, msg=''):
        super(BadRequestException, self).__init__(msg or "Check your config and query data for bad or missing values.")


class TermsException(Exception):
    def __init__(self):
        super(TermsException, self).__init__("Re-submit your request if you have consent to request the customer's personal credit.")


class IncompleteOwnerException(Exception):
    def __init__(self, msg):
        super(IncompleteOwnerException, self).__init__(msg)


class IncompleteBusinessException(Exception):
    def __init__(self, msg):
        super(IncompleteBusinessException, self).__init__(msg)