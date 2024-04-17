import atexit
import inspect
import asyncio
import logging
import sys
import aiohttp
import re
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram import F
from .buttons import InlineButtons, ReplyButtons


already_started = False
dp = Dispatcher()


@dp.message(~F.text.startswith("/"))
async def message_handler(msg: Message) -> None:
    on_message = getattr(main_module, "on_message", None)
    if not on_message:
        raise ValueError("Нет функции on_message")
    
    
    async def answer(text, keyboard=None):
        if isinstance(keyboard, (InlineButtons, ReplyButtons)):
            message_instance = await msg.answer(text, reply_markup=keyboard.as_markup())
        else:
            message_instance = await msg.answer(text)
        
        return message_instance
    
    
    num_parms = len(inspect.signature(on_message).parameters)
    
    message = lambda: None
    message.answer = answer
    message.text = msg.text
    message.chat_id = msg.chat.id
    
    if num_parms == 0:
        args = tuple()
    elif num_parms == 1:
        args = (message,)
    else:
        raise ValueError("Функция on_message не должна иметь больше одного параметра")
    
    try:
        await on_message(*args)
    except Exception as e:
        await msg.answer("Возникла ошибка")
        raise e


@dp.message(F.text.startswith("/"))
async def command_handler(msg: Message) -> None:
    cmd = re.search(r"(?<=\/)[a-zA-Z_]*", msg.text).group()
    
    if cmd == "start":
        try:
            await set_chat_commands(dp.token, dp.commands, msg.from_user.id)
        except:
            pass
    
    on_command = getattr(main_module, f"on_command_{cmd}", None)
    
    if not on_command and cmd == "start":
        on_command = lambda msg: "Начинаем!"
    elif not on_command:
        raise ValueError(f"Нет функции для отработки команды {cmd}")

    
    async def answer(text, keyboard=None):
        if isinstance(keyboard, (InlineButtons, ReplyButtons)):
            message_instance = await msg.answer(text, reply_markup=keyboard.as_markup())
        else:
            message_instance = await msg.answer(text)
        
        return message_instance
    
    
    num_parms = len(inspect.signature(on_command).parameters)
    
    message = lambda: None
    message.answer = answer
    message.text = msg.text
    message.chat_id = msg.chat.id
    
    if num_parms == 0:
        args = tuple()
    elif num_parms == 1:
        args = (message, )
    else:
        raise ValueError(f"Функция on_command_{cmd} не должна иметь больше одного параметров")
    
    try:
        await on_command(*args)
    except Exception as e:
        await msg.answer("Возникла ошибка")
        raise e
    

@dp.callback_query()
async def inline_button_handler(callback: CallbackQuery):
    on_button = getattr(main_module, "on_button", None)
    if not on_button:
        raise ValueError("Нет функции on_button")
    
    
    async def answer(text, keyboard=None):
        await callback.answer()
        if isinstance(keyboard, (InlineButtons, ReplyButtons)):
            message_instance = await callback.message.answer(text, reply_markup=keyboard.as_markup())
        else:
            message_instance = await callback.message.answer(text)
        
        return message_instance
    
    
    num_parms = len(inspect.signature(on_button).parameters)
    
    call = lambda: None
    call.answer = answer
    call.chat_id = callback.message.chat.id
    call.data = callback.data
    call.delete = callback.message.delete
    
    if num_parms == 0:
        args = tuple()
    elif num_parms == 1:
        args = (call,)
    else:
        raise ValueError("Функция on_button не должна иметь больше одного параметра")
    
    try:
        await on_button(*args)
    except Exception as e:
        await callback.message.answer("Возникла ошибка")
        raise e


async def set_chat_commands(token, commands, chat_id) -> None:
    payload = {
        "commands": commands,
        "scope": {
            "type": "chat",
            "chat_id": chat_id
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://api.telegram.org/bot{token}/setMyCommands", json=payload) as resp:
            if resp.status == 200:
                print("Команды подключены!")


def find_command_handlers(main_module) -> list:
    commands = []
    for attr_name in dir(main_module):
        if attr_name.startswith("on_command_"):
            attr = getattr(main_module, attr_name)
            if callable(attr):
                command = attr_name[len("on_command_"):]
                description = attr.__doc__ or command
                commands.append({"command": command, "description": description})
    return commands


def run_bot(token) -> None:
    global already_started, main_module
    if already_started:
        return
    
    already_started = True
    
    main_module = sys.modules["__main__"]
    
    dp.token = token
    dp.commands = find_command_handlers(main_module)
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(Bot(token)))
    
    
def check_run_bot() -> None:
    if already_started:
        return
    
    raise ValueError("Необходимо добавить вызов функции run_bot(\"ВАШ ТОКЕН\") в самый конец кода для запуска бота")


if __name__ == "__main__":
    print("Модуль должен быть импортирован:\nfrom botmom import *")
    sys.exit()


atexit.register(check_run_bot)
