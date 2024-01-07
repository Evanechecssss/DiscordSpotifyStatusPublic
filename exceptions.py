class AccessTokenExpired(BaseException):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"Spotify requires a new token.\n{self.message}"
        else:
            return f"Spotify requires a new token."