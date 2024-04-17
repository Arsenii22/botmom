# Botmom

Простая и многофункциональная библиотека для создания своих ботов для телеграмм


## Установка

Введите в терминал:

```bash
pip install botmom --upgrade --user
```

или запустите этот код:

```python
import os, sys

python = sys.executable
user = '--user' if 'venv' not in python and 'envs' not in python else ''
cmd = f'"{python}" -m pip install botmom --upgrade {user}'
os.system(cmd)
```


## Примеры

Простой echo-бот:

```python
from botmom import *

async def on_message(msg):
    await msg.answer("Твоё сообщение: " + msg.text)

run_bot("TOKEN_FROM_BOTFATHER")
```

Простой работа с командами:

```python
from botmom import *

async def on_command_start(cmd):
    await cmd.answer("Привет! \nДля помощи - напиши /help")


async def on_command_help(cmd):
    await cmd.answer("Пока ничем не могу помочь :(")


run_bot("TOKEN_FROM_BOTFATHER")
```

Создание Inline-кнопок

```python
from botmom import *

async def on_command_start(cmd):
    buttons = InlineButtons({"Да": "help_yes", "Нет": "help_no"})

    await cmd.answer("Привет! Тебе помочь?", buttons)


async def on_button(callback):
    if callback.data == "help_yes":
        await callback.answer("Тогда слушай внимательно!")

    elif callback.data == "help_no":
        msg = await callback.answer("Ну и ладно")
        
        await asyncio.sleep(3) # Вместо time.sleep(), время в секундах
        await msg.delete() # Удалит сообщение "Ну и ладно"
       

run_bot("TOKEN_FROM_BOTFATHER")
```


Создание Reply-кнопок

```python
from botmom import *

states = dict()

async def on_command_start(cmd):
    buttons = ReplyButtons(["Да", "Нет"])

    await cmd.answer("Привет! Тебе помочь?", buttons)
    states[cmd.chat_id] = "waiting"


async def on_message(msg):
    if states[cmd.chat_id] == "waiting" and msg.text == "Да":
        buttons = ReplyButtons(["Окей"])

        await msg.answer("Тогда слушай внимательно!", buttons)

    if states[cmd.chat_id] == "waiting" and msg.text == "Да":
        buttons = ReplyButtons() # Удалить все кнопки

        ok_msg = await msg.answer("Ну и ладно", buttons)

        await asyncio.sleep(3) # Вместо time.sleep(), время в секундах
        await ok_msg.delete() # Удалит сообщение "Ну и ладно"
        

run_bot("TOKEN_FROM_BOTFATHER")
```


