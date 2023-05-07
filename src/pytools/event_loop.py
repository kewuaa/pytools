import asyncio


def start(loop: asyncio.base_events.BaseEventLoop) -> None:
    """启动事件循环。"""

    async def shutdown(loop: asyncio.base_events.BaseEventLoop) -> None:
        await loop.shutdown_asyncgens()
        await loop.shutdown_default_executor()
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        for task in asyncio.tasks.all_tasks(loop=loop):
            task.cancel()
        loop.run_until_complete(shutdown(loop))
        loop.close()
