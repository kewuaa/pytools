from pathlib import Path
import os

from .lib.alib import asynctk
from .lib.alib import aiofile
from . import logging
setting_path = Path(os.environ['Appdata']) / 'pytools'
setting_file = setting_path / 'setting.json'


async def __init():
    await aiofile.AWrapper(setting_path.mkdir)(exist_ok=True)


async def __load() -> dict:
    if not setting_file.exists():
        return {}
    async with aiofile.async_open(setting_file, 'r') as f:
        setting = await f.read()
    setting = await aiofile.ajson.loads(setting)
    return setting


def load(callback):
    def cb(fut) -> None:
        if fut.exception() is not None:
            logging.warning('load setting file failed')
            callback({})
        else:
            logging.info('setting file successfully loaded')
            callback(fut.result())
    if not callable(callback):
        raise ValueError('the input must be callable')
    asynctk.create_task(__load()).add_done_callback(cb)


async def save(setting: dict) -> None:
    if not setting:
        return
    old_st = await __load()
    old_st.update(setting)
    st = await aiofile.ajson.dumps(old_st)
    async with aiofile.async_open(setting_file, 'w') as f:
        await f.write(st)
    logging.info('setting successfully saved')


asynctk.create_task(__init())
