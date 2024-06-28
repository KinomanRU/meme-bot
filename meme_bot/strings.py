from typing import Final

HELP: Final[str] = (
    "Supported commands:\n/anec - random anecdote\n/meme - random meme\n/gmeme - gif meme\n/vmeme - video meme"
)
HELLO: Final[str] = "Hello, %USER%! Welcome to Meme bot. \n\n" + HELP
CONTENT_ERROR: Final[str] = "Sorry, but there is a problem with content"
UNKNOWN_COMMAND: Final[str] = "Unknown command. Type /help for help."
