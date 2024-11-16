class CredentialException(Exception):
    """ Custom Exception for Credentials """
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self):
        return self.detail

    def __repr__(self):
        return self.detail
