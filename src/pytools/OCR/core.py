from typing import Optional, Iterator
from urllib.parse import quote
from base64 import b64encode
from pathlib import Path
import asyncio
import json

from aiohttp import ClientSession
import aiofiles

from .. import logging
from ..types import AnyPath


class Recognizer:
    """文字识别类。"""

    URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'

    def __init__(
        self,
        loop: Optional[asyncio.base_events.BaseEventLoop] = None
    ) -> None:
        self._loop = loop = loop or asyncio.get_event_loop()
        self._sess = ClientSession(loop=loop)
        self._keys = loop.create_task(self._load_api_keys())
        self._token = loop.create_task(self._init_access_token())
        self._concurrency = 2

    def reset_concurrency(self, concurrency: int) -> None:
        """重新设置并发量。

        :param concurrency: 并发量大小
        """

        self._concurrency = concurrency
        if concurrency > 2:
            logging.info(f'concurrency has been setted to {concurrency}, '
                         'make sure that your account support it')

    def _encode(self, data: bytes) -> str:
        """对 URL 进行编码。

        :param data: 需要编码的数据
        :return: 编码完成的 URL
        """

        b64str = b64encode(data).decode()
        url_encoded = quote(b64str)
        return url_encoded

    async def _load_api_keys(self) -> tuple:
        """获取 API 的密钥。

        :return: (API_KEY, SECRET_KEY)
        """

        home_path = Path.home()
        config_path = home_path / '.config/baidu'
        config_path.mkdir(exist_ok=True)
        setting_path = config_path / 'config.json'
        if not setting_path.exists():
            msg = f'do not find any config file at {str(setting_path)}'
            logging.warning(msg)
            raise RuntimeError(msg)
        async with aiofiles.open(setting_path, 'r') as f:
            lines = await f.read()
        config = json.loads(lines.strip())
        if ('API_KEY' not in config) | ('SECRET_KEY' not in config):
            msg = 'please check you config and make sure that '
            'API_KEY and SECRET_KEY should be both within it'
            logging.warning(msg)
            raise RuntimeError(msg)
        return config['API_KEY'], config['SECRET_KEY']

    async def _init_access_token(self) -> str:
        """初始化 token 参数。"""

        url = 'https://aip.baidubce.com/oauth/2.0/token'
        api_key, secret_key = await self._keys
        params = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": secret_key,
        }
        resp = await self._sess.post(url, params=params)
        resp_dict = await resp.json(content_type=None)
        token = resp_dict.get('access_token')
        if not token:
            msg = 'API_KEY and SECRET_KEY error'
            logging.error(msg)
            raise RuntimeError(msg)
        return token

    async def _send_data(self, data: dict) -> str:
        """对文件内容进行识别。

        :param data: 需要发送的数据
        :return: 返回的结果
        """
        token = await self._token
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        payload = '&'.join(f'{k}={v}' for k, v in data.items() if v)
        resp = await self._sess.post(
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

    async def recognize(
        self,
        files: Optional[Iterator[AnyPath]],
    ) -> dict:
        """对文件输入进行识别。

        :param files: 需要识别的一个或多个文件
        :return: 返回字典形式的结果
        """

        async def parse(file: AnyPath):
            data = {}
            if str(file).startswith('http'):
                data['url'] = file
            else:
                async with aiofiles.open(file, 'rb') as f:
                    content = await f.read()
                if Path(file).suffix == '.pdf':
                    data['pdf_file'] = content
                else:
                    data['image'] = content
            return await self._send_data(data)
        coros = {file: parse(file) for file in files}
        concurrency = self._concurrency
        result = {}
        for i in range(0, len(coros), concurrency):
            tasks = {
                coro_id: self._loop.create_task(coros[coro_id])
                for coro_id in coros.keys()[i: i + concurrency]
            }
            for _id, task in tasks:
                result[_id] = await task
        logging.info('successfully recognized')
        return result

    async def exit(self):
        """关闭会话。"""

        await self._sess.close()
