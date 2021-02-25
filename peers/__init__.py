class UserError(Exception):
    def __init__(self, message):
        self.msesage = message
