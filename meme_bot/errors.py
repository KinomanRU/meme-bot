class BotNoToken(Exception):
    def __init__(self, *args: object) -> None:
        self._msg = "BOT_TOKEN environment variable is not set"
        super().__init__(self._msg, *args)

    def __str__(self):
        return self._msg
