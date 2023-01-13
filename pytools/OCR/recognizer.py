from urllib.parse import quote
from base64 import b64encode
from pathlib import Path
import asyncio
import json

from aiohttp import ClientSession

from pytools import logging
from pytools.libs import aiofile


class Recognizer:
    support_type = ('.jpg', '.jpeg', '.png', '.bmp', '.pdf')
    URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'

    def __init__(self, loop: asyncio.base_events.BaseEventLoop = None) -> None:
        self.__loop = loop = loop or asyncio.get_event_loop()
        self.__sess = ClientSession(loop=loop)
        self.__keys = loop.create_task(self.__load_api_keys())
        self.__token = loop.create_task(self.__init_access_token())
        self.__concurrency = 2

    @property
    def concurrency(self) -> int:
        return self.__concurrency

    def reset_concurrency(self, concurrency: int) -> None:
        self.__concurrency = concurrency
        if concurrency > 2:
            logging.info(f'concurrency has been setted to {concurrency}, '
                         'make sure that you account support it')

    def __encode(self, data: bytes) -> str:
        b64str = b64encode(data).decode()
        url_encoded = quote(b64str)
        return url_encoded

    async def __load_api_keys(self) -> tuple:
        home_path = Path.home()
        config_path = home_path / '.config/baidu'
        config_path.mkdir(exist_ok=True)
        setting_path = config_path / 'config.json'
        if not setting_path.exists():
            msg = f'do not find any config file at {str(setting_path)}'
            logging.warning(msg)
            raise RuntimeError(msg)
        async with aiofile.async_open(setting_path, 'r') as f:
            lines = await f.read()
        config = json.loads(lines.strip())
        if ('API_KEY' not in config) | ('SECRET_KEY' not in config):
            msg = 'please check you config and make sure that '
            'API_KEY and SECRET_KEY should be both within it'
            logging.warning(msg)
            raise RuntimeError(msg)
        return config['API_KEY'], config['SECRET_KEY']

    async def __init_access_token(self) -> str:
        url = 'https://aip.baidubce.com/oauth/2.0/token'
        api_key, secret_key = await self.__keys
        params = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": secret_key,
        }
        resp = await self.__sess.post(url, params=params)
        resp_dict = await resp.json(content_type=None)
        token = resp_dict.get('access_token')
        if not token:
            msg = 'API_KEY and SECRET_KEY error'
            logging.error(msg)
            raise RuntimeError(msg)
        return token

    async def __recognize(self, file: Path, **params) -> str:
        token = await self.__token
        data = params
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        if not file:
            image_data = data.get('image')
            pdf_data = data.get('pdf_file')
            if image_data is not None:
                data['image'] = self.__encode(image_data)
                data.pop('pdf_file', None)
            elif pdf_data is not None:
                data['pdf_file'] = self.__encode(pdf_data)
            else:
                msg = 'not enough parameters, "image" or "pdf_file" is needed'
                logging.error(msg)
                raise RuntimeError(msg)
        elif str(file).startswith('http'):
            data['url'] = file
        else:
            suffix = file.suffix
            if suffix not in self.support_type:
                msg = f'do not support {suffix} type'
                logging.error(msg)
                raise RuntimeError(msg)
            async with aiofile.async_open(file, 'rb') as f:
                content = await f.read()
            if suffix == '.pdf':
                data['pdf_file'] = self.__encode(content)
            else:
                data['image'] = self.__encode(content)
        payload = '&'.join(f'{k}={v}' for k, v in data.items() if v)
        resp = await self.__sess.post(
            self.URL,
            headers=headers,
            params={'access_token': token},
            data=payload,
        )
        resp_dict = await resp.json(content_type=None)
        if 'error_code' in resp_dict:
            msg = resp_dict['error_msg']
            logging.error(msg)
            raise RuntimeError(msg)
        return '\n'.join(
            result['words']
            for result in resp_dict['words_result']
        )

    async def recognize(self, path: str or Path, **params) -> str or dict:
        if not path:
            return await self.__recognize('', **params)
        path = Path(path)
        if path.is_file():
            result = await self.__recognize(path)
        elif path.is_dir():
            files = tuple(
                file
                for file in path.iterdir()
                if file.suffix in self.support_type
            )
            if not files:
                msg = f'no supported file found in {path}\n'\
                    f'{", ".join(self.support_type)} are supported'
                logging.error(msg)
                raise RuntimeError(msg)
            cores = [
                self.__recognize(file)
                for file in files
            ]
            concurrency = self.__concurrency
            result = {}
            for i in range(0, len(cores), concurrency):
                tasks = [
                    self.__loop.create_task(coro)
                    for coro in cores[i: i + concurrency]
                ]
                result.update({
                    files[i + j].stem: await task
                    for j, task in enumerate(tasks)
                })
        else:
            msg = f'"{path}" not a file or directory'
            logging.error(msg)
            raise RuntimeError(msg)
        logging.info('successfully recognized')
        return result

    async def exit(self):
        await self.__sess.close()
