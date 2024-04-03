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

TOKEN = "token from botfather"

def on_message(msg: str):
    return "Твоё сообщение: " + msg

run_bot(TOKEN)
```

