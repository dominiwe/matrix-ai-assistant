import simplematrixbotlib as botlib
from bs4 import BeautifulSoup
import nio
from .config import config
from .log import logger_group
from .util import detect_mention_at_beginning, detect_command, process_message
from logbook import Logger

logger = Logger("bot.bot")
logger_group.add_logger(logger)

_creds = botlib.Creds(
    homeserver=config.get("homeserver"),
    username=config.get("username"),
    access_token=config.get("access_token"),
)

_config = botlib.Config()

# Default config
_config.join_on_invite = False
_config.encryption_enabled = False
# If encryption was enabled
_config.emoji_verify = True
_config.ignore_unverified_devices = True

bot = botlib.Bot(_creds, _config)

logger.info("Bot instance initialized.")

@bot.listener.on_startup
async def membership_information(room_id):
    logger.debug(f"Bot is a member of room with id {room_id}.")

@bot.listener.on_custom_event(nio.Event)
async def handle(room: nio.MatrixRoom, event: nio.RoomMessageFormatted):
    try:
        if not isinstance(event, nio.RoomMessageFormatted): return
        match = botlib.MessageMatch(room, event, bot)
        if not match.is_not_from_this_bot: return # bot shouldn't trigger itself
        source = event.flattened()
        formatted_body: str = source.get("content.formatted_body") # type: ignore
        if not formatted_body: return
        soup = BeautifulSoup(formatted_body, "html.parser")
        links = soup.find_all("a")
        mentioned = False
        if detect_mention_at_beginning(soup):
            mentioned = True
            if len(links) == 1 and len(soup.contents) == 1:
                if not await detect_command(soup, room.room_id, bot):
                    await process_message(soup, room.room_id, bot, mentioned)
            else:
                await process_message(soup, room.room_id, bot, mentioned)
        else:
            await process_message(soup, room.room_id, bot, mentioned)
    except Exception as e:
        logger.error('Error while reacting to event...')
        logger.error(e)
        pass