from .log import logger_group
from .config import config
from .commands import *
from logbook import Logger
from bs4 import BeautifulSoup, PageElement, Tag
import simplematrixbotlib as botlib 

logger = Logger("bot.util")
logger_group.add_logger(logger)

_username = config.get("username")

def detect_mention_at_beginning(soup: BeautifulSoup) -> bool:
    first_element = soup.find()
    if first_element and isinstance(first_element, Tag):
        if first_element.name == 'a':
            first_element_link = first_element.get('href')
            if first_element_link and isinstance(first_element_link, str):
                if first_element_link.find(f"@{_username}"):
                    first_element.replace_with()
                    if soup.contents:
                        rest = soup.contents[0]
                        rest_text = rest.getText()
                        rest.replace_with(rest_text.removeprefix(':').lstrip())
                    return True
    return False

async def detect_command(soup: BeautifulSoup, room_id: str, bot: botlib.Bot):
    if soup.contents:
        command = soup.contents[0].getText().split()
        if command:
            command_length = len(command)
            if command[0] == 'help':
                if command_length == 2:
                    if command[1] in ['info', 'list', 'delete', 'active', 'activate', 'new']:
                        await help(room_id, bot, command[1])
                        return True
                elif command_length == 1:
                    await help(room_id, bot, '')
                    return True
            elif command_length == 1:
                if command[0] == 'info':
                    await info(room_id, bot)
                    return True
                elif command[0] == 'active':
                    await active(room_id, bot)
                    return True
                elif command[0] == 'list':
                    await list(room_id, bot)
                    return True
            elif command_length == 2:
                if command[0] == 'delete':
                    await delete(room_id, bot, command[1])
                    return True
                elif command[0] == 'activate':
                    await activate(room_id, bot, command[1])
                    return True
    return False

async def process_message(soup: BeautifulSoup, room_id: str, bot: botlib.Bot, mentioned=False):
    new = False
    if soup.contents:
        message = soup.contents[0].getText()
        command = message.split()
        if command:
            if command[0] == 'new':
                command = command[0]
                soup.contents[0].replace_with(message.removeprefix(command).lstrip())
                if len(soup.decode()) == 0:
                    await new_error(room_id, bot)
                    return
                new = True
    for link in soup.find_all("a"):
        if link.get("href").find(f"@{_username}"):
            link.replace_with("ChatGPT")
            if not mentioned: mentioned = True
    if not mentioned:
        return
    await generic(room_id, bot, soup.decode(), new)